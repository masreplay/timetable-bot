from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, SQLModel, Session

from core.config import get_settings, Settings

settings: Settings = get_settings()

DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session
