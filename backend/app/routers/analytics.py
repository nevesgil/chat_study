from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.schemas.analytics import DelayedPackage, DelayedPackageSummary, PackageStatus
from app.services import analytics as analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/delayed-milestones", response_model=list[DelayedPackage])
def get_delayed_milestones(db: Session = Depends(get_db)):
    return analytics_service.get_delayed_milestones(db)


@router.get("/delayed-packages", response_model=list[DelayedPackageSummary])
def get_delayed_packages(db: Session = Depends(get_db)):
    return analytics_service.get_delayed_packages(db)


@router.get("/delay-by")
def get_delay_by(
    dimension: str = Query(..., pattern="^(category|milestone|package)$"),
    db: Session = Depends(get_db),
) -> list[Any]:
    if dimension == "category":
        return analytics_service.get_delay_by_category(db)
    if dimension == "milestone":
        return analytics_service.get_delay_by_milestone(db)
    if dimension == "package":
        return analytics_service.get_delay_by_package(db)

    raise HTTPException(status_code=400, detail="Invalid dimension")


@router.get("/package-status/{package_id}", response_model=PackageStatus)
def get_package_status(
    package_id: int,
    db: Session = Depends(get_db),
):
    try:
        return analytics_service.get_package_status(db, package_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
