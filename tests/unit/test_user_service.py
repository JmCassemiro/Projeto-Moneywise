from datetime import date
from types import SimpleNamespace

import pytest

from app.exceptions import ValidationError
from app.users_authentication.services.user_service import UserService


def test_authenticate_returns_user_when_password_matches(mocker):
    user = SimpleNamespace(check_password=lambda password: password == "secret")
    mocker.patch(
        "app.users_authentication.services.user_service.UserRepository.find_by_email",
        return_value=user,
    )

    assert UserService.authenticate("person@example.com", "secret") is user


def test_authenticate_returns_none_when_user_missing_or_password_mismatch(mocker):
    find_by_email = mocker.patch(
        "app.users_authentication.services.user_service.UserRepository.find_by_email"
    )
    find_by_email.return_value = None
    assert UserService.authenticate("missing@example.com", "secret") is None

    find_by_email.return_value = SimpleNamespace(check_password=lambda password: False)
    assert UserService.authenticate("person@example.com", "wrong") is None


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("2026-05-14", date(2026, 5, 14)),
        ("14/05/2026", date(2026, 5, 14)),
        (None, None),
    ],
)
def test_parse_birthday_accepts_supported_formats(value, expected):
    assert UserService._parse_birthday(value) == expected


def test_parse_birthday_rejects_invalid_format():
    with pytest.raises(ValidationError, match="Formato de data invalido."):
        UserService._parse_birthday("05-14-2026")


def test_create_user_rejects_duplicate_email(mocker):
    mocker.patch(
        "app.users_authentication.services.user_service.UserRepository.find_by_email",
        return_value=object(),
    )

    with pytest.raises(ValidationError, match="Email ja cadastrado."):
        UserService.create_user(
            "Person", "person@example.com", "Password123!", date(1995, 1, 1)
        )


def test_create_user_rejects_duplicate_name(mocker):
    mocker.patch(
        "app.users_authentication.services.user_service.UserRepository.find_by_email",
        return_value=None,
    )
    mocker.patch(
        "app.users_authentication.services.user_service.UserRepository.find_by_name",
        return_value=object(),
    )

    with pytest.raises(ValidationError, match="Usuario ja cadastrado."):
        UserService.create_user(
            "Person", "person@example.com", "Password123!", date(1995, 1, 1)
        )
