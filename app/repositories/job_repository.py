from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AnonymizationJob, JobStatus


class JobRepository:
    """Access to anonymization jobs; the caller owns the session transaction."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, document_id: int) -> AnonymizationJob:
        job = AnonymizationJob(document_id=document_id)
        self.session.add(job)
        self.session.flush()
        return job

    def get(self, job_id: int) -> AnonymizationJob | None:
        return self.session.get(AnonymizationJob, job_id)

    def list_for_document(self, document_id: int) -> list[AnonymizationJob]:
        query = (select(AnonymizationJob)
                 .where(AnonymizationJob.document_id == document_id)
                 .order_by(AnonymizationJob.id))
        return list(self.session.scalars(query))

    def update_status(self, job_id: int, status: JobStatus) -> AnonymizationJob | None:
        job = self.get(job_id)
        if job is not None:
            job.status = status
        return job

    def delete(self, job_id: int) -> bool:
        job = self.get(job_id)
        if job is None:
            return False
        self.session.delete(job)
        return True
