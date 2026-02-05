from pydantic import BaseModel


class BaseGroup(BaseModel):
    name: str
