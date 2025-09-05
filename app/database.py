# app/database.py

from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

# Database engine
engine = create_engine(
    settings.database_url,
    echo=settings.environment == "development"
)

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Database session dependency"""
    with Session(engine) as session:
        yield session