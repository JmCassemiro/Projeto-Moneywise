from datetime import datetime, timezone

from flask_login import UserMixin

from app.extensions import bcrypt, db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    avatar = db.Column(db.String(255), nullable=True)

    transactions = db.relationship(
        "Transaction",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __init__(
        self,
        email: str,
        name: str,
        password: str,
        birthday,
        avatar: str | None = None,
    ):
        self.email = email
        self.name = name
        self.set_password(password)
        self.birthday = birthday
        self.avatar = avatar

    def __repr__(self) -> str:
        return f"<User {self.name} ID {self.id}>"

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "avatar": self.avatar,
            "name": self.name,
            "email": self.email,
            "birthday": self.birthday.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.hashed_password, password)

    def set_password(self, password: str) -> None:
        self.hashed_password = bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None
