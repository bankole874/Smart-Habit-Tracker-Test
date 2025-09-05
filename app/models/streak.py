from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from app.models.habit import Habit

class Streak(SQLModel, table=True):
    __tablename__ = "streaks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    habit_id: int = Field(foreign_key="habits.id")
    start_date: date
    end_date: Optional[date] = Field(default=None)
    longest: bool = Field(default=False)
    current: bool = Field(default=False)
    
    # Relationships - use string reference
    habit: "Habit" = Relationship(back_populates="streaks")