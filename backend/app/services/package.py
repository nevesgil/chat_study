from sqlalchemy.orm import Session
from app.db import models
from app.schemas.package import PackageCreate


def get_packages(db: Session) -> list[models.Package]:
    return db.query(models.Package).all()


def get_package_by_id(db: Session, package_id: int) -> models.Package | None:
    return db.query(models.Package).filter(models.Package.id == package_id).first()


def create_package(db: Session, package: PackageCreate) -> models.Package:
    new_package = models.Package(
        package_code=package.package_code,
        package_description=package.package_description,
        category=package.category,
    )

    db.add(new_package)
    db.commit()
    db.refresh(new_package)

    return new_package


def deactivate_package(db: Session, package_id: int) -> models.Package | None:
    package = db.query(models.Package).filter(models.Package.id == package_id).first()

    if package:
        package.is_active = False
        db.commit()
        db.refresh(package)

    return package
