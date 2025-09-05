from typing import List
from datetime import date
from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.habit_progress import HabitProgress
from app.models.user import User
from app.schemas.habit_progress import HabitProgressCreate, HabitProgressUpdate
from app.services.habit_service import HabitService

class ProgressService:
    @staticmethod
    def create_or_update_progress(
        db: Session, 
        habit_id: int, 
        progress_data: HabitProgressCreate, 
        user: User
    ) -> HabitProgress:
        """Create or update progress entry"""
        # Verify habit ownership
        HabitService.get_habit_by_id(db, habit_id, user)
        
        # Check if progress already exists
        statement = select(HabitProgress).where(
            (HabitProgress.habit_id == habit_id) & 
            (HabitProgress.date == progress_data.date)
        )
        existing_progress = db.exec(statement).first()
        
        if existing_progress:
            # Update existing
            update_data = progress_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(existing_progress, key, value)
            db.add(existing_progress)
            db.commit()
            db.refresh(existing_progress)
            return existing_progress
        else:
            # Create new
            progress = HabitProgress(**progress_data.model_dump(), habit_id=habit_id)
            db.add(progress)
            db.commit()
            db.refresh(progress)
            return progress
    
    @staticmethod
    def get_habit_progress(db: Session, habit_id: int, user: User) -> List[HabitProgress]:
        """Get all progress entries for a habit"""
        HabitService.get_habit_by_id(db, habit_id, user)
        
        statement = select(HabitProgress).where(HabitProgress.habit_id == habit_id)
        return db.exec(statement).all()
    
    @staticmethod
    def get_progress_by_date(
        db: Session, 
        habit_id: int, 
        target_date: date, 
        user: User
    ) -> HabitProgress:
        """Get progress for specific date"""
        HabitService.get_habit_by_id(db, habit_id, user)
        
        statement = select(HabitProgress).where(
            (HabitProgress.habit_id == habit_id) & 
            (HabitProgress.date == target_date)
        )
        progress = db.exec(statement).first()
        
        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Progress entry not found"
            )
        return progress
