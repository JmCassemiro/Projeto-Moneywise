class AppError(Exception):
    status_code = 400

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self) -> dict[str, str]:
        return {"error": self.message}


class ValidationError(AppError):
    status_code = 400


class AuthenticationError(AppError):
    status_code = 401


class NotFoundError(AppError):
    status_code = 404
