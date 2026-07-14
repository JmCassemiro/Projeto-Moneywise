import os
from datetime import timedelta

try:
    from dotenv import load_dotenv
except ImportError:
    pass
else:
    load_dotenv()


def _env(name: str, *, allow_blank: bool = False) -> str:
    value = os.environ.get(name)
    if value is None or (not allow_blank and value == ""):
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _env_bool(name: str) -> bool:
    return _env(name).strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str) -> int:
    return int(_env(name))


def _env_list(name: str) -> list[str]:
    return [item.strip() for item in _env(name).split(",") if item.strip()]


def _database_uri() -> str:
    uri = os.environ.get("DATABASE_URL")
    if uri:
        return uri.replace("postgres://", "postgresql://", 1)

    host = _env("DB_HOST")
    port = _env("DB_PORT")
    name = _env("DB_NAME")
    user = _env("DB_USER")
    password = _env("DB_PASSWORD")
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


class Config:
    SECRET_KEY = _env("SECRET_KEY")
    SECURITY_PASSWORD_SALT = _env("SECURITY_PASSWORD_SALT")

    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = _env_bool("SQLALCHEMY_TRACK_MODIFICATIONS")

    MAIL_SERVER = _env("MAIL_SERVER")
    MAIL_PORT = _env_int("MAIL_PORT")
    MAIL_USE_TLS = _env_bool("MAIL_USE_TLS")
    MAIL_USE_SSL = _env_bool("MAIL_USE_SSL")
    MAIL_USERNAME = _env("MAIL_USERNAME", allow_blank=True) or None
    MAIL_PASSWORD = _env("MAIL_PASSWORD", allow_blank=True) or None
    MAIL_DEFAULT_SENDER = _env("MAIL_DEFAULT_SENDER")
    MAIL_CONTACT_RECIPIENT = _env("MAIL_CONTACT_RECIPIENT")

    JWT_SECRET_KEY = _env("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = _env_list("JWT_TOKEN_LOCATION")
    JWT_COOKIE_SECURE = _env_bool("JWT_COOKIE_SECURE")
    JWT_COOKIE_SAMESITE = _env("JWT_COOKIE_SAMESITE")
    JWT_COOKIE_CSRF_PROTECT = _env_bool("JWT_COOKIE_CSRF_PROTECT")
    JWT_COOKIE_NAME = _env("JWT_COOKIE_NAME")
    JWT_ACCESS_COOKIE_PATH = _env("JWT_ACCESS_COOKIE_PATH")
    JWT_REFRESH_COOKIE_PATH = _env("JWT_REFRESH_COOKIE_PATH")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=_env_int("JWT_ACCESS_TOKEN_MINUTES"))


class DevelopmentConfig(Config):
    DEBUG = _env_bool("DEBUG")


class TestingConfig(Config):
    TESTING = _env_bool("TESTING")
    WTF_CSRF_ENABLED = _env_bool("WTF_CSRF_ENABLED")
    SQLALCHEMY_DATABASE_URI = _env("TEST_DATABASE_URL")


class ProductionConfig(Config):
    DEBUG = _env_bool("DEBUG")
    JWT_COOKIE_SECURE = _env_bool("JWT_COOKIE_SECURE")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
