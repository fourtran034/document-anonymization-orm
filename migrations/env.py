from alembic import context

from app import models  # Import all models so they are registered in Base.metadata.
from app.db import Base, database_url, make_engine


def migrate() -> None:
    if context.is_offline_mode():
        context.configure(url=database_url(), target_metadata=Base.metadata,
                          literal_binds=True, dialect_opts={'paramstyle': 'named'})
        with context.begin_transaction():
            context.run_migrations()
    else:
        engine = make_engine()
        try:
            with engine.connect() as connection:
                context.configure(connection=connection, target_metadata=Base.metadata)
                with context.begin_transaction():
                    context.run_migrations()
        finally:
            engine.dispose()


migrate()
