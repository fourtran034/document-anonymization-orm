import os

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def database_url() -> str:
    return os.environ.get('DATABASE_URL', 'sqlite:///anonymization.db')


def make_engine(url: str | None = None):
    engine = create_engine(url or database_url())
    if engine.dialect.name == 'sqlite':
        @event.listens_for(engine, 'connect')
        def enable_foreign_keys(dbapi_connection, _):
            cursor = dbapi_connection.cursor()
            try:
                cursor.execute('PRAGMA foreign_keys = ON')
            finally:
                cursor.close()
    return engine
