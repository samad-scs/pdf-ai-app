# api/v1/__init__.py
from fastapi import APIRouter
from .auth.routes import router as auth_router
from src.core.response import BaseResponse

router = APIRouter(prefix="/v1")
router.include_router(auth_router)
