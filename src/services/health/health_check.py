# src/utils/health_check.py
from datetime import datetime
from typing import Dict, Any, Callable, Optional
import logging
import asyncio
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class HealthCheckDetails(BaseModel):
    """Details of a single health check"""

    status: str = Field(..., description="Health status: healthy/unhealthy")
    details: Optional[Dict[str, Any]] = Field(None, description="Check details")
    error: Optional[str] = Field(None, description="Error message if unhealthy")


class HealthCheckModel(BaseModel):
    status: str = Field(..., description="Overall health status: healthy/unhealthy")
    timestamp: str = Field(..., description="ISO timestamp of the check")
    checks: Dict[str, HealthCheckDetails] = Field(
        ..., description="Individual check results"
    )


class HealthChecker:
    def __init__(self):
        self.checks = []

    def add_check(self, name: str, check_function: Callable):
        """Add a health check function"""
        self.checks.append((name, check_function))

    async def perform_checks(self) -> HealthCheckModel:
        """Perform all registered health checks"""
        print(self.checks)
        results = {}
        overall_status = True

        if not self.checks:
            logger.warning("No health checks registered")
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "checks": {"warning": "No health checks configured"},
            }

        for name, check_func in self.checks:
            try:
                # Check if the function is async or sync
                if asyncio.iscoroutinefunction(check_func):
                    result = await check_func()
                else:
                    result = check_func()

                results[name] = {"status": "healthy", "details": result}

            except Exception as e:
                logger.error(f"Health check failed for {name}: {str(e)}")
                results[name] = {
                    "status": "unhealthy",
                    "error": str(e),
                    "details": None,
                }
                overall_status = False

        return {
            "status": "healthy" if overall_status else "unhealthy",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "checks": results,
        }


# Create a global health checker instance
health_checker = HealthChecker()


# Add a basic check to ensure we always have at least one check
async def basic_app_check():
    """Basic application health check"""
    return {"message": "Application is running"}
