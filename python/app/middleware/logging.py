"""
Request/Response logging middleware for better observability
"""
import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log requests and responses for better observability"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Start timer
        start_time = time.time()
        
        # Extract request info
        method = request.method
        url = str(request.url)
        user_agent = request.headers.get("user-agent", "")
        client_ip = self._get_client_ip(request)
        
        # Log request
        logger.info(f"Request: {method} {url} - IP: {client_ip} - User-Agent: {user_agent}")
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate response time
            process_time = time.time() - start_time
            
            # Log response
            logger.info(
                f"Response: {method} {url} - Status: {response.status_code} - "
                f"Time: {process_time:.3f}s - IP: {client_ip}"
            )
            
            # Add response time header
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as exc:
            # Calculate error response time
            process_time = time.time() - start_time
            
            # Log error
            logger.error(
                f"Error: {method} {url} - Exception: {str(exc)} - "
                f"Time: {process_time:.3f}s - IP: {client_ip}",
                exc_info=True
            )
            
            # Re-raise exception to be handled by error handlers
            raise exc
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address from request headers"""
        # Check for forwarded headers (for reverse proxy setups)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to direct client IP
        if hasattr(request, "client") and request.client:
            return request.client.host
        
        return "unknown"