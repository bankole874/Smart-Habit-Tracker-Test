from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, time
from enum import Enum

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.habit_progress import HabitProgress
    from app.models.streak import Streak
    from app.models.reminder import Reminder

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
    
    # Relationships - use string references
    user: "User" = Relationship(back_populates="habits")
    progress_entries: List["HabitProgress"] = Relationship(back_populates="habit")
    streaks: List["Streak"] = Relationship(back_populates="habit")
    reminders: List["Reminder"] = Relationship(back_populates="habit")