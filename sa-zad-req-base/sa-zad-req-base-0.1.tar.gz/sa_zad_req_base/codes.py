from enum import IntEnum
from http import HTTPStatus

__all__ = ['ErrorCode']


# noinspection PyInitNewSignature,PyTypeChecker
class ErrorCode(IntEnum):
    def __new__(cls, value, phrase, description=''):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.phrase = phrase
        obj.description = description
        return obj

    USER_NOT_FOUND = 1, "User not found", "The user is not found."
    CODE_NOT_FOUND = 11, "Code not found", "The code requested does not exists or has already used."
    ACCOUNT_SUSPENDED = 2, "User suspended", "The user account has been suspended and information cannot be retrieved"
    USER_LOCKED_OUT = 3, "User locked out", "The user account has been locked out and information cannot be retrieved"
    USER_LOCKING_OUT_WARNING = 4, "User locking out warning", "The user account is at risk of locking out"
    ACCOUNT_SUSPENSION_WARNING = 5, "User suspension warning", "The user account is at risk of suspension"
    EXPIRED_OR_INVALID_TOKEN = 6, "Invalid or expired token", "The access token used in the request is incorrect or " \
                                                              "has expired. "
    INVALID_FIELD_VALUE = 8, "Invalid field value", "The value provided for the field is invalid or did not match the " \
                                                    "requirement. "
    AUTH_TOKEN_EXPIRED = 9, "Auth token expired", "Authorization failed."
    AUTH_TOKEN_NOT_FOUND = 7, "Auth token not found", "User is not authorized."
    INVALID_AUTH_TOKEN = 10, "Invalid auth token", "Token provided is not valid."

    INVALID_GOOGLE_AUTH_TOKEN = 19, "Invalid google auth token", "Google account can not be authenticated"

    EMAIL_ALREADY_EXISTS = 15, "Email already exists", "Email provided already exists with different account."
    FIELDS_MISSING = 16, "Fields missing", "Required fields not provided."

    INVALID_METHOD = 18, "Invalid method", "Method requested in invalid. Check the API docs."
    INTERNAL_ERROR = 20, "Internal error", "Something went wrong on our side."
    FIELDS_ERROR = 21, "Fields error", "Fields error."

    INVALID_FCM_TOKEN = 22, "FCM token error", "FCM token provided is invalid"

    def get_http_status_code(self) -> HTTPStatus:
        if self.is_USER_NOT_FOUND() or self.is_USER_LOCKING_OUT_WARNING() or self.is_ACCOUNT_SUSPENSION_WARNING() \
                or self.is_CODE_NOT_FOUND():
            return HTTPStatus.NOT_FOUND
        elif self.is_USER_LOCKED_OUT() or self.is_ACCOUNT_SUSPENDED() or self.is_INVALID_FIELD_VALUE() or self.is_AUTH_TOKEN_EXPIRED() or self.is_GOOGLE_AUTH_TOKEN_EXPIRED() or self.is_EXPIRED_OR_INVALID_TOKEN() or self.is_EMAIL_ALREADY_EXISTS() or self.is_FIELDS_ERROR() or self.INVALID_FCM_TOKEN:
            return HTTPStatus.FORBIDDEN
        elif self.is_AUTH_TOKEN_NOT_FOUND() or self.is_INVALID_AUTH_TOKEN():
            return HTTPStatus.UNAUTHORIZED
        elif self.value == ErrorCode.INTERNAL_ERROR.value:
            return HTTPStatus.INTERNAL_SERVER_ERROR

        return HTTPStatus.METHOD_NOT_ALLOWED

    def is_same(self, error):
        return self.value == error.value

    def is_ACCOUNT_SUSPENDED(self):
        return self.is_same(ErrorCode.ACCOUNT_SUSPENDED)

    def is_USER_NOT_FOUND(self):
        return self.is_same(ErrorCode.USER_NOT_FOUND)

    def is_USER_LOCKED_OUT(self):
        return self.is_same(ErrorCode.USER_LOCKED_OUT)

    def is_USER_LOCKING_OUT_WARNING(self):
        return self.is_same(ErrorCode.USER_LOCKING_OUT_WARNING)

    def is_ACCOUNT_SUSPENSION_WARNING(self):
        return self.is_same(ErrorCode.ACCOUNT_SUSPENSION_WARNING)

    def is_EXPIRED_OR_INVALID_TOKEN(self):
        return self.is_same(ErrorCode.EXPIRED_OR_INVALID_TOKEN)

    def is_INVALID_FIELD_VALUE(self):
        return self.is_same(ErrorCode.INVALID_FIELD_VALUE)

    def is_AUTH_TOKEN_NOT_FOUND(self):
        return self.is_same(ErrorCode.AUTH_TOKEN_NOT_FOUND)

    def is_AUTH_TOKEN_EXPIRED(self):
        return self.is_same(ErrorCode.AUTH_TOKEN_EXPIRED)

    def is_INVALID_AUTH_TOKEN(self):
        return self.is_same(ErrorCode.INVALID_AUTH_TOKEN)

    def is_EMAIL_ALREADY_EXISTS(self):
        return self.is_same(ErrorCode.EMAIL_ALREADY_EXISTS)

    def is_FIELDS_MISSING(self):
        return self.is_same(ErrorCode.FIELDS_MISSING)

    def is_FIELDS_ERROR(self):
        return self.is_same(ErrorCode.FIELDS_ERROR)

    def is_INVALID_FCM_TOKEN(self):
        return self.is_same(ErrorCode.INVALID_FCM_TOKEN)
