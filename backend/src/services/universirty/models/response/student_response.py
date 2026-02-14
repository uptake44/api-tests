from pydantic import BaseModel

from backend.src.services.universirty.models.base_student import BaseStudent


class StudentResponse(BaseStudent):
    id: int


class AllStudentsResponse(BaseModel):
    students: list[StudentResponse]
