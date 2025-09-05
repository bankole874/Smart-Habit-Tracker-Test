from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, date

if TYPE_CHECKING:
    from app.models.habit import Habit

class HabitProgress(SQLModel, table=True):
    __tablename__ = "habit_progress"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    habit_id: int = Field(foreign_key="habits.id")
    date: date = Field(index=True)
    completed: bool = Field(default=False)
    note: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships - use string reference
    habit: "Habit" = Relationship(back_populates="progress_entries")
    
    class Config:
        # Note: SQLModel doesn't use table_args the same way as SQLAlchemy
        # The unique constraint should be handled differently
        pass
