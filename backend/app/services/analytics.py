from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.db import models
from app.schemas.analytics import (
    DelayedPackage,
    DelayedPackageSummary,
    PackageStatus,
    MilestoneDelaySummary,
    CategoryDelaySummary,
    PackageDelaySummary,
)


def get_delayed_milestones(db: Session) -> list[DelayedPackage]:

    today = date.today()

    rows = (
        db.query(models.Package, models.Milestone, models.PSR)
        .join(models.PSR, models.Package.id == models.PSR.package_id)
        .join(models.Milestone, models.PSR.milestone_id == models.Milestone.id)
        .filter(
            models.Package.is_active.is_(True),
            models.PSR.actual_date.is_(None),
            models.PSR.planned_date.is_not(None),
            models.PSR.planned_date < today,
        )
        .order_by(
            models.Package.package_code,
            models.Milestone.milestone_order,
        )
        .all()
    )

    delayed: list[DelayedPackage] = []

    for package, milestone, psr in rows:
        delay_days = (today - psr.planned_date).days

        delayed.append(
            DelayedPackage(
                package_id=package.id,
                package_code=package.package_code,
                milestone_id=milestone.id,
                milestone_name=milestone.name,
                milestone_order=milestone.milestone_order,
                planned_date=psr.planned_date,
                actual_date=psr.actual_date,
                delay_days=delay_days,
            )
        )

    return delayed


def get_delayed_packages(db: Session) -> list[DelayedPackageSummary]:
    today = date.today()

    rows = (
        db.query(
            models.Package.id,
            models.Package.package_code,
            func.count(models.PSR.id).label("delayed_milestones"),
            func.min(models.PSR.planned_date).label("first_delay_date"),
        )
        .join(models.PSR, models.Package.id == models.PSR.package_id)
        .filter(
            models.Package.is_active.is_(True),
            models.PSR.actual_date.is_(None),
            models.PSR.planned_date.is_not(None),
            models.PSR.planned_date < today,
        )
        .group_by(models.Package.id, models.Package.package_code)
        .order_by(models.Package.package_code)
        .all()
    )

    result: list[DelayedPackageSummary] = []

    for row in rows:
        delay_days = (today - row.first_delay_date).days

        result.append(
            DelayedPackageSummary(
                package_id=row.id,
                package_code=row.package_code,
                delayed_milestones=row.delayed_milestones,
                delay_days=delay_days,
            )
        )

    return result


def get_delay_by_milestone(db: Session) -> list[MilestoneDelaySummary]:
    today = date.today()

    delay_expr = func.coalesce(models.PSR.actual_date, today) - models.PSR.planned_date

    rows = (
        db.query(
            models.Milestone.id,
            models.Milestone.name,
            models.Milestone.milestone_order,
            models.Package.category,
            func.count(models.PSR.id).label("delayed_count"),
            func.sum(delay_expr).label("total_delay_days"),
            func.avg(delay_expr).label("avg_delay_days"),
        )
        .join(models.PSR, models.Milestone.id == models.PSR.milestone_id)
        .join(models.Package, models.Package.id == models.PSR.package_id)
        .filter(
            models.Package.is_active.is_(True),
            models.PSR.planned_date.is_not(None),
            func.coalesce(models.PSR.actual_date, today) > models.PSR.planned_date,
        )
        .group_by(
            models.Milestone.id,
            models.Milestone.name,
            models.Milestone.milestone_order,
            models.Package.category,
        )
        .order_by(func.sum(delay_expr).desc())
        .all()
    )

    result: list[MilestoneDelaySummary] = []

    for row in rows:
        result.append(
            MilestoneDelaySummary(
                milestone_id=row.id,
                milestone_name=row.name,
                milestone_order=row.milestone_order,
                category=row.category,
                delayed_count=row.delayed_count,
                total_delay_days=int(row.total_delay_days or 0),
                avg_delay_days=float(row.avg_delay_days or 0),
            )
        )

    return result


def get_delay_by_category(db: Session) -> list[CategoryDelaySummary]:
    today = date.today()

    delay_expr = func.coalesce(models.PSR.actual_date, today) - models.PSR.planned_date

    rows = (
        db.query(
            models.Package.category,
            func.count(func.distinct(models.Package.id)).label("delayed_packages"),
            func.sum(delay_expr).label("total_delay_days"),
            func.avg(delay_expr).label("avg_delay_days"),
        )
        .join(models.PSR, models.Package.id == models.PSR.package_id)
        .filter(
            models.Package.is_active.is_(True),
            models.PSR.planned_date.is_not(None),
            func.coalesce(models.PSR.actual_date, today) > models.PSR.planned_date,
        )
        .group_by(models.Package.category)
        .order_by(func.sum(delay_expr).desc())
        .all()
    )

    result: list[CategoryDelaySummary] = []

    for row in rows:
        result.append(
            CategoryDelaySummary(
                category=row.category,
                delayed_packages=row.delayed_packages,
                total_delay_days=int(row.total_delay_days or 0),
                avg_delay_days=float(row.avg_delay_days or 0),
            )
        )

    return result


def get_delay_by_package(db: Session) -> list[PackageDelaySummary]:
    today = date.today()

    delay_expr = func.coalesce(models.PSR.actual_date, today) - models.PSR.planned_date

    rows = (
        db.query(
            models.Package.id,
            models.Package.package_code,
            models.Package.category,
            func.count(models.PSR.id).label("delayed_milestones"),
            func.sum(delay_expr).label("total_delay_days"),
            func.avg(delay_expr).label("avg_delay_days"),
        )
        .join(models.PSR, models.Package.id == models.PSR.package_id)
        .filter(
            models.Package.is_active.is_(True),
            models.PSR.planned_date.is_not(None),
            func.coalesce(models.PSR.actual_date, today) > models.PSR.planned_date,
        )
        .group_by(
            models.Package.id, models.Package.package_code, models.Package.category
        )
        .order_by(func.sum(delay_expr).desc())
        .all()
    )

    result: list[PackageDelaySummary] = []

    for row in rows:
        result.append(
            PackageDelaySummary(
                package_id=row.id,
                package_code=row.package_code,
                category=row.category,
                delayed_milestones=row.delayed_milestones,
                total_delay_days=int(row.total_delay_days or 0),
                avg_delay_days=float(row.avg_delay_days or 0),
            )
        )

    return result


def get_package_status(db: Session, package_id: int) -> PackageStatus:

    package = db.query(models.Package).filter(models.Package.id == package_id).first()

    if not package:
        raise ValueError(f"Package {package_id} not found")

    rows = (
        db.query(models.Milestone, models.PSR)
        .join(models.PSR, models.Milestone.id == models.PSR.milestone_id)
        .filter(models.PSR.package_id == package_id)
        .order_by(models.Milestone.milestone_order)
        .all()
    )

    total_milestones = len(rows)
    completed = 0
    total_delay = 0
    current_milestone = None
    current_order = None

    for milestone, psr in rows:
        if psr.actual_date:
            completed += 1

            if psr.planned_date and psr.actual_date > psr.planned_date:
                total_delay += (psr.actual_date - psr.planned_date).days

        elif not current_milestone:
            current_milestone = milestone.name
            current_order = milestone.milestone_order

    if completed == total_milestones:
        current_milestone = "completed"
        current_order = total_milestones

    completion_percentage = (
        (completed / total_milestones) * 100 if total_milestones else 0
    )

    return PackageStatus(
        package_id=package.id,
        package_code=package.package_code,
        current_milestone=current_milestone,
        current_milestone_order=current_order,
        completion_percentage=completion_percentage,
        delayed=total_delay > 0,
        total_delay_days=total_delay,
    )

def get_package_status_v2(db: Session, package_id: int) -> PackageStatus:
    today = date.today()

    package = db.query(models.Package).filter(models.Package.id == package_id).first()
    if not package:
        raise ValueError(f"Package {package_id} not found")

    rows = (
        db.query(models.Milestone, models.PSR)
        .join(models.PSR, models.Milestone.id == models.PSR.milestone_id)
        .filter(models.PSR.package_id == package_id)
        .order_by(models.Milestone.milestone_order)
        .all()
    )

    total_milestones = len(rows)

    if total_milestones == 0:
        return PackageStatus(
            package_id=package.id,
            package_code=package.package_code,
            current_milestone="no milestones",
            current_milestone_order=0,
            completion_percentage=0,
            delayed=False,
            total_delay_days=0,
        )

    completed = 0
    total_delay = 0
    current_milestone = None
    current_order = None
    is_currently_delayed = False

    for milestone, psr in rows:
        if psr.actual_date:
            completed += 1

            if psr.planned_date and psr.actual_date > psr.planned_date:
                total_delay += (psr.actual_date - psr.planned_date).days

        elif current_milestone is None:
            current_milestone = milestone.name
            current_order = milestone.milestone_order

            if psr.planned_date and psr.planned_date < today:
                is_currently_delayed = True
                total_delay += (today - psr.planned_date).days

    if completed == total_milestones:
        current_milestone = "completed"
        current_order = total_milestones

    completion_percentage = (completed / total_milestones) * 100

    return PackageStatus(
        package_id=package.id,
        package_code=package.package_code,
        current_milestone=current_milestone,
        current_milestone_order=current_order,
        completion_percentage=completion_percentage,
        delayed=is_currently_delayed or total_delay > 0,
        total_delay_days=total_delay,
    )