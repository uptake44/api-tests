from enum import StrEnum, IntEnum


class ValidationErrorType(StrEnum):
    NO_REQUIRED_FIELD = "missing"
    VALUE_ERROR = "value_error"


class GradeCount(IntEnum):
    MIN = 3
    MAX = 6
