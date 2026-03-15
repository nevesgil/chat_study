from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.services import package as package_service
from app.schemas.package import PackageCreate, PackageResponse, PackageUpdate

router = APIRouter(prefix="/packages", tags=["packages"])


@router.get("", response_model=list[PackageResponse])
def get_packages(db: Session = Depends(get_db)):
    """Get all packages"""
    return package_service.get_packages(db)


@router.get("/{package_id}", response_model=PackageResponse)
def get_package(package_id: int, db: Session = Depends(get_db)):
    """Get a package by ID"""
    package = package_service.get_package_by_id(db, package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package


@router.post("", response_model=PackageResponse, status_code=201)
def create_package(package: PackageCreate, db: Session = Depends(get_db)):
    """Create a new package"""
    return package_service.create_package(db, package)


@router.patch("/{package_id}", response_model=PackageResponse)
def update_package(
    package_id: int, package_update: PackageUpdate, db: Session = Depends(get_db)
):
    """Update a package"""
    package = package_service.get_package_by_id(db, package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    if package_update.package_description is not None:
        package.package_description = package_update.package_description
    if package_update.category is not None:
        package.category = package_update.category
    if package_update.is_active is not None:
        package.is_active = package_update.is_active

    db.commit()
    db.refresh(package)
    return package


@router.patch("/{package_id}/deactivate", response_model=PackageResponse)
def deactivate_package(package_id: int, db: Session = Depends(get_db)):
    """Deactivate a package by setting is_active to False"""
    package = package_service.deactivate_package(db, package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package
