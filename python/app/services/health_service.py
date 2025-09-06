"""
Enhanced health check service with system monitoring
"""
import time
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.connection import get_db
from app.schemas.responses import HealthCheckResponse

logger = logging.getLogger(__name__)

class HealthCheckService:
    """Service for comprehensive health monitoring"""
    
    def __init__(self):
        self.start_time = time.time()
    
    async def get_health_status(self) -> HealthCheckResponse:
        """Get comprehensive health status"""
        try:
            # Basic health info
            current_time = datetime.utcnow().isoformat()
            uptime = time.time() - self.start_time
            
            # Check database connectivity
            db_status = await self._check_database_health()
            
            # Check external dependencies
            dependencies = await self._check_dependencies()
            
            # Determine overall status
            overall_status = "healthy" if db_status == "connected" else "unhealthy"
            
            return HealthCheckResponse(
                status=overall_status,
                timestamp=current_time,
                version="1.0.0",
                uptime=uptime,
                database=db_status,
                dependencies=dependencies
            )
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return HealthCheckResponse(
                status="unhealthy",
                timestamp=datetime.utcnow().isoformat(),
                version="1.0.0",
                uptime=time.time() - self.start_time,
                database="error",
                dependencies={"error": str(e)}
            )
    
    async def _check_database_health(self) -> str:
        """Check database connectivity"""
        try:
            # Use dependency injection to get database session
            db_gen = get_db()
            db = next(db_gen)
            
            # Execute simple query
            result = db.execute(text("SELECT 1"))
            result.fetchone()
            
            return "connected"
            
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return "disconnected"
        finally:
            try:
                db.close()
            except:
                pass
    
    async def _check_dependencies(self) -> dict:
        """Check status of external dependencies"""
        dependencies = {}
        
        # Check Twilio (if configured)
        try:
            from app.core.config import settings
            if settings.twilio_account_sid and settings.twilio_auth_token:
                dependencies["twilio"] = "configured"
            else:
                dependencies["twilio"] = "not_configured"
        except Exception as e:
            dependencies["twilio"] = f"error: {str(e)}"
        
        return dependencies

# Global health check service instance
health_service = HealthCheckService()