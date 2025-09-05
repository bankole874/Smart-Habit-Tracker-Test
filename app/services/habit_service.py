# app/services/habit_service.py
from typing import List
from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.habit import Habit
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitUpdate

class HabitService:
    @staticmethod
    def create_habit(db: Session, habit_data: HabitCreate, user: User) -> Habit:
        """Create new habit"""
        habit = Habit(**habit_data.model_dump(), user_id=user.id)
        db.add(habit)
        db.commit()
        db.refresh(habit)
        return habit
    
    @staticmethod
    def get_user_habits(db: Session, user: User) -> List[Habit]:
        """Get all habits for user"""
        statement = select(Habit).where(
            (Habit.user_id == user.id) & (Habit.archived == False)
        )
        return db.exec(statement).all()
    
    @staticmethod
    def get_habit_by_id(db: Session, habit_id: int, user: User) -> Habit:
        """Get habit by ID with ownership check"""
        statement = select(Habit).where(
            (Habit.id == habit_id) & (Habit.user_id == user.id)
        )
        habit = db.exec(statement).first()
        
        if not habit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Habit not found"
            )
        return habit
    
    @staticmethod
    def update_habit(db: Session, habit_id: int, habit_data: HabitUpdate, user: User) -> Habit:
        """Update habit"""
        habit = HabitService.get_habit_by_id(db, habit_id, user)
        
        update_data = habit_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(habit, key, value)
        
        db.add(habit)
        db.commit()
        db.refresh(habit)
        return habit
    
    @staticmethod
    def delete_habit(db: Session, habit_id: int, user: User):
        """Delete habit"""
        habit = HabitService.get_habit_by_id(db, habit_id, user)
        db.delete(habit)
        db.commit()
    
    @staticmethod
    def archive_habit(db: Session, habit_id: int, user: User) -> Habit:
        """Archive habit (soft delete)"""
        habit = HabitService.get_habit_by_id(db, habit_id, user)
        habit.archived = True
        db.add(habit)
        db.commit()
        db.refresh(habit)
        return habit
