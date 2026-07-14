from collections.abc import Callable
from datetime import date
from decimal import Decimal
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from flask_jwt_extended import create_access_token

from app import create_app
from app.extensions import db as _db
from app.extensions import mail
from app.transactions.models import Transaction
from app.users_authentication.models import User


def _assert_test_database(app) -> None:
    database_uri = app.config["SQLALCHEMY_DATABASE_URI"]
    database_name = database_uri.rsplit("/", 1)[-1].split("?", 1)[0]
    if "test" not in database_name.lower():
        raise RuntimeError(
            "Refusing to run integration tests outside a test database. "
            "Set TEST_DATABASE_URL to a database whose name contains 'test'."
        )


@pytest.fixture(scope="session")
def app():
    flask_app = create_app("testing")
    flask_app.config.update(
        SERVER_NAME="localhost.localdomain",
        TESTING=True,
        WTF_CSRF_ENABLED=False,
    )

    yield flask_app


@pytest.fixture
def database(app):
    with app.app_context():
        _assert_test_database(app)
        _db.session.remove()
        _db.drop_all()
        _db.create_all()

    yield _db

    with app.app_context():
        _db.session.rollback()
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def create_user(app, database) -> Callable[..., User]:
    def factory(
        *,
        name: str = "Test User",
        email: str = "test@example.com",
        password: str = "Password123!",
        birthday: date = date(1995, 5, 14),
        avatar: str | None = None,
    ) -> User:
        user = User(
            name=name,
            email=email,
            password=password,
            birthday=birthday,
            avatar=avatar,
        )
        with app.app_context():
            database.session.add(user)
            database.session.commit()
            database.session.refresh(user)
        return user

    return factory


@pytest.fixture
def create_transaction(app, database, create_user) -> Callable[..., Transaction]:
    def factory(
        *,
        user: User | None = None,
        title: str = "Groceries",
        amount: Decimal | str = Decimal("25.90"),
        category: str = "Mercado",
        payment_method: str = "Credit Card",
        description: str = "",
        transaction_date: date = date(2026, 5, 14),
        transaction_hour=None,
        is_recurring: bool = False,
        start_date=None,
        end_date=None,
        interval: str | None = None,
        number_of_payments: int | None = None,
        transaction_type: str = "expense",
    ) -> Transaction:
        owner = user or create_user()
        transaction = Transaction(
            user_id=owner.id,
            title=title,
            amount=Decimal(str(amount)),
            category=category,
            payment_method=payment_method,
            description=description,
            transaction_date=transaction_date,
            transaction_hour=transaction_hour,
            is_recurring=is_recurring,
            start_date=start_date,
            end_date=end_date,
            interval=interval,
            number_of_payments=number_of_payments,
            transaction_type=transaction_type,
        )
        with app.app_context():
            database.session.add(transaction)
            database.session.commit()
            database.session.refresh(transaction)
        return transaction

    return factory


@pytest.fixture
def authenticated_client(app, client, create_user):
    def factory(user: User | None = None, **user_kwargs):
        auth_user = user or create_user(**user_kwargs)
        with app.app_context():
            token = create_access_token(identity=str(auth_user.id))
        client.set_cookie(
            app.config["JWT_ACCESS_COOKIE_NAME"],
            token,
            domain="localhost.localdomain",
        )
        return client, auth_user

    return factory


@pytest.fixture
def mail_mock(mocker):
    return mocker.patch.object(mail, "send")
