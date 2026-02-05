from enum import StrEnum


class ValidationErrorType(StrEnum):
    NO_REQUIRED_FIELD = "missing"
    VALUE_ERROR = "value_error"
