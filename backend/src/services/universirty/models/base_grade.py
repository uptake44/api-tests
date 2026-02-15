from enum import IntEnum

from pydantic import BaseModel, Field, StrictInt

class GradeLimits(IntEnum):
    MAX = 5
    MIN = 0

class BaseGrade(BaseModel):
    teacher_id: int
    student_id: int
    grade: StrictInt = Field(ge=GradeLimits.MIN, le=GradeLimits.MAX)
