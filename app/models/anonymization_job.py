from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.replacement_candidate import ReplacementCandidate


class JobStatus(StrEnum):
    DRAFT = 'draft'
    IN_REVIEW = 'in_review'
    COMPLETED = 'completed'


class AnonymizationJob(Base):
    __tablename__ = 'anonymization_jobs'

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey('documents.id'), index=True)
    status: Mapped[JobStatus] = mapped_column(
        Enum(JobStatus, name='job_status', native_enum=False, create_constraint=True,
             values_callable=lambda enum: [member.value for member in enum]),
        default=JobStatus.DRAFT,
    )
    document: Mapped['Document'] = relationship(back_populates='jobs')
    candidates: Mapped[list['ReplacementCandidate']] = relationship(
        back_populates='job', cascade='all, delete-orphan', passive_deletes=True
    )
