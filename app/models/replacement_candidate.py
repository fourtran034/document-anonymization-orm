from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.anonymization_job import AnonymizationJob


class ReplacementCandidate(Base):
    """A location and proposed replacement token; no original personal data."""

    __tablename__ = 'replacement_candidates'

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(
        ForeignKey('anonymization_jobs.id', ondelete='CASCADE'), index=True
    )
    location: Mapped[str] = mapped_column(String(120))
    category: Mapped[str] = mapped_column(String(40))
    token: Mapped[str] = mapped_column(String(80))
    approved: Mapped[bool | None]  # None means not yet reviewed.
    job: Mapped['AnonymizationJob'] = relationship(back_populates='candidates')
