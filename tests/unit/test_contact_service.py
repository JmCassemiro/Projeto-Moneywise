from app.home.services import ContactService


def test_send_contact_message_sends_email(app, mocker):
    send = mocker.patch("app.home.services.mail.send")

    with app.app_context():
        ContactService.send_contact_message(
            name="Person",
            email="person@example.com",
            phone="123",
            message="Hello",
        )

    message = send.call_args.args[0]
    assert message.subject == "Nova mensagem de contato"
    assert message.recipients == [app.config["MAIL_CONTACT_RECIPIENT"]]
    assert "Person" in message.html
    assert "person@example.com" in message.html
    assert "Hello" in message.html
