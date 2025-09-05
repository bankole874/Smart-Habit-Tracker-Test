# app/middleware/logging.py
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request details
        client_ip = request.client.host
        method = request.method
        url = str(request.url)
        
        logger.info(f"Request: {method} {url} from {client_ip}")
        
        response = await call_next(request)
        
        # Log response details
        logger.info(f"Response: {response.status_code}")
        
        return response
