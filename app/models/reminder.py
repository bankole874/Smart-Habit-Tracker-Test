from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import time

if TYPE_CHECKING:
    from app.models.habit import Habit

class Reminder(SQLModel, table=True):
    __tablename__ = "reminders"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    habit_id: int = Field(foreign_key="habits.id")
    reminder_time: time
    enabled: bool = Field(default=True)
    
    # Relationships - use string reference
    habit: "Habit" = Relationship(back_populates="reminders")