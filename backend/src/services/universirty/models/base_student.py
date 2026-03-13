from enum import StrEnum

from pydantic import BaseModel, EmailStr


class DegreeEnum(StrEnum):
    ASSOCIATE = "Associate"
    BACHELOR = "Bachelor"
    MASTER = "Master"
    DOCTORATE = "Doctorate"


class BaseStudent(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    degree: DegreeEnum
    phone: str
    group_id: int
