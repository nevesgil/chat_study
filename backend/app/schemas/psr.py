from pydantic import BaseModel, ConfigDict
from datetime import date


class PSRCreate(BaseModel):
    package_id: int
    milestone_id: int
    planned_date: date | None = None
    actual_date: date | None = None


class PSRUpdate(BaseModel):
    planned_date: date | None = None
    actual_date: date | None = None


class PSRResponse(BaseModel):
    id: int
    package_id: int
    milestone_id: int
    planned_date: date | None = None
    actual_date: date | None = None

    model_config = ConfigDict(from_attributes=True)
