from enum import StrEnum, IntEnum


class ValidationErrorType(StrEnum):
    NO_REQUIRED_FIELD = "missing"
    VALUE_ERROR = "value_error"


class ResponseMessage(StrEnum):
    USERNAME_TAKEN = "Username is already taken"
    EMAIL_TAKEN = "Email is already taken"
    INVALID_LOGIN = "Invalid login credentials"


class GradeCount(IntEnum):
    MIN = 3
    MAX = 6
