# app/models/habit.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, time
from enum import Enum

from app.models.user import User

class FrequencyType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    CUSTOM = "custom"

class Habit(SQLModel, table=True):
    __tablename__ = "habits"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    frequency: FrequencyType = Field(default=FrequencyType.DAILY)
    reminder_time: Optional[time] = Field(default=None)
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    archived: bool = Field(default=False)
    
    # Relationships
    user: User = Relationship(back_populates="habits")
    progress_entries: List["HabitProgress"] = Relationship(back_populates="habit")
    streaks: List["Streak"] = Relationship(back_populates="habit")
    reminders: List["Reminder"] = Relationship(back_populates="habit")
