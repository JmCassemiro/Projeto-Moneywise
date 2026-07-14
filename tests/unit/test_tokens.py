from app.users_authentication.utils.token import confirm_reset_token
from app.users_authentication.utils.token import generate_reset_token


def test_generate_and_confirm_reset_token(app):
    with app.app_context():
        token = generate_reset_token("person@example.com")

        assert confirm_reset_token(token) == "person@example.com"


def test_confirm_reset_token_returns_false_for_invalid_token(app):
    with app.app_context():
        assert confirm_reset_token("invalid-token") is False
