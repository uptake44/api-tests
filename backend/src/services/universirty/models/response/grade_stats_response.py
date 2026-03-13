from pydantic import BaseModel, Field, StrictInt

from backend.src.services.universirty.models.base_grade import GradeLimits


class GradeStatsResponse(BaseModel):
    count: StrictInt = Field(ge=GradeLimits.MIN)
    min: StrictInt | None = Field(ge=GradeLimits.MIN, le=GradeLimits.MAX)
    max: StrictInt | None = Field(ge=GradeLimits.MIN, le=GradeLimits.MAX)
    avg: float | None = Field(ge=GradeLimits.MIN, le=GradeLimits.MAX)
