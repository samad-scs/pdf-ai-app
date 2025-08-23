from fastapi import APIRouter
from src.core.response import BaseResponse
from src.services.auth.tokens import create_access_token, get_user
from src.core.response import error_response
import logging
from pydantic import BaseModel


logger = logging.getLogger(__name__)


router = APIRouter(tags=["Authentication"])


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post(
    "/login",
    summary="User Login",
    description="Authenticate user and return a token",
    response_model=BaseResponse,
    responses={
        200: {
            "description": "Login successful",
            "content": {
                "application/json": {
                    "example": {
                        "status": True,
                        "status_code": 200,
                        "message": "Login successful",
                        "data": {"token": "fake-jwt-token"},
                    }
                }
            },
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "status": False,
                        "status_code": 422,
                        "message": "Validation Error",
                        "data": {
                            "detail": [
                                {
                                    "loc": ["body", "username"],
                                    "msg": "field required",
                                    "type": "value_error.missing",
                                }
                            ]
                        },
                    }
                }
            },
        },
        401: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {
                        "status": False,
                        "status_code": 401,
                        "message": "Invalid credentials",
                        "data": None,
                    }
                },
            },
        },
    },
)
async def login(body: LoginRequest):
    user = await get_user(body.email)
    logger.info(f"Attempting login for user {body.email}")
    logger.info(f"User fetched from DB: {user}")
    if not user:
        return error_response(message="Invalid credentials", status_code=401, data=None)
    token = create_access_token({"email": body.email})
    logger.info(f"Token {token} generated for user {body.email}")

    logger.info(f"User {body.email} logged in successfully")
    return {
        "status": True,
        "status_code": 200,
        "message": "Login successful",
        "data": {"token": "fake-jwt-token"},
    }
