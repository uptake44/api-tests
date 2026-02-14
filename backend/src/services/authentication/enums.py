from enum import StrEnum


class ResponseMessage(StrEnum):
    USERNAME_TAKEN = "Username is already taken"
    EMAIL_TAKEN = "Email is already taken"
    INVALID_LOGIN = "Invalid login credentials"