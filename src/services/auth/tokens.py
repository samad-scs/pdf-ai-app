from pydantic import BaseModel
from src.core.config import settings
from src.core.response import error_response, unauthorized_response
from datetime import datetime, timedelta, timezone
from src.models.user import User
from passlib.context import CryptContext
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.core.database import get_db
from .encryption import decrypt_data, encrypt_data
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = settings.SECRET_KEY


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class UnauthorizedResponse(BaseModel):
    status: bool = False
    status_code: int = 401
    message: str = "Unauthorized"
    data: None = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(email: str, db: AsyncSession = Depends(get_db)) -> User | None:
    logger.info(f"Fetching user with email: {email}")

    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalar_one_or_none()
    logger.info(f"User fetched: {user}")
    if user:
        return user
    return None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = encrypt_data(to_encode, SECRET_KEY)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db)
):
    try:
        payload = decrypt_data(token, SECRET_KEY)
        email = payload.get("sub")
        if email is None:
            raise unauthorized_response()
        token_data = TokenData(email=email)
    except Exception:
        raise unauthorized_response()
    user = get_user(email=token_data.email, db=db)
    if user is None:
        raise unauthorized_response()
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise error_response(message="Inactive user", status_code=400)
    return current_user


async def authenticate_user(email: str, password: str, db: AsyncSession) -> User | bool:
    user = await get_user(email, db=db)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user
