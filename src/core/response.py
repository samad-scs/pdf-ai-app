# src/core/response.py
from fastapi import status
from typing import Any, Optional
from pydantic import BaseModel, Field
from typing import TypeVar, Generic

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    status: bool = Field(..., description="Indicates if the request was successful")
    status_code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Human-readable message")
    data: Optional[T] = Field(None, description="Response data payload")


def success_response(
    data: Any = None, message: str = "Success", status_code: int = status.HTTP_200_OK
) -> BaseResponse:
    return BaseResponse(
        status=True, status_code=status_code, message=message, data=data
    )


def error_response(
    data: Any = None,
    message: str = "Error occurred",
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> BaseResponse:
    return BaseResponse(
        status=False, status_code=status_code, message=message, data=data
    )


def unauthorized_response(
    message: str = "Unauthorized", data: Any = None
) -> BaseResponse:
    return error_response(
        data=data, message=message, status_code=status.HTTP_401_UNAUTHORIZED
    )
