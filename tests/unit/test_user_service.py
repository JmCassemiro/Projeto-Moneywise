from datetime import date
from types import SimpleNamespace

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import AuthenticationError, NotFoundError, ValidationError
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


def test_get_user_returns_user_or_raises_not_found(mocker):
    user = SimpleNamespace(id=1)
    get_by_id = mocker.patch(
        "app.users_authentication.services.user_service.UserRepository.get_by_id",
        return_value=user,
    )

    assert UserService.get_user(1) is user

    get_by_id.return_value = None
    with pytest.raises(NotFoundError, match="Usuario nao encontrado."):
        UserService.get_user(999)


def test_create_user_adds_new_user(mocker):
    mocker.patch(
        "app.users_authentication.services.user_service.UserRepository.find_by_email",
        return_value=None,
    )
    mocker.patch(
        "app.users_authentication.services.user_service.UserRepository.find_by_name",
        return_value=None,
    )
    add = mocker.patch(
        "app.users_authentication.services.user_service.UserRepository.add",
        side_effect=lambda user: user,
    )

    user = UserService.create_user(
        "Person",
        "person@example.com",
        "Password123!",
        date(1995, 1, 1),
    )

    assert add.call_count == 1
    assert user.name == "Person"
    assert user.email == "person@example.com"
    assert user.birthday == date(1995, 1, 1)
    assert user.check_password("Password123!")


def test_create_user_rolls_back_repository_error(mocker):
    mocker.patch(
        "app.users_authentication.services.user_service.UserRepository.find_by_email",
        return_value=None,
    )
    mocker.patch(
        "app.users_authentication.services.user_service.UserRepository.find_by_name",
        return_value=None,
    )
    mocker.patch(
        "app.users_authentication.services.user_service.UserRepository.add",
        side_effect=SQLAlchemyError("insert failed"),
    )
    rollback = mocker.patch(
        "app.users_authentication.services.user_service.db.session.rollback"
    )

    with pytest.raises(ValidationError, match="Erro ao criar conta."):
        UserService.create_user(
            "Person", "person@example.com", "Password123!", date(1995, 1, 1)
        )

    rollback.assert_called_once()


def test_update_profile_validates_required_and_duplicate_fields(mocker):
    user = SimpleNamespace(id=1, name="Old", email="old@example.com", birthday=None)
    mocker.patch.object(UserService, "get_user", return_value=user)

    with pytest.raises(ValidationError, match="Nome e obrigatorio."):
        UserService.update_profile(1, {"name": "", "email": "new@example.com"})

    with pytest.raises(ValidationError, match="Email e obrigatorio."):
        UserService.update_profile(1, {"name": "New", "email": ""})

    mocker.patch(
        "app.users_authentication.services.user_service.UserRepository.find_by_email",
        return_value=SimpleNamespace(id=2),
    )
    with pytest.raises(ValidationError, match="Email ja cadastrado."):
        UserService.update_profile(
            1,
            {"name": "New", "email": "other@example.com"},
        )


def test_update_profile_updates_and_commits(mocker):
    user = SimpleNamespace(
        id=1,
        name="Old",
        email="old@example.com",
        birthday=date(1990, 1, 1),
    )
    mocker.patch.object(UserService, "get_user", return_value=user)
    mocker.patch(
        "app.users_authentication.services.user_service.UserRepository.find_by_email",
        return_value=SimpleNamespace(id=1),
    )
    commit = mocker.patch(
        "app.users_authentication.services.user_service.db.session.commit"
    )

    result = UserService.update_profile(
        1,
        {
            "name": " New Name ",
            "email": "new@example.com",
            "birthday": "2026-05-14",
        },
    )

    assert result is user
    assert user.name == "New Name"
    assert user.email == "new@example.com"
    assert user.birthday == date(2026, 5, 14)
    commit.assert_called_once()


def test_delete_account_validates_password_and_deletes(mocker):
    user = SimpleNamespace(check_password=lambda password: password == "secret")
    mocker.patch.object(UserService, "get_user", return_value=user)
    delete = mocker.patch(
        "app.users_authentication.services.user_service.UserRepository.delete"
    )

    with pytest.raises(AuthenticationError, match="Senha incorreta."):
        UserService.delete_account(1, "wrong")

    UserService.delete_account(1, "secret")

    delete.assert_called_once_with(user)


def test_reset_password_sets_hash_and_rolls_back_on_error(mocker):
    user = SimpleNamespace(set_password=mocker.Mock())
    mocker.patch(
        "app.users_authentication.services.user_service.db.session.commit",
        side_effect=SQLAlchemyError("commit failed"),
    )
    rollback = mocker.patch(
        "app.users_authentication.services.user_service.db.session.rollback"
    )

    with pytest.raises(ValidationError, match="Erro ao redefinir senha."):
        UserService.reset_password(user, "NewPassword123!")

    user.set_password.assert_called_once_with("NewPassword123!")
    rollback.assert_called_once()
