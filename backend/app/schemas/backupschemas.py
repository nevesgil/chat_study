from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict


# ============================================================================
# PACKAGE SCHEMAS
# ============================================================================


class PackageCategory(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    Std = "Std"


class PackageBase(BaseModel):
    package_code: int
    package_description: str
    category: PackageCategory


class PackageCreate(PackageBase):
    pass


class PackageUpdate(BaseModel):
    package_description: str | None = None
    category: PackageCategory | None = None
    is_active: bool | None = None


class PackageResponse(PackageBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# MILESTONE SCHEMAS
# ============================================================================


class MilestoneResponse(BaseModel):
    id: int
    name: str
    milestone_order: int

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# PSR SCHEMAS
# ============================================================================


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


# ============================================================================
# COMMENT SCHEMAS
# ============================================================================


class CommentBase(BaseModel):
    comment_text: str


class CommentCreate(CommentBase):
    psr_id: int
    created_by: str | None = None


class CommentUpdate(BaseModel):
    comment_text: str | None = None
    created_by: str | None = None


class CommentResponse(CommentBase):
    id: int
    psr_id: int
    created_by: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# ANALYTICS SCHEMAS
# ============================================================================


class ProcurementSummary(BaseModel):
    total_packages: int
    active_packages: int
    completed_packages: int
    delayed_packages: int
    avg_delay_days: float


class DelayedPackage(BaseModel):
    package_id: int
    package_code: int
    milestone_id: int
    milestone_name: str
    milestone_order: int
    planned_date: date
    actual_date: date | None = None
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


# ============================================================================
# TIMELINE SCHEMAS
# ============================================================================


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
