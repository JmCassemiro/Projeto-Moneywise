from urllib.parse import quote, unquote

from flask import url_for
from flask_mail import Message

from app.exceptions import NotFoundError, ValidationError
from app.extensions import mail
from app.users_authentication.repositories import UserRepository
from app.users_authentication.services.user_service import UserService
from app.users_authentication.utils.token import (
    confirm_reset_token,
    generate_reset_token,
)


class PasswordResetService:
    @staticmethod
    def send_reset_link(email: str) -> None:
        user = UserRepository.find_by_email(email)
        if not user:
            raise NotFoundError("E-mail nao cadastrado.")

        token = generate_reset_token(user.email)
        reset_url = url_for(
            "users.reset_password",
            token=quote(token),
            _external=True,
        )

        message = Message(
            subject="Recuperacao de senha - MoneyWise",
            recipients=[user.email],
            html=PasswordResetService._email_body(user.name, reset_url),
        )
        mail.send(message)

    @staticmethod
    def reset_password(token: str, new_password: str) -> None:
        email = confirm_reset_token(unquote(token))
        if not email:
            raise ValidationError("Link invalido ou expirado.")

        user = UserRepository.find_by_email(email)
        if not user:
            raise NotFoundError("Usuario nao encontrado.")

        UserService.reset_password(user, new_password)

    @staticmethod
    def _email_body(name: str, reset_url: str) -> str:
        return f"""
        <p>Ola, {name}!</p>
        <p>Para redefinir sua senha, clique no botao abaixo:</p>
        <p>
            <a href="{reset_url}"
               style="display: inline-block;
                      background-color: #efa23b;
                      color: #1f1f23;
                      text-decoration: none;
                      font-weight: bold;
                      padding: 12px 20px;
                      border-radius: 6px;
                      font-family: 'Segoe UI', Tahoma, sans-serif;
                      font-size: 16px;">
                Redefinir Senha
            </a>
        </p>
        <p>Se voce nao solicitou isso, ignore esta mensagem.</p>
        <p>Atenciosamente,<br>Equipe MoneyWise</p>
        """
