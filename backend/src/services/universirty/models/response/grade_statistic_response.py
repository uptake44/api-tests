from pydantic import BaseModel, Field, StrictInt


class GradeStatisticResponse(BaseModel):
    count: StrictInt = Field(ge=0)
    min: StrictInt | None = Field(ge=0, le=5)
    max: StrictInt | None = Field(ge=0, le=5)
    avg: float | None = Field(ge=0, le=5)