from decimal import Decimal

from sqlalchemy import select

from app.extensions import db
from app.transactions.models import Transaction


class TransactionRepository:
    @staticmethod
    def list_for_user(filters: dict, user_id: int | str) -> list[Transaction]:
        statement = select(Transaction).where(Transaction.user_id == int(user_id))
        statement = TransactionRepository._apply_filters(statement, filters)
        statement = statement.order_by(
            Transaction.transaction_date.desc().nullslast(),
            Transaction.transaction_id.desc(),
        )
        return list(db.session.execute(statement).scalars())

    @staticmethod
    def get_for_user(
        transaction_id: int,
        user_id: int | str,
    ) -> Transaction | None:
        return db.session.execute(
            select(Transaction).where(
                Transaction.transaction_id == transaction_id,
                Transaction.user_id == int(user_id),
            )
        ).scalar_one_or_none()

    @staticmethod
    def create(transaction: Transaction) -> Transaction:
        db.session.add(transaction)
        db.session.commit()
        return transaction

    @staticmethod
    def save() -> None:
        db.session.commit()

    @staticmethod
    def delete(transaction: Transaction) -> None:
        db.session.delete(transaction)
        db.session.commit()

    @staticmethod
    def list_recent_for_user(user_id: int | str, start_date) -> list[Transaction]:
        return list(
            db.session.execute(
                select(Transaction)
                .where(
                    Transaction.user_id == int(user_id),
                    Transaction.transaction_date >= start_date,
                )
                .order_by(Transaction.transaction_date.asc())
            ).scalars()
        )

    @staticmethod
    def _apply_filters(statement, filters: dict):
        search = filters.get("search")
        if search:
            statement = statement.where(Transaction.title.ilike(f"%{search}%"))

        exact_filters = {
            "filter-type": Transaction.transaction_type,
            "filter-category": Transaction.category,
            "filter-payment-method": Transaction.payment_method,
        }
        for key, column in exact_filters.items():
            value = filters.get(key)
            if value:
                statement = statement.where(column == value)

        if filters.get("filter-start-date"):
            statement = statement.where(
                Transaction.transaction_date >= filters["filter-start-date"]
            )
        if filters.get("filter-end-date"):
            statement = statement.where(
                Transaction.transaction_date <= filters["filter-end-date"]
            )
        if filters.get("filter-min-amount"):
            statement = statement.where(
                Transaction.amount >= Decimal(filters["filter-min-amount"])
            )
        if filters.get("filter-max-amount"):
            statement = statement.where(
                Transaction.amount <= Decimal(filters["filter-max-amount"])
            )

        return statement
