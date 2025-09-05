# Project Structure:
# habit_tracker/
# ├── app/
# │   ├── __init__.py
# │   ├── main.py
# │   ├── config.py
# │   ├── database.py
# │   ├── models/
# │   │   ├── __init__.py
# │   │   ├── user.py
# │   │   ├── habit.py
# │   │   ├── habit_progress.py
# │   │   ├── streak.py
# │   │   └── reminder.py
# │   ├── schemas/
# │   │   ├── __init__.py
# │   │   ├── user.py
# │   │   ├── habit.py
# │   │   ├── habit_progress.py
# │   │   ├── streak.py
# │   │   └── auth.py
# │   ├── routers/
# │   │   ├── __init__.py
# │   │   ├── auth.py
# │   │   ├── habits.py
# │   │   ├── progress.py
# │   │   ├── streaks.py
# │   │   ├── dashboard.py
# │   │   └── reminders.py
# │   ├── services/
# │   │   ├── __init__.py
# │   │   ├── auth_service.py
# │   │   ├── habit_service.py
# │   │   ├── progress_service.py
# │   │   └── streak_service.py
# │   ├── utils/
# │   │   ├── __init__.py
# │   │   ├── security.py
# │   │   └── dependencies.py
# │   └── middleware/
# │       ├── __init__.py
# │       └── logging.py
# ├── requirements.txt
# ├── .env
# └── alembic/