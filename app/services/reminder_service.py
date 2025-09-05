# app/services/reminder_service.py
from typing import List
from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.reminder import Reminder
from app.models.user import User
from app.schemas.reminder import ReminderCreate, ReminderUpdate
from app.services.habit_service import HabitService

class ReminderService:
    @staticmethod
    def create_reminder(db: Session, habit_id: int, reminder_data: ReminderCreate, user: User) -> Reminder:
        """Create reminder for habit"""
        HabitService.get_habit_by_id(db, habit_id, user)
        
        reminder = Reminder(**reminder_data.model_dump(), habit_id=habit_id)
        db.add(reminder)
        db.commit()
        db.refresh(reminder)
        return reminder
    
    @staticmethod
    def get_habit_reminders(db: Session, habit_id: int, user: User) -> List[Reminder]:
        """Get all reminders for a habit"""
        HabitService.get_habit_by_id(db, habit_id, user)
        
        statement = select(Reminder).where(Reminder.habit_id == habit_id)
        return db.exec(statement).all()
    
    @staticmethod
    def get_reminder_by_id(db: Session, reminder_id: int, user: User) -> Reminder:
        """Get reminder by ID with ownership check"""
        statement = select(Reminder).join(
            Habit, Reminder.habit_id == Habit.id
        ).where(
            (Reminder.id == reminder_id) & (Habit.user_id == user.id)
        )
        reminder = db.exec(statement).first()
        
        if not reminder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reminder not found"
            )
        return reminder
    
    @staticmethod
    def update_reminder(db: Session, reminder_id: int, reminder_data: ReminderUpdate, user: User) -> Reminder:
        """Update reminder"""
        reminder = ReminderService.get_reminder_by_id(db, reminder_id, user)
        
        update_data = reminder_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(reminder, key, value)
        
        db.add(reminder)
        db.commit()
        db.refresh(reminder)
        return reminder
    
    @staticmethod
    def delete_reminder(db: Session, reminder_id: int, user: User):
        """Delete reminder"""
        reminder = ReminderService.get_reminder_by_id(db, reminder_id, user)
        db.delete(reminder)
        db.commit()
