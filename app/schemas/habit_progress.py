# app/schemas/habit_progress.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class HabitProgressBase(BaseModel):
    date: date
    completed: bool = False
    note: Optional[str] = None

class HabitProgressCreate(HabitProgressBase):
    pass

class HabitProgressUpdate(BaseModel):
    completed: Optional[bool] = None
    note: Optional[str] = None

class HabitProgressResponse(HabitProgressBase):
    id: int
    habit_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True