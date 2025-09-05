# app/schemas/reminder.py
from pydantic import BaseModel
from typing import Optional
from datetime import time

class ReminderBase(BaseModel):
    reminder_time: time
    enabled: bool = True

class ReminderCreate(ReminderBase):
    pass

class ReminderUpdate(BaseModel):
    reminder_time: Optional[time] = None
    enabled: Optional[bool] = None

class ReminderResponse(ReminderBase):
    id: int
    habit_id: int
    
    class Config:
        from_attributes = True
