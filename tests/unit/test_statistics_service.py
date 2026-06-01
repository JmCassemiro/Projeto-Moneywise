from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from app.statistics.services import StatisticsService


def _transaction(title, amount, category, transaction_type, transaction_date):
    return SimpleNamespace(
        title=title,
        amount=Decimal(str(amount)),
        category=category,
        transaction_type=transaction_type,
        transaction_date=transaction_date,
    )


def test_dashboard_returns_empty_totals_without_history(mocker):
    mocker.patch(
        "app.statistics.services.TransactionRepository.list_recent_for_user",
        return_value=[],
    )

    dashboard = StatisticsService.dashboard(user_id=1)

    assert dashboard["receitas"] == 0
    assert dashboard["despesas"] == 0
    assert dashboard["total"] == 0
    assert dashboard["meses"] == []
    assert dashboard["top5Despesas"] == []


def test_dashboard_calculates_monthly_totals_categories_balance_and_top_expenses(
    mocker,
):
    transactions = [
        _transaction("Salary", "5000", "Work", "income", date(2026, 4, 30)),
        _transaction("Bonus", "1000", "Work", "income", date(2026, 5, 1)),
        _transaction("Rent", "1500", "Casa", "expense", date(2026, 5, 2)),
        _transaction("Market", "700", "Mercado", "expense", date(2026, 5, 3)),
        _transaction("Trip", "900", "Viagem", "expense", date(2026, 4, 20)),
        _transaction("Books", "120", "Estudos", "expense", date(2026, 5, 4)),
        _transaction("Cinema", "80", "Entretenimento", "expense", date(2026, 5, 5)),
        _transaction("Coffee", "20", "Mercado", "expense", date(2026, 5, 6)),
    ]
    mocker.patch(
        "app.statistics.services.TransactionRepository.list_recent_for_user",
        return_value=transactions,
    )

    dashboard = StatisticsService.dashboard(user_id=1)

    assert dashboard["receitas"] == 6000.0
    assert dashboard["despesas"] == 3320.0
    assert dashboard["total"] == 2680.0
    assert dashboard["meses"] == ["2026-04", "2026-05"]
    assert dashboard["receitas_mensais"] == [5000.0, 1000.0]
    assert dashboard["despesas_mensais"] == [900.0, 2420.0]
    assert dashboard["saldos_mensais"] == [4100.0, -1420.0]
    assert dashboard["receitas_por_categoria"] == [("Work", 6000.0)]
    assert dashboard["despesas_por_categoria"] == [
        ("Casa", 1500.0),
        ("Entretenimento", 80.0),
        ("Estudos", 120.0),
        ("Mercado", 720.0),
        ("Viagem", 900.0),
    ]
    assert dashboard["top5Despesas"] == [
        ("Rent", 1500.0, "Casa"),
        ("Trip", 900.0, "Viagem"),
        ("Market", 700.0, "Mercado"),
        ("Books", 120.0, "Estudos"),
        ("Cinema", 80.0, "Entretenimento"),
    ]
