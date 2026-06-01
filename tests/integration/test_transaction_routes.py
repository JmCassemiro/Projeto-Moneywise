from datetime import date

from app.extensions import db
from app.transactions.models import Transaction


def _transaction_count(app) -> int:
    with app.app_context():
        return db.session.query(Transaction).count()


def test_transactions_page_redirects_when_unauthenticated(database, client):
    response = client.get("/transactions/", follow_redirects=False)

    assert response.status_code == 302
    assert "/signin" in response.headers["Location"]


def test_statistics_page_redirects_when_unauthenticated(database, client):
    response = client.get("/statistics/", follow_redirects=False)

    assert response.status_code == 302
    assert "/signin" in response.headers["Location"]


def test_transactions_page_shows_only_authenticated_user_data(
    database,
    authenticated_client,
    create_user,
    create_transaction,
):
    client, user = authenticated_client(
        name="Owner",
        email="owner@example.com",
    )
    create_transaction(user=user, title="Owner Salary", transaction_type="income")

    other_user = create_user(name="Other", email="other@example.com")
    create_transaction(
        user=other_user, title="Other Expense", transaction_type="expense"
    )

    response = client.get("/transactions/")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Owner Salary" in page
    assert "Other Expense" not in page


def test_create_transaction_persists_and_redirects(database, app, authenticated_client):
    client, _user = authenticated_client()

    response = client.post(
        "/transactions/create",
        data={
            "title": "Gym",
            "amount": "89.90",
            "category": "Saúde",
            "payment_method": "PIX",
            "description": "Monthly membership",
            "transaction_date": "2026-05-14",
            "transaction_hour": "08:00",
            "transaction_type": "expense",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/transactions/")
    assert _transaction_count(app) == 1


def test_create_transaction_invalid_amount_does_not_persist(
    database,
    app,
    authenticated_client,
):
    client, _user = authenticated_client()

    response = client.post(
        "/transactions/create",
        data={
            "title": "Gym",
            "amount": "invalid",
            "category": "Saúde",
            "payment_method": "PIX",
            "description": "Monthly membership",
            "transaction_date": "2026-05-14",
            "transaction_hour": "08:00",
            "transaction_type": "expense",
        },
        follow_redirects=False,
    )

    assert response.status_code == 200
    assert _transaction_count(app) == 0


def test_edit_transaction_updates_persisted_values(
    database,
    app,
    authenticated_client,
    create_transaction,
):
    client, user = authenticated_client()
    transaction = create_transaction(user=user, title="Old Title", amount="100")

    response = client.post(
        f"/transactions/edit/{transaction.transaction_id}",
        data={
            "title": "Updated Title",
            "amount": "150.50",
            "category": "Casa",
            "payment_method": "Credito",
            "description": "Updated description",
            "transaction_date": "2026-06-01",
            "transaction_hour": "10:30",
            "transaction_type": "expense",
        },
        follow_redirects=False,
    )

    with app.app_context():
        updated = db.session.get(Transaction, transaction.transaction_id)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/transactions/")
    assert updated.title == "Updated Title"
    assert str(updated.amount) == "150.50"
    assert updated.category == "Casa"


def test_edit_missing_transaction_returns_not_found_json(
    database,
    authenticated_client,
):
    client, _user = authenticated_client()

    response = client.post(
        "/transactions/edit/99999",
        data={
            "title": "Anything",
            "amount": "10",
            "category": "Casa",
            "payment_method": "PIX",
            "transaction_type": "expense",
        },
        headers={"Accept": "application/json"},
        follow_redirects=False,
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Transacao nao encontrada."}


def test_delete_transaction_removes_record(
    database,
    app,
    authenticated_client,
    create_transaction,
):
    client, user = authenticated_client()
    transaction = create_transaction(user=user, title="To Delete")

    response = client.post(
        f"/transactions/delete/{transaction.transaction_id}",
        follow_redirects=False,
    )

    with app.app_context():
        deleted = db.session.get(Transaction, transaction.transaction_id)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/transactions/")
    assert deleted is None


def test_delete_other_user_transaction_does_not_remove_record(
    database,
    app,
    authenticated_client,
    create_user,
    create_transaction,
):
    client, _user = authenticated_client(
        name="Owner",
        email="owner@example.com",
    )
    other_user = create_user(name="Other", email="other@example.com")
    transaction = create_transaction(user=other_user, title="Other Tx")

    response = client.post(
        f"/transactions/delete/{transaction.transaction_id}",
        follow_redirects=False,
    )

    with app.app_context():
        existing = db.session.get(Transaction, transaction.transaction_id)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/transactions/")
    assert existing is not None


def test_transactions_filter_by_category(
    database, authenticated_client, create_transaction
):
    client, user = authenticated_client()
    create_transaction(
        user=user,
        title="House Expense",
        category="Casa",
        amount="120",
        transaction_date=date(2026, 5, 1),
    )
    create_transaction(
        user=user,
        title="Market Expense",
        category="Mercado",
        amount="45",
        transaction_date=date(2026, 5, 2),
    )

    response = client.get("/transactions/?filter-category=Casa")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "House Expense" in page
    assert "Market Expense" not in page
