# app/routers/progress.py
from typing import List
from datetime import date
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.schemas.habit_progress import HabitProgressCreate, HabitProgressUpdate, HabitProgressResponse
from app.services.progress_service import ProgressService
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/habits", tags=["Progress"])

@router.post("/{habit_id}/progress", response_model=HabitProgressResponse)
async def create_progress(
    habit_id: int,
    progress_data: HabitProgressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Mark habit as done/undone for specific date"""
    return ProgressService.create_or_update_progress(db, habit_id, progress_data, current_user)

@router.get("/{habit_id}/progress", response_model=List[HabitProgressResponse])
async def get_habit_progress(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get all progress logs for habit"""
    return ProgressService.get_habit_progress(db, habit_id, current_user)

@router.get("/{habit_id}/progress/{target_date}", response_model=HabitProgressResponse)
async def get_progress_by_date(
    habit_id: int,
    target_date: date,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get progress for specific date"""
    return ProgressService.get_progress_by_date(db, habit_id, target_date, current_user)
