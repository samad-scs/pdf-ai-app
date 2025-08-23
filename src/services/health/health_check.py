# src/utils/health_check.py
from datetime import datetime
from typing import Dict, Any, List, Callable
import logging
import asyncio

logger = logging.getLogger(__name__)


class HealthChecker:
    def __init__(self):
        self.checks = []

    def add_check(self, name: str, check_function: Callable):
        """Add a health check function"""
        self.checks.append((name, check_function))
        logger.info(f"Registered health check: {name}")

    async def perform_checks(self) -> Dict[str, Any]:
        """Perform all registered health checks"""
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
                logger.debug(f"Health check passed: {name}")
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


health_checker.add_check("application", basic_app_check)
