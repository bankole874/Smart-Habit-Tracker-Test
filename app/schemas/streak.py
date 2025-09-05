# app/schemas/streak.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

class StreakResponse(BaseModel):
    id: int
    habit_id: int
    start_date: date
    end_date: Optional[date] = None
    longest: bool
    current: bool
    
    class Config:
        from_attributes = True