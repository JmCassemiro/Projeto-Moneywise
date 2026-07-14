from types import SimpleNamespace

import pytest

from app.exceptions import NotFoundError, ValidationError
from app.users_authentication.services.password_reset_service import (
    PasswordResetService,
)


def test_send_reset_link_sends_email_with_generated_token(app, mocker):
    user = SimpleNamespace(email="person@example.com", name="Person")
    mocker.patch(
        "app.users_authentication.services.password_reset_service.UserRepository.find_by_email",
        return_value=user,
    )
    mocker.patch(
        "app.users_authentication.services.password_reset_service.generate_reset_token",
        return_value="token value",
    )
    send = mocker.patch(
        "app.users_authentication.services.password_reset_service.mail.send"
    )

    with app.test_request_context("/"):
        PasswordResetService.send_reset_link("person@example.com")

    message = send.call_args.args[0]
    assert message.subject == "Recuperacao de senha - MoneyWise"
    assert message.recipients == ["person@example.com"]
    assert "token%2520value" in message.html


def test_send_reset_link_rejects_unknown_email(mocker):
    mocker.patch(
        "app.users_authentication.services.password_reset_service.UserRepository.find_by_email",
        return_value=None,
    )

    with pytest.raises(NotFoundError, match="E-mail nao cadastrado."):
        PasswordResetService.send_reset_link("missing@example.com")


def test_reset_password_updates_user_for_valid_token(mocker):
    user = SimpleNamespace(email="person@example.com")
    mocker.patch(
        "app.users_authentication.services.password_reset_service.confirm_reset_token",
        return_value="person@example.com",
    )
    mocker.patch(
        "app.users_authentication.services.password_reset_service.UserRepository.find_by_email",
        return_value=user,
    )
    reset_password = mocker.patch(
        "app.users_authentication.services.password_reset_service.UserService.reset_password"
    )

    PasswordResetService.reset_password("token", "Password123!")

    reset_password.assert_called_once_with(user, "Password123!")


def test_reset_password_rejects_invalid_token(mocker):
    mocker.patch(
        "app.users_authentication.services.password_reset_service.confirm_reset_token",
        return_value=False,
    )

    with pytest.raises(ValidationError, match="Link invalido ou expirado."):
        PasswordResetService.reset_password("bad-token", "Password123!")
