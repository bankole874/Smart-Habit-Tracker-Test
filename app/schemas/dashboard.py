# app/schemas/dashboard.py
from pydantic import BaseModel
from typing import List, Dict
from datetime import date

class DashboardOverview(BaseModel):
    total_habits: int
    completed_today: int
    active_streaks: int
    completion_percentage: float

class HabitStatistics(BaseModel):
    habit_id: int
    habit_name: str
    success_rate: float
    current_streak: int
    longest_streak: int
    total_completions: int

class DashboardStatistics(BaseModel):
    weekly_completion_rate: float
    monthly_completion_rate: float
    habits_statistics: List[HabitStatistics]

class CalendarEntry(BaseModel):
    date: date
    completed_habits: int
    total_habits: int

class MonthlyCalendar(BaseModel):
    month: int
    year: int
    entries: List[CalendarEntry]
