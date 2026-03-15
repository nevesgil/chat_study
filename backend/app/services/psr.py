from sqlalchemy.orm import Session
from datetime import date
from app.db import models
from app.schemas.psr import PSRCreate
from app.schemas.psr import PSRUpdate


def get_psr(db: Session, package_id: int | None = None) -> list[models.PSR]:
    query = db.query(models.PSR)
    if package_id is not None:
        query = query.filter(models.PSR.package_id == package_id)
    return query.all()


def create_psr(db: Session, psr_create: PSRCreate) -> models.PSR:
    new_psr = models.PSR(
        package_id=psr_create.package_id,
        milestone_id=psr_create.milestone_id,
        planned_date=psr_create.planned_date,
        actual_date=psr_create.actual_date,
    )

    db.add(new_psr)
    db.commit()
    db.refresh(new_psr)

    return new_psr


def update_psr_dates(
    db: Session, psr_id: int, psr_update: PSRUpdate
) -> models.PSR | None:

    psr = db.query(models.PSR).filter(models.PSR.id == psr_id).first()

    if not psr:
        return None

    if psr_update.planned_date is not None:
        psr.planned_date = psr_update.planned_date

    if psr_update.actual_date is not None:
        psr.actual_date = psr_update.actual_date

    db.commit()
    db.refresh(psr)

    return psr


def complete_psr(
    db: Session, psr_id: int, completion_date: date | None = None
) -> models.PSR | None:
    psr = db.query(models.PSR).filter(models.PSR.id == psr_id).first()

    if not psr:
        return None

    psr.actual_date = completion_date or date.today()
    db.commit()
    db.refresh(psr)

    return psr
