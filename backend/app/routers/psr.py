from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.psr import PSRCreate, PSRResponse, PSRUpdate
from app.services import psr as psr_service

router = APIRouter(prefix="/psr", tags=["psr"])


@router.get("", response_model=list[PSRResponse])
def get_psr(package_id: int | None = None, db: Session = Depends(get_db)):
    return psr_service.get_psr(db, package_id)


@router.post("", response_model=PSRResponse, status_code=201)
def create_psr(psr_create: PSRCreate, db: Session = Depends(get_db)):
    return psr_service.create_psr(db, psr_create)


@router.patch("/{psr_id}", response_model=PSRResponse)
def update_psr(psr_id: int, psr_update: PSRUpdate, db: Session = Depends(get_db)):
    psr = psr_service.update_psr_dates(db, psr_id, psr_update)
    if not psr:
        raise HTTPException(status_code=404, detail="PSR not found")
    return psr


@router.patch("/{psr_id}/complete", response_model=PSRResponse)
def complete_psr(
    psr_id: int, actual_date: date | None = None, db: Session = Depends(get_db)
):
    psr = psr_service.complete_psr(db, psr_id, actual_date)
    if not psr:
        raise HTTPException(status_code=404, detail="PSR not found")
    return psr
