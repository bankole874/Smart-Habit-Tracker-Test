# app/routers/reminders.py
from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderResponse
from app.services.reminder_service import ReminderService
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/habits", tags=["Reminders"])

@router.post("/{habit_id}/reminders", response_model=ReminderResponse)
async def create_reminder(
    habit_id: int,
    reminder_data: ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Add reminder to habit"""
    return ReminderService.create_reminder(db, habit_id, reminder_data, current_user)

@router.get("/{habit_id}/reminders", response_model=List[ReminderResponse])
async def get_habit_reminders(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get all reminders for habit"""
    return ReminderService.get_habit_reminders(db, habit_id, current_user)

# Separate router for reminder-specific endpoints
reminder_router = APIRouter(prefix="/reminders", tags=["Reminders"])

@reminder_router.put("/{reminder_id}", response_model=ReminderResponse)
async def update_reminder(
    reminder_id: int,
    reminder_data: ReminderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Update reminder"""
    return ReminderService.update_reminder(db, reminder_id, reminder_data, current_user)

@reminder_router.delete("/{reminder_id}")
async def delete_reminder(
    reminder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Delete reminder"""
    ReminderService.delete_reminder(db, reminder_id, current_user)
    return {"message": "Reminder deleted successfully"}
