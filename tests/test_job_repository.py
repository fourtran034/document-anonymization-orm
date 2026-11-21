import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alembic import command
from alembic.config import Config
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import make_engine
from app.models import Document, JobStatus, ReplacementCandidate
from app.repositories.job_repository import JobRepository


class JobRepositoryTest(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(folder.cleanup)
        url = f'sqlite:///{Path(folder.name) / "test.db"}'
        with patch.dict('os.environ', {'DATABASE_URL': url}):
            command.upgrade(Config('alembic.ini'), 'head')
        self.engine = make_engine(url)
        self.addCleanup(self.engine.dispose)

    def test_crud_and_cascade_on_migrated_schema(self):
        with Session(self.engine) as session, session.begin():
            first = Document(reference='example-a', sha256='a' * 64)
            second = Document(reference='example-b', sha256='b' * 64)
            session.add_all([first, second])
            session.flush()
            repo = JobRepository(session)
            a = repo.create(first.id)
            other = repo.create(second.id)
            b = repo.create(first.id)
            self.assertEqual(a.status, JobStatus.DRAFT)
            candidate = ReplacementCandidate(location='Абзац 7', category='имя', token='[ЛИЦО-1]')
            a.candidates.append(candidate)
            repo.update_status(a.id, JobStatus.IN_REVIEW)
            session.flush()
            document_id, a_id, b_id, other_id, candidate_id = first.id, a.id, b.id, other.id, candidate.id

        with Session(self.engine) as session, session.begin():
            repo = JobRepository(session)
            self.assertEqual([job.id for job in repo.list_for_document(document_id)], [a_id, b_id])
            self.assertEqual(repo.get(a_id).status, JobStatus.IN_REVIEW)
            self.assertTrue(repo.delete(a_id))

        with Session(self.engine) as session:
            repo = JobRepository(session)
            self.assertIsNone(repo.get(a_id))
            self.assertIsNone(session.get(ReplacementCandidate, candidate_id))
            self.assertIsNotNone(repo.get(other_id))
            self.assertFalse(repo.delete(a_id))

    def test_create_rejects_missing_document(self):
        with Session(self.engine) as session:
            with self.assertRaises(IntegrityError), session.begin():
                JobRepository(session).create(999)
