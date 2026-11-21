from hashlib import sha256
from uuid import uuid4

from sqlalchemy.orm import Session

from app.db import make_engine
from app.models import Document, JobStatus, ReplacementCandidate
from app.repositories.job_repository import JobRepository


def main() -> None:
    engine = make_engine()
    with Session(engine) as session, session.begin():
        document = Document(reference=f'demo-{uuid4()}', sha256=sha256(b'example docx').hexdigest())
        session.add(document)
        session.flush()
        repo = JobRepository(session)
        job = repo.create(document.id)
        job.candidates.append(ReplacementCandidate(
            location='Абзац 2', category='имя', token='[ЛИЦО-1]'
        ))
        print(f'Создано задание №{job.id}: {job.status}')
        print('Найдено заданий по документу:', len(repo.list_for_document(document.id)))
        repo.update_status(job.id, JobStatus.IN_REVIEW)
        print('Новый статус:', repo.get(job.id).status)
        repo.delete(job.id)
        session.flush()
        print('После удаления:', repo.get(job.id))
        session.delete(document)
    engine.dispose()


if __name__ == '__main__':
    main()
