import os

from flask import Flask

from app.errors import register_error_handlers
from app.extensions import bcrypt, csrf, db, jwt, login_manager, mail, migrate
from config import config


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    selected_config = config_name or os.environ.get("FLASK_CONFIG", "default")
    app.config.from_object(config.get(selected_config, config["default"]))

    register_extensions(app)
    register_models()
    register_blueprints(app)
    register_error_handlers(app)

    return app


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)


def register_models() -> None:
    from app.transactions import models as transaction_models  # noqa: F401
    from app.users_authentication import models as user_models  # noqa: F401


def register_blueprints(app: Flask) -> None:
    from app.home.routes import home
    from app.statistics.routes import statistics
    from app.transactions.routes import transactions
    from app.users_authentication.routes import users

    app.register_blueprint(home)
    app.register_blueprint(transactions)
    app.register_blueprint(users)
    app.register_blueprint(statistics)
