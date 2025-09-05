# app/middleware/rate_limiting.py
from fastapi import Request, HTTPException, status
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import redis

# Redis connection for rate limiting (optional)
# redis_client = redis.Redis(host='localhost', port=6379, db=0)

limiter = Limiter(key_func=get_remote_address)

# Rate limit decorator for different endpoints
auth_rate_limit = limiter.limit("5/minute")  # Auth endpoints
api_rate_limit = limiter.limit("100/minute")  # General API endpoints
