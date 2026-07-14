from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import AuthenticationError, NotFoundError, ValidationError
from app.extensions import db
from app.users_authentication.models import User
from app.users_authentication.repositories import UserRepository


class UserService:
    @staticmethod
    def get_user(user_id: int | str) -> User:
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError("Usuario nao encontrado.")
        return user

    @staticmethod
    def create_user(
        name: str,
        email: str,
        password: str,
        birthday,
    ) -> User:
        if UserRepository.find_by_email(email):
            raise ValidationError("Email ja cadastrado.")
        if UserRepository.find_by_name(name):
            raise ValidationError("Usuario ja cadastrado.")

        user = User(
            email=email,
            name=name,
            password=password,
            birthday=birthday,
        )
        try:
            return UserRepository.add(user)
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise ValidationError("Erro ao criar conta. Tente novamente.") from exc

    @staticmethod
    def authenticate(email: str, password: str) -> User | None:
        user = UserRepository.find_by_email(email)
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def update_profile(user_id: int | str, data: dict) -> User:
        user = UserService.get_user(user_id)

        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip()
        birthday = UserService._parse_birthday(data.get("birthday"))

        if not name:
            raise ValidationError("Nome e obrigatorio.")
        if not email:
            raise ValidationError("Email e obrigatorio.")

        existing_user = UserRepository.find_by_email(email)
        if existing_user and existing_user.id != user.id:
            raise ValidationError("Email ja cadastrado.")

        user.name = name
        user.email = email
        if birthday:
            user.birthday = birthday

        try:
            db.session.commit()
            return user
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise ValidationError(
                "Erro ao atualizar perfil. Tente novamente."
            ) from exc

    @staticmethod
    def delete_account(user_id: int | str, password: str) -> None:
        user = UserService.get_user(user_id)
        if not user.check_password(password):
            raise AuthenticationError("Senha incorreta. Conta nao foi excluida.")

        try:
            UserRepository.delete(user)
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise ValidationError("Erro ao excluir conta.") from exc

    @staticmethod
    def reset_password(user: User, new_password: str) -> None:
        user.set_password(new_password)
        try:
            db.session.commit()
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise ValidationError("Erro ao redefinir senha.") from exc

    @staticmethod
    def _parse_birthday(value: str | None):
        if not value:
            return None

        for date_format in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(value, date_format).date()
            except ValueError:
                continue

        raise ValidationError("Formato de data invalido.")
