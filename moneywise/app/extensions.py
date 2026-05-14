from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
jwt = JWTManager()
mail = Mail()
bcrypt = Bcrypt()
csrf = CSRFProtect()

login_manager.login_view = "users.signin_page"
login_manager.login_message_category = "auth"
