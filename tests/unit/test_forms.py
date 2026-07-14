import pytest
from wtforms.validators import ValidationError

from app.users_authentication.forms import ResetPasswordForm, UserSignupForm
from app.users_authentication.forms import validate_password_strength


@pytest.mark.parametrize(
    ("password", "message"),
    [
        ("Short1!", "A senha deve ter pelo menos 8 caracteres."),
        ("12345678!", "A senha deve conter pelo menos uma letra."),
        ("Password!", "A senha deve conter pelo menos um número."),
        ("Password1", "A senha deve conter pelo menos um caractere especial."),
    ],
)
def test_validate_password_strength_rejects_weak_passwords(password, message):
    with pytest.raises(ValidationError, match=message):
        validate_password_strength(password)


def test_validate_password_strength_accepts_strong_password():
    validate_password_strength("Password123!")


def test_signup_form_validates_unique_user_and_strong_password(app, mocker):
    mocker.patch(
        "app.users_authentication.forms.UserRepository.find_by_name",
        return_value=None,
    )
    mocker.patch(
        "app.users_authentication.forms.UserRepository.find_by_email",
        return_value=None,
    )

    with app.test_request_context(
        "/signup",
        method="POST",
        data={
            "username": "person",
            "email_address": "person@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
            "birthday": "1995-05-14",
        },
    ):
        form = UserSignupForm()

        assert form.validate() is True


def test_reset_password_form_rejects_mismatched_confirmation(app):
    with app.test_request_context(
        "/reset-password/token",
        method="POST",
        data={
            "password": "Password123!",
            "confirm_password": "Different123!",
        },
    ):
        form = ResetPasswordForm()

        assert form.validate() is False
        assert "As senhas não coincidem." in form.confirm_password.errors
