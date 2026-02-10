from typing import List

from pydantic import BaseModel

from backend.src.services.universirty.models.base_grade import BaseGrade


class AllGradesResponse(BaseModel):
    grades: List[GradeResponse]


class GradeResponse(BaseGrade):
    id: int
