# src/utils/__init__.py
"""
Utility modules initialization - ensures health checks are registered
"""
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import health checker
from .health_check import health_checker


# Register basic application check
async def basic_app_check():
    """Basic application health check"""
    return {"message": "Application is running"}


health_checker.add_check("application", basic_app_check)

# Try to register database health check
try:
    from .db_check import check_database_connection

    health_checker.add_check("database", check_database_connection)

except ImportError as e:
    logger.warning(f"Could not register database health check: {e}")

    # Add a placeholder database check
    async def database_not_configured():
        return {"message": "Database not configured", "configured": False}

    health_checker.add_check("database", database_not_configured)
