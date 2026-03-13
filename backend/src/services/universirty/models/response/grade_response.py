from pydantic import BaseModel

from backend.src.services.universirty.models.base_grade import BaseGrade


class GradeResponse(BaseGrade):
    id: int


class AllGradesResponse(BaseModel):
    grades: list[GradeResponse]
