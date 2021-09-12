from http import HTTPStatus
from json import dumps
from typing import Optional


# Base HttpError class
class HttpError(Exception):
    def __init__(
        self,
        status: int = HTTPStatus.INTERNAL_SERVER_ERROR,
        code: str = "internal_failure",
        message: str = "Internal Failure",
    ):
        self.status = status
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return dumps(self.to_dict())

    def to_dict(self) -> dict:
        return {"code": self.code, "message": self.message}


# Base Error classes


class IntentionalError(HttpError):
    pass


class UnauthorizedError(HttpError):  # Wrong or expired credentials
    def __init__(self, error: str = "authorization_error", message: str = "Authorization error"):
        super().__init__(HTTPStatus.UNAUTHORIZED, error, message)


class ForbiddenError(HttpError):  # Authorization acknowledged, but insufficient rights
    def __init__(self, error: str = "forbidden", message: str = "Not authorized to perform this action"):
        super().__init__(HTTPStatus.FORBIDDEN, error, message)


class UnhandledEventError(HttpError):
    def __init__(self, error: str = "unhandled_event", message: str = "Unhandled Event"):
        super().__init__(HTTPStatus.NOT_IMPLEMENTED, error, message)


class NotFoundError(HttpError):
    def __init__(self, error: str = "not_found", message: str = "Resource not found"):
        super().__init__(HTTPStatus.NOT_FOUND, error, message)


class BadRequestError(HttpError):
    def __init__(self, error: str = "bad_request", message: str = "Bad Request"):
        super().__init__(HTTPStatus.BAD_REQUEST, error, message)


class ConflictError(HttpError):
    def __init__(self, error: str = "conflict", message: str = "Conflict"):
        super().__init__(HTTPStatus.CONFLICT, error, message)


class InvalidParamsError(HttpError):
    def __init__(self, error: str = "invalid_params", message: str = "Invalid params"):
        super().__init__(HTTPStatus.UNPROCESSABLE_ENTITY, error, message)

