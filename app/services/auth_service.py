from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import UniqueConstraint
from app.config import settings

# Database engine
engine = create_engine(
    settings.database_url,
    echo=settings.environment == "development"
)

def create_db_and_tables():
    """Create database tables with constraints"""
    from app.models.habit_progress import HabitProgress
    
    # Add unique constraint to HabitProgress table
    HabitProgress.__table_args__ = (
        UniqueConstraint('habit_id', 'date', name='unique_habit_date'),
    )
    
    SQLModel.metadata.create_all(engine)

def get_session():
    """Database session dependency"""
    with Session(engine) as session:
        yield session
