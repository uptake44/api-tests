from enum import StrEnum

from pydantic import BaseModel


class SubjectEnum(StrEnum):
    MATH = "Mathematics"
    PHYS = "Physics"
    HIST = "History"
    BIOL = "Biology"
    GEOG = "Geography"


class BaseTeacher(BaseModel):
    first_name: str
    last_name: str
    subject: SubjectEnum
