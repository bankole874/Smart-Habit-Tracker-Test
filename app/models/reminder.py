# app/models/reminders.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import time

class Reminder(SQLModel, table=True):
    __tablename__ = "reminders"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    habit_id: int = Field(foreign_key="habits.id")
    reminder_time: time
    enabled: bool = Field(default=True)
    
    # Relationships
    habit: Habit = Relationship(back_populates="reminders")