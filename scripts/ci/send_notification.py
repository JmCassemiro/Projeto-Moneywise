import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path


def _env(name: str, fallback: str | None = None) -> str:
    value = os.environ.get(name)
    if value is None or value.strip() == "":
        return fallback or ""
    return value.strip()


def _env_bool(name: str, fallback: str = "false") -> bool:
    return _env(name, fallback).lower() in {"1", "true", "yes", "on"}


def _read_text(path_name: str) -> str:
    path = _env(path_name)
    if not path:
        return ""
    return Path(path).read_text(encoding="utf-8").strip()


def main() -> int:
    recipients = _env("NOTIFICATION_EMAIL", _env("MAIL_CONTACT_RECIPIENT"))
    sender = _env("NOTIFICATION_FROM", _env("MAIL_DEFAULT_SENDER"))
    host = _env("SMTP_HOST", _env("MAIL_SERVER"))
    port = int(_env("SMTP_PORT", _env("MAIL_PORT", "25")))
    username = _env("SMTP_USERNAME", _env("MAIL_USERNAME"))
    password = _env("SMTP_PASSWORD", _env("MAIL_PASSWORD"))
    use_tls = _env_bool("SMTP_USE_TLS", _env("MAIL_USE_TLS", "false"))
    use_ssl = _env_bool("SMTP_USE_SSL", _env("MAIL_USE_SSL", "false"))

    missing = [
        name
        for name, value in {
            "NOTIFICATION_EMAIL or MAIL_CONTACT_RECIPIENT": recipients,
            "NOTIFICATION_FROM or MAIL_DEFAULT_SENDER": sender,
            "SMTP_HOST or MAIL_SERVER": host,
        }.items()
        if not value
    ]
    if missing:
        print("Email notification skipped. Missing: " + ", ".join(missing))
        return 0

    message = EmailMessage()
    message["Subject"] = _read_text("NOTIFICATION_SUBJECT_FILE") or _env(
        "NOTIFICATION_SUBJECT"
    )
    message["From"] = sender
    message["To"] = recipients
    message.set_content(
        _read_text("NOTIFICATION_BODY_FILE") or _env("NOTIFICATION_BODY")
    )

    try:
        context = ssl.create_default_context()
        if use_ssl:
            with smtplib.SMTP_SSL(host, port, context=context, timeout=30) as smtp:
                if username or password:
                    smtp.login(username, password)
                smtp.send_message(message)
        else:
            with smtplib.SMTP(host, port, timeout=30) as smtp:
                if use_tls:
                    smtp.starttls(context=context)
                if username or password:
                    smtp.login(username, password)
                smtp.send_message(message)
    except (OSError, smtplib.SMTPException) as error:
        print(f"Email notification could not be sent: {error}")
        return 0

    print("Email notification sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
