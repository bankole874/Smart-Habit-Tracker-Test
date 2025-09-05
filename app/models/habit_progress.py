# app/models/habit_progress.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, date

class HabitProgress(SQLModel, table=True):
    __tablename__ = "habit_progress"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    habit_id: int = Field(foreign_key="habits.id")
    date: date = Field(index=True)
    completed: bool = Field(default=False)
    note: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    habit: Habit = Relationship(back_populates="progress_entries")
    
    class Config:
        # Ensure unique constraint on habit_id and date
        table_args = ({"unique": ("habit_id", "date")},)
