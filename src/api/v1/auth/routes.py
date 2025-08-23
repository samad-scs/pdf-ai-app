from fastapi import APIRouter
from src.core.response import BaseResponse

router = APIRouter()

@router.post("/login", response_model=BaseResponse, tags=["Authentication"])
def login():
    return {"status": True, "status_code": 200, "message": "Login successful", "data": {"token": "fake-jwt-token"}}