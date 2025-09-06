from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

Base = declarative_base()

def get_engine():
    settings = get_settings()
    return create_engine(settings.database_url)

def get_session_local():
    engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()