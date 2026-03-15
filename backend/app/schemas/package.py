from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum


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
