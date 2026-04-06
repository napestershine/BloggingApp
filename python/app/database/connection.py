from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import get_settings

Base = declarative_base()


def get_engine():
    settings = get_settings()
    return create_engine(settings.database_url)


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session_local():
    return SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
