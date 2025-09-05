# app/schemas/habit.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time
from app.models.habit import FrequencyType

class HabitBase(BaseModel):
    name: str
    description: Optional[str] = None
    frequency: FrequencyType = FrequencyType.DAILY
    reminder_time: Optional[time] = None

class HabitCreate(HabitBase):
    pass

class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[FrequencyType] = None
    reminder_time: Optional[time] = None

class HabitResponse(HabitBase):
    id: int
    user_id: int
    created_at: datetime
    archived: bool
    
    class Config:
        from_attributes = True