from typing import List

from pydantic import BaseModel

from backend.src.services.universirty.models.base_student import BaseStudent


class AllStudentsResponse(BaseModel):
    students: List[StudentResponse]


class StudentResponse(BaseStudent):
    id: int
