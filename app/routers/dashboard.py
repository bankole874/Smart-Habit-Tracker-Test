# app/routers/dashboard.py
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.schemas.dashboard import DashboardOverview, DashboardStatistics, MonthlyCalendar
from app.services.dashboard_service import DashboardService
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/overview", response_model=DashboardOverview)
async def get_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get dashboard overview"""
    return DashboardService.get_overview(db, current_user)

@router.get("/statistics", response_model=DashboardStatistics)
async def get_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get detailed statistics"""
    return DashboardService.get_statistics(db, current_user)

@router.get("/calendar/{year}/{month}", response_model=MonthlyCalendar)
async def get_monthly_calendar(
    year: int,
    month: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get monthly calendar view"""
    return DashboardService.get_monthly_calendar(db, current_user, month, year)
