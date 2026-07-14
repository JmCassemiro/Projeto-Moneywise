from datetime import date, time
from decimal import Decimal
from types import SimpleNamespace

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import NotFoundError, ValidationError
from app.transactions.services import TransactionService


class FormData(dict):
    def get(self, key, default=None):
        return super().get(key, default)


def _valid_form(**overrides):
    data = FormData(
        {
            "title": "Salary",
            "amount": "1200,50",
            "category": "Work",
            "payment_method": "PIX",
            "description": " Monthly salary ",
            "transaction_date": "2026-05-14",
            "transaction_hour": "08:30",
            "transaction_type": "income",
        }
    )
    data.update(overrides)
    return data


def test_build_filters_parses_dates_and_amounts():
    filters = TransactionService.build_filters(
        FormData(
            {
                "search": "rent",
                "filter-start-date": "2026-05-01",
                "filter-end-date": "2026-05-31",
                "filter-min-amount": "10,50",
                "filter-max-amount": "99.90",
            }
        )
    )

    assert filters["search"] == "rent"
    assert filters["filter-start-date"] == date(2026, 5, 1)
    assert filters["filter-end-date"] == date(2026, 5, 31)
    assert filters["filter-min-amount"] == Decimal("10.50")
    assert filters["filter-max-amount"] == Decimal("99.90")


def test_clean_form_data_handles_recurring_transaction_defaults():
    data = TransactionService._clean_form_data(
        _valid_form(
            is_recurring="on",
            start_date="2026-05-01",
            end_date="2026-06-01",
            interval="monthly",
            number_of_payments="",
        )
    )

    assert data["amount"] == Decimal("1200.50")
    assert data["description"] == "Monthly salary"
    assert data["transaction_date"] == date(2026, 5, 14)
    assert data["transaction_hour"] == time(8, 30)
    assert data["is_recurring"] is True
    assert data["start_date"] == date(2026, 5, 1)
    assert data["end_date"] == date(2026, 6, 1)
    assert data["interval"] == "monthly"
    assert data["number_of_payments"] == 2


def test_clean_form_data_rejects_invalid_values():
    with pytest.raises(ValidationError, match="Tipo de transacao invalido."):
        TransactionService._clean_form_data(_valid_form(transaction_type="transfer"))

    with pytest.raises(ValidationError, match="Campo obrigatorio ausente: title."):
        TransactionService._clean_form_data(_valid_form(title=""))

    with pytest.raises(ValidationError, match="Valor monetario invalido."):
        TransactionService._parse_amount("not-money")

    with pytest.raises(ValidationError, match="Numero de parcelas invalido."):
        TransactionService._parse_int("many")

    with pytest.raises(ValidationError, match="Data invalida."):
        TransactionService._parse_date("14/05/2026")

    with pytest.raises(ValidationError, match="Hora invalida."):
        TransactionService._parse_time("8h30")


def test_list_and_get_transactions_use_repository(mocker):
    transaction = SimpleNamespace(to_dict=lambda: {"transaction_id": 1})
    mocker.patch(
        "app.transactions.services.TransactionRepository.list_for_user",
        return_value=[transaction],
    )
    mocker.patch(
        "app.transactions.services.TransactionRepository.get_for_user",
        return_value=transaction,
    )

    assert TransactionService.list_transactions({}, 7) == [{"transaction_id": 1}]
    assert TransactionService.get_transaction(1, 7) == {"transaction_id": 1}


def test_get_update_and_delete_raise_when_transaction_is_missing(mocker):
    mocker.patch(
        "app.transactions.services.TransactionRepository.get_for_user",
        return_value=None,
    )

    with pytest.raises(NotFoundError, match="Transacao nao encontrada."):
        TransactionService.get_transaction(999, 1)

    with pytest.raises(NotFoundError, match="Transacao nao encontrada."):
        TransactionService.update_transaction(999, _valid_form(), 1)

    with pytest.raises(NotFoundError, match="Transacao nao encontrada."):
        TransactionService.delete_transaction(999, 1)


def test_repository_errors_are_reported_as_validation_errors(mocker):
    transaction = SimpleNamespace()
    rollback = mocker.patch("app.transactions.services.db.session.rollback")

    mocker.patch(
        "app.transactions.services.TransactionRepository.create",
        side_effect=SQLAlchemyError("create failed"),
    )
    with pytest.raises(ValidationError, match="Erro ao criar transacao."):
        TransactionService.create_transaction(_valid_form(), 1)

    mocker.patch(
        "app.transactions.services.TransactionRepository.get_for_user",
        return_value=transaction,
    )
    mocker.patch(
        "app.transactions.services.TransactionRepository.save",
        side_effect=SQLAlchemyError("save failed"),
    )
    with pytest.raises(ValidationError, match="Erro ao atualizar transacao."):
        TransactionService.update_transaction(1, _valid_form(), 1)

    mocker.patch(
        "app.transactions.services.TransactionRepository.delete",
        side_effect=SQLAlchemyError("delete failed"),
    )
    with pytest.raises(ValidationError, match="Erro ao deletar transacao."):
        TransactionService.delete_transaction(1, 1)

    assert rollback.call_count == 3
