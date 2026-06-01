from app.extensions import db
from app.users_authentication.models import User


def _get_user_by_email(app, email):
    with app.app_context():
        return db.session.query(User).filter_by(email=email).one_or_none()


def test_signup_page_loads(database, client):
    response = client.get("/signup")

    assert response.status_code == 200


def test_signup_creates_user_and_redirects(database, app, client):
    response = client.post(
        "/signup",
        data={
            "username": "newuser",
            "email_address": "newuser@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
            "birthday": "1995-05-14",
        },
        follow_redirects=False,
    )

    created = _get_user_by_email(app, "newuser@example.com")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/signin")
    assert created is not None


def test_signup_duplicate_email_does_not_create_second_user(
    database,
    app,
    client,
    create_user,
):
    create_user(name="existing", email="dup@example.com")

    response = client.post(
        "/signup",
        data={
            "username": "another",
            "email_address": "dup@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
            "birthday": "1994-05-14",
        },
        follow_redirects=False,
    )

    with app.app_context():
        count = db.session.query(User).filter_by(email="dup@example.com").count()

    assert response.status_code == 200
    assert count == 1


def test_signin_sets_access_cookie_and_redirects(database, client, create_user):
    create_user(email="signin@example.com", password="Password123!")

    response = client.post(
        "/signin",
        data={"email": "signin@example.com", "password": "Password123!"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/transactions/")
    assert "access_token_cookie=" in response.headers.get("Set-Cookie", "")


def test_signin_invalid_credentials_returns_200(database, client):
    response = client.post(
        "/signin",
        data={"email": "missing@example.com", "password": "bad-pass"},
        follow_redirects=False,
    )

    assert response.status_code == 200


def test_logout_redirects_and_unsets_cookie(database, authenticated_client):
    client, _user = authenticated_client()

    response = client.get("/logout", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/signin")
    assert "access_token_cookie=;" in response.headers.get("Set-Cookie", "")


def test_profile_requires_authentication(database, client):
    response = client.get("/profile", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/signin")


def test_profile_update_returns_success_json(database, authenticated_client):
    client, _user = authenticated_client(email="before@example.com")

    response = client.post(
        "/profile/update",
        json={
            "name": "updated name",
            "email": "after@example.com",
            "birthday": "1990-01-01",
        },
        follow_redirects=False,
    )
    body = response.get_json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["user"]["email"] == "after@example.com"
    assert body["user"]["name"] == "updated name"


def test_delete_account_with_wrong_password_keeps_user(
    database,
    app,
    authenticated_client,
):
    client, user = authenticated_client(email="keep@example.com")

    response = client.post(
        "/delete_account",
        data={"password": "wrong"},
        follow_redirects=False,
    )

    with app.app_context():
        existing = db.session.get(User, user.id)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/profile")
    assert existing is not None


def test_delete_account_with_correct_password_removes_user(
    database,
    app,
    authenticated_client,
):
    client, user = authenticated_client(email="remove@example.com")

    response = client.post(
        "/delete_account",
        data={"password": "Password123!"},
        follow_redirects=False,
    )

    with app.app_context():
        removed = db.session.get(User, user.id)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/signin")
    assert removed is None


def test_forgot_password_route_calls_service_and_redirects(
    database,
    client,
    mocker,
):
    send_reset_link = mocker.patch(
        "app.users_authentication.routes.PasswordResetService.send_reset_link"
    )

    response = client.post(
        "/forgot-password",
        data={"email": "person@example.com"},
        follow_redirects=False,
    )

    send_reset_link.assert_called_once_with("person@example.com")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/signin")


def test_forgot_password_mail_failure_returns_page_instead_of_500(
    database,
    client,
    create_user,
    mocker,
):
    create_user(name="Reset User", email="reset@example.com")
    mocker.patch(
        "app.users_authentication.services.password_reset_service.mail.send",
        side_effect=ConnectionRefusedError("smtp offline"),
    )

    response = client.post(
        "/forgot-password",
        data={"email": "reset@example.com"},
        follow_redirects=False,
    )
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Erro ao enviar" in page


def test_reset_password_route_calls_service_and_redirects(database, client, mocker):
    reset_password = mocker.patch(
        "app.users_authentication.routes.PasswordResetService.reset_password"
    )

    response = client.post(
        "/reset-password/test-token",
        data={
            "password": "Password123!",
            "confirm_password": "Password123!",
        },
        follow_redirects=False,
    )

    reset_password.assert_called_once_with("test-token", "Password123!")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/signin")


def test_token_expires_returns_remaining_time(database, authenticated_client):
    client, _user = authenticated_client()

    response = client.get("/token/expires")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["time_remaining_seconds"] >= 0
    assert "time_remaining_human" in payload
