from flask_mail import Message

from app.extensions import mail


class ContactService:
    @staticmethod
    def send_contact_message(
        name: str,
        email: str,
        phone: str,
        message: str,
    ) -> None:
        email_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;
                     color: #333;">
            <h2 style="color: #4CAF50;">Nova mensagem de contato</h2>
            <p><strong>Nome:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Telefone:</strong> {phone}</p>
            <p><strong>Mensagem:</strong></p>
            <p style="margin-left: 20px; font-style: italic;">"{message}"</p>
            <hr>
            <p style="font-size: 12px; color: #777;">
                Recebido via formulario do site MoneyWise
            </p>
        </body>
        </html>
        """

        mail.send(
            Message(
                subject="Nova mensagem de contato",
                recipients=["joaomarcos.jm@ges.inatel.br"],
                html=email_body,
            )
        )
