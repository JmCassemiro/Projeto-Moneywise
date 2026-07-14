from datetime import date

from app.users_authentication.models import User, load_user


def test_user_string_representations_and_to_dict(database, app, create_user):
    user = create_user(
        name="Model User",
        email="model@example.com",
        birthday=date(1990, 1, 2),
        avatar="avatar.png",
    )

    with app.app_context():
        data = user.to_dict()

    assert str(user) == "Model User"
    assert repr(user) == f"<User Model User ID {user.id}>"
    assert data["id"] == user.id
    assert data["avatar"] == "avatar.png"
    assert data["name"] == "Model User"
    assert data["email"] == "model@example.com"
    assert data["birthday"] == "1990-01-02"
    assert "created_at" in data
    assert "updated_at" in data


def test_load_user_returns_user_or_none(database, app, create_user):
    user = create_user(email="loader@example.com")

    with app.app_context():
        assert load_user(str(user.id)).id == user.id
        assert load_user("not-a-number") is None
        assert load_user(None) is None
