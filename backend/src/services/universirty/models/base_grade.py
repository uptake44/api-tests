from pydantic import BaseModel, Field, StrictInt


class BaseGrade(BaseModel):
    teacher_id: int
    student_id: int
    grade: StrictInt = Field(ge=0, le=5)
