from collections import defaultdict
from datetime import date, timedelta

from app.transactions.repositories import TransactionRepository


class StatisticsService:
    @staticmethod
    def dashboard(user_id: int | str, days: int = 180) -> dict:
        start_date = date.today() - timedelta(days=days)
        transactions = TransactionRepository.list_recent_for_user(
            user_id,
            start_date,
        )

        income = [
            transaction
            for transaction in transactions
            if transaction.transaction_type == "income"
        ]
        expenses = [
            transaction
            for transaction in transactions
            if transaction.transaction_type == "expense"
        ]

        monthly = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
        for transaction in transactions:
            if not transaction.transaction_date:
                continue
            month_key = transaction.transaction_date.strftime("%Y-%m")
            monthly[month_key][transaction.transaction_type] += float(
                transaction.amount
            )

        months = sorted(monthly.keys())
        monthly_income = [monthly[month]["income"] for month in months]
        monthly_expenses = [monthly[month]["expense"] for month in months]
        monthly_balance = [
            income_value - expense_value
            for income_value, expense_value in zip(monthly_income, monthly_expenses)
        ]

        return {
            "receitas": sum(float(transaction.amount) for transaction in income),
            "despesas": sum(float(transaction.amount) for transaction in expenses),
            "total": (
                sum(float(transaction.amount) for transaction in income)
                - sum(float(transaction.amount) for transaction in expenses)
            ),
            "receitas_por_categoria": StatisticsService._sum_by_category(income),
            "despesas_por_categoria": StatisticsService._sum_by_category(
                expenses
            ),
            "meses": months,
            "receitas_mensais": monthly_income,
            "despesas_mensais": monthly_expenses,
            "saldos_mensais": monthly_balance,
            "top5Despesas": [
                (
                    transaction.title,
                    float(transaction.amount),
                    transaction.category,
                )
                for transaction in sorted(
                    expenses,
                    key=lambda item: item.amount,
                    reverse=True,
                )[:5]
            ],
        }

    @staticmethod
    def _sum_by_category(transactions) -> list[tuple[str, float]]:
        totals = defaultdict(float)
        for transaction in transactions:
            totals[transaction.category] += float(transaction.amount)
        return sorted(totals.items())
