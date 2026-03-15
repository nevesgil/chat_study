from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.timeline import PackageTimeline
from app.services import timeline as timeline_service

router = APIRouter(prefix="/timeline", tags=["timeline"])


@router.get("/{package_id}", response_model=PackageTimeline)
def get_timeline(package_id: int, db: Session = Depends(get_db)):
    timeline = timeline_service.get_package_timeline(db, package_id)
    if timeline is None:
        raise HTTPException(status_code=404, detail="Timeline not found")
    return timeline
