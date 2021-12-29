import os

from sqlmodel import create_engine, SQLModel, Session

from config import get_settings, Settings

settings: Settings = get_settings()

DATABASE_URL = os.getenv('', settings.database_url)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
