from datetime import date
from pydantic import BaseModel


class ProcurementSummary(BaseModel):
    total_packages: int
    active_packages: int
    completed_packages: int
    delayed_packages: int
    avg_delay_days: float | None


class CategoryDelaySummary(BaseModel):
    category: str
    delayed_packages: int
    total_delay_days: int
    avg_delay_days: float


class DelayedPackageSummary(BaseModel):
    package_id: int
    package_code: int
    delayed_milestones: int
    delay_days: int


class PackageDelaySummary(BaseModel):
    package_id: int
    package_code: int
    category: str
    delayed_milestones: int
    total_delay_days: int
    avg_delay_days: float


class MilestoneDelaySummary(BaseModel):
    milestone_id: int
    milestone_name: str
    milestone_order: int
    category: str
    delayed_count: int
    total_delay_days: int
    avg_delay_days: float


class DelayedPackage(BaseModel):
    package_id: int
    package_code: int
    milestone_id: int
    milestone_name: str
    milestone_order: int
    planned_date: date
    actual_date: date | None
    delay_days: int


class PackageStatus(BaseModel):
    package_id: int
    package_code: int
    current_milestone: str | None = None
    current_milestone_order: int | None = None
    completion_percentage: float
    delayed: bool
    total_delay_days: int


class PSRDetail(BaseModel):
    package_code: int
    package_description: str
    milestone_name: str
    milestone_order: int
    planned_date: date | None = None
    actual_date: date | None = None


class PSRDetailWithAnalytics(PSRDetail):
    delay_days: int | None = None
    is_delayed: bool = False
    is_completed: bool = False
