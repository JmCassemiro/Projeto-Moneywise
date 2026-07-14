from flask import Flask

from app.errors import register_error_handlers
from app.exceptions import AppError, AuthenticationError, NotFoundError, ValidationError


def _error_test_app():
    test_app = Flask(__name__)
    register_error_handlers(test_app)
    return test_app


def test_app_error_serializes_message_and_status_code():
    error = AppError("Something happened.", status_code=418)

    assert error.to_dict() == {"error": "Something happened."}
    assert error.status_code == 418


def test_domain_errors_define_expected_status_codes():
    assert ValidationError("bad").status_code == 400
    assert AuthenticationError("nope").status_code == 401
    assert NotFoundError("missing").status_code == 404


def test_app_error_handler_returns_json():
    test_app = _error_test_app()

    @test_app.route("/raise-app-error-for-test")
    def raise_app_error_for_test():
        raise ValidationError("Invalid input.")

    response = test_app.test_client().get(
        "/raise-app-error-for-test",
        headers={"Accept": "application/json"},
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid input."}


def test_not_found_handler_returns_json():
    response = (
        _error_test_app()
        .test_client()
        .get(
            "/missing",
            headers={"Accept": "application/json"},
        )
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Recurso nao encontrado."}
