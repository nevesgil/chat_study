from pydantic import BaseModel
from datetime import date


class MilestoneStatus(BaseModel):
    milestone_id: int
    milestone_name: str
    milestone_order: int
    planned_date: date | None = None
    actual_date: date | None = None


class PackageTimeline(BaseModel):
    package_id: int
    package_code: int
    milestones: list[MilestoneStatus]
