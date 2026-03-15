from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, date
from typing import Optional

from .db import Base


class Package(Base):
    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(primary_key=True)
    package_code: Mapped[int]
    package_description: Mapped[str]
    category: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    psr_entries: Mapped[list["PSR"]] = relationship("PSR", back_populates="package")


class Milestone(Base):
    __tablename__ = "milestones"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    milestone_order: Mapped[int] = mapped_column(unique=True)

    psr_entries: Mapped[list["PSR"]] = relationship("PSR", back_populates="milestone")


class PSR(Base):
    __tablename__ = "psr"

    id: Mapped[int] = mapped_column(primary_key=True)

    package_id: Mapped[int] = mapped_column(ForeignKey("packages.id"))
    milestone_id: Mapped[int] = mapped_column(ForeignKey("milestones.id"))

    planned_date: Mapped[Optional[date]]
    actual_date: Mapped[Optional[date]]

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    package: Mapped["Package"] = relationship("Package", back_populates="psr_entries")
    milestone: Mapped["Milestone"] = relationship(
        "Milestone", back_populates="psr_entries"
    )


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)

    psr_id: Mapped[int] = mapped_column(ForeignKey("psr.id"))
    comment_text: Mapped[str]
    created_by: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
