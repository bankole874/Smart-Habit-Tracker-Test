# app/models/streak.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date

class Streak(SQLModel, table=True):
    __tablename__ = "streaks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    habit_id: int = Field(foreign_key="habits.id")
    start_date: date
    end_date: Optional[date] = Field(default=None)
    longest: bool = Field(default=False)
    current: bool = Field(default=False)
    
    # Relationships
    habit: Habit = Relationship(back_populates="streaks")
