from fastapi import APIRouter
from src.core.response import BaseResponse, success_response, error_response
from datetime import datetime
from src.services.health.health_check import health_checker, HealthCheckModel

router = APIRouter(prefix="/health", tags=["Health Check"])


@router.get(
    "/",
    summary="Health Check Endpoint",
    description="Check the health status of the API",
    response_model=BaseResponse[HealthCheckModel],
    responses={
        200: {
            "description": "Service health status",
            "content": {
                "application/json": {
                    "example": {
                        "status": True,
                        "status_code": 200,
                        "message": "API is healthy",
                        "data": {
                            "status": "healthy",
                            "timestamp": "2023-01-01T00:00:00Z",
                            "checks": {
                                "database": {
                                    "status": "healthy",
                                    "details": {
                                        "message": "Database connection successful",
                                        "result": 1,
                                    },
                                }
                            },
                        },
                    }
                }
            },
        },
        503: {
            "description": "Service is unhealthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": False,
                        "status_code": 503,
                        "message": "Service is unavailable",
                        "data": {
                            "status": "unhealthy",
                            "timestamp": "2023-01-01T00:00:00Z",
                            "checks": {
                                "database": {
                                    "status": "unhealthy",
                                    "error": "Database connection failed: connection refused",
                                    "details": None,
                                }
                            },
                        },
                    }
                }
            },
        },
    },
)
async def health_check():
    health_data = await health_checker.perform_checks()
    if health_data["status"] == "healthy":
        return success_response(data=health_data, message="API is healthy")
    else:
        return error_response(
            data=health_data, message="API is experiencing issues", status_code=503
        )
