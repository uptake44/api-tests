from pydantic import BaseModel


class ValidationError(BaseModel):
    loc: list[str | int]
    msg: str
    type: str


class HTTPValidationError(BaseModel):
    detail: list[ValidationError]
