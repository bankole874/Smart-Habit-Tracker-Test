# app/services/dashboard_service.py
from typing import List
from datetime import date, timedelta, datetime
from sqlmodel import Session, select, func
from app.models.habit import Habit
from app.models.habit_progress import HabitProgress
from app.models.user import User
from app.schemas.dashboard import DashboardOverview, DashboardStatistics, HabitStatistics, MonthlyCalendar, CalendarEntry
from app.services.streak_service import StreakService

class DashboardService:
    @staticmethod
    def get_overview(db: Session, user: User) -> DashboardOverview:
        """Get dashboard overview"""
        # Total active habits
        total_habits_stmt = select(func.count(Habit.id)).where(
            (Habit.user_id == user.id) & (Habit.archived == False)
        )
        total_habits = db.exec(total_habits_stmt).first() or 0
        
        # Completed today
        today = date.today()
        completed_today_stmt = select(func.count(HabitProgress.id)).join(
            Habit, HabitProgress.habit_id == Habit.id
        ).where(
            (Habit.user_id == user.id) &
            (HabitProgress.date == today) &
            (HabitProgress.completed == True) &
            (Habit.archived == False)
        )
        completed_today = db.exec(completed_today_stmt).first() or 0
        
        # Active streaks (habits with current streak > 0)
        habits_stmt = select(Habit).where(
            (Habit.user_id == user.id) & (Habit.archived == False)
        )
        habits = db.exec(habits_stmt).all()
        
        active_streaks = 0
        for habit in habits:
            current_streak = StreakService.calculate_current_streak(db, habit.id, user)
            if current_streak > 0:
                active_streaks += 1
        
        # Completion percentage
        completion_percentage = (completed_today / total_habits * 100) if total_habits > 0 else 0
        
        return DashboardOverview(
            total_habits=total_habits,
            completed_today=completed_today,
            active_streaks=active_streaks,
            completion_percentage=round(completion_percentage, 1)
        )
    
    @staticmethod
    def get_statistics(db: Session, user: User) -> DashboardStatistics:
        """Get detailed statistics"""
        # Get all active habits
        habits_stmt = select(Habit).where(
            (Habit.user_id == user.id) & (Habit.archived == False)
        )
        habits = db.exec(habits_stmt).all()
        
        # Calculate weekly and monthly completion rates
        today = date.today()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Weekly completion rate
        weekly_total_stmt = select(func.count(HabitProgress.id)).join(
            Habit, HabitProgress.habit_id == Habit.id
        ).where(
            (Habit.user_id == user.id) &
            (HabitProgress.date >= week_ago) &
            (Habit.archived == False)
        )
        weekly_total = db.exec(weekly_total_stmt).first() or 0
        
        weekly_completed_stmt = select(func.count(HabitProgress.id)).join(
            Habit, HabitProgress.habit_id == Habit.id
        ).where(
            (Habit.user_id == user.id) &
            (HabitProgress.date >= week_ago) &
            (HabitProgress.completed == True) &
            (Habit.archived == False)
        )
        weekly_completed = db.exec(weekly_completed_stmt).first() or 0
        
        weekly_rate = (weekly_completed / weekly_total * 100) if weekly_total > 0 else 0
        
        # Monthly completion rate
        monthly_total_stmt = select(func.count(HabitProgress.id)).join(
            Habit, HabitProgress.habit_id == Habit.id
        ).where(
            (Habit.user_id == user.id) &
            (HabitProgress.date >= month_ago) &
            (Habit.archived == False)
        )
        monthly_total = db.exec(monthly_total_stmt).first() or 0
        
        monthly_completed_stmt = select(func.count(HabitProgress.id)).join(
            Habit, HabitProgress.habit_id == Habit.id
        ).where(
            (Habit.user_id == user.id) &
            (HabitProgress.date >= month_ago) &
            (HabitProgress.completed == True) &
            (Habit.archived == False)
        )
        monthly_completed = db.exec(monthly_completed_stmt).first() or 0
        
        monthly_rate = (monthly_completed / monthly_total * 100) if monthly_total > 0 else 0
        
        # Habit statistics
        habits_stats = []
        for habit in habits:
            # Total completions
            total_completions_stmt = select(func.count(HabitProgress.id)).where(
                (HabitProgress.habit_id == habit.id) &
                (HabitProgress.completed == True)
            )
            total_completions = db.exec(total_completions_stmt).first() or 0
            
            # Total progress entries
            total_entries_stmt = select(func.count(HabitProgress.id)).where(
                HabitProgress.habit_id == habit.id
            )
            total_entries = db.exec(total_entries_stmt).first() or 0
            
            # Success rate
            success_rate = (total_completions / total_entries * 100) if total_entries > 0 else 0
            
            # Streaks
            current_streak = StreakService.calculate_current_streak(db, habit.id, user)
            longest_streak = StreakService.calculate_longest_streak(db, habit.id, user)
            
            habits_stats.append(HabitStatistics(
                habit_id=habit.id,
                habit_name=habit.name,
                success_rate=round(success_rate, 1),
                current_streak=current_streak,
                longest_streak=longest_streak,
                total_completions=total_completions
            ))
        
        return DashboardStatistics(
            weekly_completion_rate=round(weekly_rate, 1),
            monthly_completion_rate=round(monthly_rate, 1),
            habits_statistics=habits_stats
        )
    
    @staticmethod
    def get_monthly_calendar(db: Session, user: User, month: int, year: int) -> MonthlyCalendar:
        """Get monthly calendar view"""
        # Get first and last day of month
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1)
        
        # Get all progress for the month
        progress_stmt = select(HabitProgress).join(
            Habit, HabitProgress.habit_id == Habit.id
        ).where(
            (Habit.user_id == user.id) &
            (HabitProgress.date >= first_day) &
            (HabitProgress.date <= last_day) &
            (Habit.archived == False)
        )
        progress_entries = db.exec(progress_stmt).all()
        
        # Get total active habits count
        total_habits_stmt = select(func.count(Habit.id)).where(
            (Habit.user_id == user.id) & (Habit.archived == False)
        )
        total_habits = db.exec(total_habits_stmt).first() or 0
        
        # Group by date
        calendar_entries = {}
        for progress in progress_entries:
            if progress.date not in calendar_entries:
                calendar_entries[progress.date] = {"completed": 0, "total": 0}
            
            calendar_entries[progress.date]["total"] += 1
            if progress.completed:
                calendar_entries[progress.date]["completed"] += 1
        
        # Create calendar entries for all days in month
        entries = []
        current_date = first_day
        while current_date <= last_day:
            day_data = calendar_entries.get(current_date, {"completed": 0, "total": 0})
            entries.append(CalendarEntry(
                date=current_date,
                completed_habits=day_data["completed"],
                total_habits=max(day_data["total"], total_habits)
            ))
            current_date += timedelta(days=1)
        
        return MonthlyCalendar(
            month=month,
            year=year,
            entries=entries
        )
