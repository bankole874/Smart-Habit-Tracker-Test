# app/services/streak_service.py
from typing import List, Optional
from datetime import date, timedelta
from sqlmodel import Session, select, desc
from app.models.streak import Streak
from app.models.habit_progress import HabitProgress
from app.models.user import User
from app.services.habit_service import HabitService

class StreakService:
    @staticmethod
    def calculate_current_streak(db: Session, habit_id: int, user: User) -> int:
        """Calculate current streak for a habit"""
        HabitService.get_habit_by_id(db, habit_id, user)
        
        # Get progress entries ordered by date descending
        statement = select(HabitProgress).where(
            (HabitProgress.habit_id == habit_id) &
            (HabitProgress.completed == True)
        ).order_by(desc(HabitProgress.date))
        
        completed_dates = db.exec(statement).all()
        
        if not completed_dates:
            return 0
        
        # Calculate consecutive days from today backwards
        current_date = date.today()
        streak_count = 0
        
        for progress in completed_dates:
            if progress.date == current_date - timedelta(days=streak_count):
                streak_count += 1
            else:
                break
        
        return streak_count
    
    @staticmethod
    def calculate_longest_streak(db: Session, habit_id: int, user: User) -> int:
        """Calculate longest streak for a habit"""
        HabitService.get_habit_by_id(db, habit_id, user)
        
        statement = select(HabitProgress).where(
            (HabitProgress.habit_id == habit_id) &
            (HabitProgress.completed == True)
        ).order_by(HabitProgress.date)
        
        completed_dates = [p.date for p in db.exec(statement).all()]
        
        if not completed_dates:
            return 0
        
        max_streak = 0
        current_streak = 1
        
        for i in range(1, len(completed_dates)):
            if completed_dates[i] == completed_dates[i-1] + timedelta(days=1):
                current_streak += 1
            else:
                max_streak = max(max_streak, current_streak)
                current_streak = 1
        
        return max(max_streak, current_streak)
    
    @staticmethod
    def get_habit_streaks(db: Session, habit_id: int, user: User) -> List[Streak]:
        """Get all streaks for a habit"""
        HabitService.get_habit_by_id(db, habit_id, user)
        
        statement = select(Streak).where(Streak.habit_id == habit_id)
        return db.exec(statement).all()
    
    @staticmethod
    def update_streaks(db: Session, habit_id: int, user: User):
        """Update streak records for a habit"""
        current_streak_length = StreakService.calculate_current_streak(db, habit_id, user)
        longest_streak_length = StreakService.calculate_longest_streak(db, habit_id, user)
        
        # Update or create current streak record
        current_streak_stmt = select(Streak).where(
            (Streak.habit_id == habit_id) & (Streak.current == True)
        )
        current_streak = db.exec(current_streak_stmt).first()
        
        if current_streak_length > 0:
            if not current_streak:
                current_streak = Streak(
                    habit_id=habit_id,
                    start_date=date.today() - timedelta(days=current_streak_length-1),
                    current=True
                )
                db.add(current_streak)
            else:
                current_streak.end_date = None  # Still ongoing
        else:
            if current_streak:
                current_streak.current = False
                current_streak.end_date = date.today() - timedelta(days=1)
        
        # Update longest streak record
        longest_streak_stmt = select(Streak).where(
            (Streak.habit_id == habit_id) & (Streak.longest == True)
        )
        longest_streak = db.exec(longest_streak_stmt).first()
        
        if not longest_streak or longest_streak_length > (longest_streak.end_date - longest_streak.start_date).days + 1:
            if longest_streak:
                longest_streak.longest = False
            
            # Create new longest streak record
            new_longest = Streak(
                habit_id=habit_id,
                start_date=date.today() - timedelta(days=longest_streak_length-1),
                end_date=date.today(),
                longest=True
            )
            db.add(new_longest)
        
        db.commit()
