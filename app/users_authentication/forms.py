from flask_wtf import FlaskForm
from wtforms import DateField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.users_authentication.repositories import UserRepository


SPECIAL_CHARACTERS = "!@#$%^&*()-_+=<>?/|{}[]:;'"


def validate_password_strength(password: str) -> None:
    if len(password) < 8:
        raise ValidationError("A senha deve ter pelo menos 8 caracteres.")
    if not any(character.isalpha() for character in password):
        raise ValidationError("A senha deve conter pelo menos uma letra.")
    if not any(character.isdigit() for character in password):
        raise ValidationError("A senha deve conter pelo menos um número.")
    if not any(character in SPECIAL_CHARACTERS for character in password):
        raise ValidationError(
            "A senha deve conter pelo menos um caractere especial."
        )


class UserSigninForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Senha:", validators=[DataRequired()])
    submit = SubmitField("Login")


class UserSignupForm(FlaskForm):
    username = StringField(
        "Usuário:",
        validators=[Length(min=3, max=30), DataRequired()],
    )
    email_address = StringField(
        "Email:",
        validators=[Email(), DataRequired()],
    )
    password = PasswordField("Senha:", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirmar Senha:",
        validators=[
            DataRequired(),
            EqualTo("password", message="As senhas não coincidem."),
        ],
    )
    birthday = DateField(
        "Aniversário:",
        format="%Y-%m-%d",
        validators=[DataRequired()],
    )
    submit = SubmitField("Criar Conta")

    def validate_username(self, field) -> None:
        if UserRepository.find_by_name(field.data):
            raise ValidationError("Usuário já cadastrado.")

    def validate_email_address(self, field) -> None:
        if UserRepository.find_by_email(field.data):
            raise ValidationError("Email já cadastrado.")

    def validate_password(self, field) -> None:
        validate_password_strength(field.data)


class UserDeleteForm(FlaskForm):
    password = PasswordField("Confirme sua senha:", validators=[DataRequired()])
    submit = SubmitField("Excluir Conta")


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Enviar link de recuperação")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        label="Senha:",
        validators=[
            DataRequired(),
            Length(min=8, message="A senha deve ter pelo menos 8 caracteres."),
        ],
    )
    confirm_password = PasswordField(
        label="Confirmar Senha:",
        validators=[
            DataRequired(),
            EqualTo("password", message="As senhas não coincidem."),
        ],
    )
    submit = SubmitField("Redefinir senha")

    def validate_password(self, field) -> None:
        validate_password_strength(field.data)
