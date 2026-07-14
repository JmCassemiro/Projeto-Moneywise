from sqlalchemy import select

from app.extensions import db
from app.users_authentication.models import User


class UserRepository:
    @staticmethod
    def get_by_id(user_id: int | str) -> User | None:
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None

    @staticmethod
    def find_by_email(email: str) -> User | None:
        return db.session.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()

    @staticmethod
    def find_by_name(name: str) -> User | None:
        return db.session.execute(
            select(User).where(User.name == name)
        ).scalar_one_or_none()

    @staticmethod
    def add(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def delete(user: User) -> None:
        db.session.delete(user)
        db.session.commit()
