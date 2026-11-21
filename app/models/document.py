from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models.anonymization_job import AnonymizationJob


class Document(Base):
    """Metadata only: the source file and its contents are not stored."""

    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(primary_key=True)
    reference: Mapped[str] = mapped_column(String(100), unique=True)
    sha256: Mapped[str] = mapped_column(String(64))
    jobs: Mapped[list['AnonymizationJob']] = relationship(
        back_populates='document', passive_deletes='all'
    )
