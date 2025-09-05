# Updated app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.database import create_db_and_tables
from app.routers import auth, habits, progress, streaks, dashboard, reminders
from app.middleware.logging import LoggingMiddleware

# Create rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title="Smart Habit Tracker API",
    description="A comprehensive habit tracking backend API with authentication, progress tracking, streaks, and analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add middleware
app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Configure for your mobile app
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth.router)
app.include_router(habits.router)
app.include_router(progress.router)
app.include_router(streaks.router)
app.include_router(dashboard.router)
app.include_router(reminders.router)
app.include_router(reminders.reminder_router)

@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    create_db_and_tables()

@app.get("/")
async def root():
    """API health check"""
    return {
        "message": "Smart Habit Tracker API is running!",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}
