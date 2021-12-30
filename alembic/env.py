from app.schemas import *
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

from sqlmodel import SQLModel

from app.db.db import DATABASE_URL

config = context.config

fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

url = DATABASE_URL


def run_migrations_offline():
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(
            url=url,
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
