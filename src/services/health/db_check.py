# src/utils/database_health.py
from .health_check import health_checker
from src.core.database import AsyncSessionLocal  # Adjust import based on your setup
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)


async def check_database_connection():
    """Check if database connection is working"""
    try:
        async with AsyncSessionLocal() as session:
            # Execute a simple query to check connection
            result = await session.execute(text("SELECT 1"))
            return {
                "message": "Database connection successful",
                "result": result.scalar(),
            }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        raise Exception(f"Database connection failed: {str(e)}")
