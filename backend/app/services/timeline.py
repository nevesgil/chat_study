from sqlalchemy.orm import Session
from app.db import models
from app.schemas.timeline import PackageTimeline, MilestoneStatus


def get_package_timeline(db: Session, package_id: int) -> PackageTimeline | None:

    psr_rows = (
        db.query(models.Package, models.PSR, models.Milestone)
        .join(models.PSR, models.Package.id == models.PSR.package_id)
        .join(models.Milestone, models.PSR.milestone_id == models.Milestone.id)
        .filter(models.Package.id == package_id)
        .order_by(models.Milestone.milestone_order)
        .all()
    )

    if not psr_rows:
        return None

    package = psr_rows[0][0]

    milestones: list[MilestoneStatus] = []

    for _, psr, milestone in psr_rows:
        milestones.append(
            MilestoneStatus(
                milestone_id=milestone.id,
                milestone_name=milestone.name,
                milestone_order=milestone.milestone_order,
                planned_date=psr.planned_date,
                actual_date=psr.actual_date,
            )
        )

    return PackageTimeline(
        package_id=package.id, package_code=package.package_code, milestones=milestones
    )
