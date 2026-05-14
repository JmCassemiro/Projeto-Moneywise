from datetime import datetime
from decimal import Decimal, InvalidOperation

from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import NotFoundError, ValidationError
from app.extensions import db
from app.transactions.models import Transaction
from app.transactions.repositories import TransactionRepository


CATEGORY_COLORS = {
    "Casa": "#F7B7B7",
    "Viagem": "#B2D7F6",
    "Entretenimento": "#F1D7A7",
    "Estudos": "#B7D6B5",
    "Saúde": "#F5D1D1",
    "Mercado": "#D0E5D7",
}

FILTER_KEYS = [
    "search",
    "filter-type",
    "filter-category",
    "filter-start-date",
    "filter-end-date",
    "filter-min-amount",
    "filter-max-amount",
    "filter-payment-method",
]


class TransactionService:
    @staticmethod
    def build_filters(args) -> dict:
        filters = {key: args.get(key) for key in FILTER_KEYS}
        for key in ("filter-start-date", "filter-end-date"):
            if filters.get(key):
                filters[key] = TransactionService._parse_date(filters[key])
        for key in ("filter-min-amount", "filter-max-amount"):
            if filters.get(key):
                filters[key] = TransactionService._parse_amount(filters[key])
        return filters

    @staticmethod
    def list_transactions(filters: dict, user_id: int | str) -> list[dict]:
        transactions = TransactionRepository.list_for_user(filters, user_id)
        return [transaction.to_dict() for transaction in transactions]

    @staticmethod
    def get_transaction(transaction_id: int, user_id: int | str) -> dict:
        transaction = TransactionRepository.get_for_user(transaction_id, user_id)
        if not transaction:
            raise NotFoundError("Transacao nao encontrada.")
        return transaction.to_dict()

    @staticmethod
    def create_transaction(form_data, user_id: int | str) -> Transaction:
        transaction = Transaction(
            user_id=int(user_id),
            **TransactionService._clean_form_data(form_data),
        )
        try:
            return TransactionRepository.create(transaction)
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise ValidationError("Erro ao criar transacao.") from exc

    @staticmethod
    def update_transaction(
        transaction_id: int,
        form_data,
        user_id: int | str,
    ) -> Transaction:
        transaction = TransactionRepository.get_for_user(transaction_id, user_id)
        if not transaction:
            raise NotFoundError("Transacao nao encontrada.")

        data = TransactionService._clean_form_data(form_data)
        for key, value in data.items():
            setattr(transaction, key, value)

        try:
            TransactionRepository.save()
            return transaction
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise ValidationError("Erro ao atualizar transacao.") from exc

    @staticmethod
    def delete_transaction(transaction_id: int, user_id: int | str) -> None:
        transaction = TransactionRepository.get_for_user(transaction_id, user_id)
        if not transaction:
            raise NotFoundError("Transacao nao encontrada.")

        try:
            TransactionRepository.delete(transaction)
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise ValidationError("Erro ao deletar transacao.") from exc

    @staticmethod
    def _clean_form_data(form_data) -> dict:
        is_recurring = form_data.get("is_recurring") in {
            "on",
            "true",
            "True",
            "1",
        }
        data = {
            "title": TransactionService._required(form_data, "title"),
            "amount": TransactionService._parse_amount(
                TransactionService._required(form_data, "amount")
            ),
            "category": TransactionService._required(form_data, "category"),
            "payment_method": TransactionService._required(
                form_data,
                "payment_method",
            ),
            "description": (form_data.get("description") or "").strip(),
            "transaction_date": TransactionService._parse_date(
                form_data.get("transaction_date")
            ),
            "transaction_hour": TransactionService._parse_time(
                form_data.get("transaction_hour")
            ),
            "is_recurring": is_recurring,
            "start_date": TransactionService._parse_date(
                form_data.get("start_date")
            ),
            "end_date": TransactionService._parse_date(form_data.get("end_date")),
            "interval": form_data.get("interval") or None,
            "number_of_payments": (
                TransactionService._parse_int(
                    form_data.get("number_of_payments"),
                    default=2,
                )
                if is_recurring
                else None
            ),
            "transaction_type": TransactionService._required(
                form_data,
                "transaction_type",
            ),
        }
        if data["transaction_type"] not in {"income", "expense"}:
            raise ValidationError("Tipo de transacao invalido.")
        return data

    @staticmethod
    def _required(form_data, key: str) -> str:
        value = (form_data.get(key) or "").strip()
        if not value:
            raise ValidationError(f"Campo obrigatorio ausente: {key}.")
        return value

    @staticmethod
    def _parse_amount(value) -> Decimal:
        try:
            return Decimal(str(value).replace(",", "."))
        except (InvalidOperation, TypeError) as exc:
            raise ValidationError("Valor monetario invalido.") from exc

    @staticmethod
    def _parse_int(value, default: int | None = None) -> int | None:
        if value in (None, ""):
            return default
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise ValidationError("Numero de parcelas invalido.") from exc

    @staticmethod
    def _parse_date(value):
        if not value:
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValidationError("Data invalida.") from exc

    @staticmethod
    def _parse_time(value):
        if not value:
            return None
        try:
            return datetime.strptime(value, "%H:%M").time()
        except ValueError as exc:
            raise ValidationError("Hora invalida.") from exc
