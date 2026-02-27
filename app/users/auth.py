from http.client import HTTPException

from argon2 import verify_password
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings
from app.users.dao import UserDAO
from app.users.models import User
from app.users.token import decode_token

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def get_password_hash(password: str) -> str:
    password = password.strip()
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    if not (user and verify_password(password, user.password_hash)):
        raise Exception("Invalid email or password")
    return user

async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = decode_token(token, expected_type="access")
        user_id = int(payload.get("sub"))
        user = await UserDAO.find_one_or_none(id=user_id)
        return user
    except Exception:
        return None
    
class AddUserToContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user = await get_current_user(request)
        response = await call_next(request)
        return response
    

async def get_user_from_session(request: Request):
    token = request.session.get("token")
    if not token:
        return None
    
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = int(payload.get("sub"))
        return await UserDAO.find_one_or_none(id=user_id)
    except JWTError:
        return None
    

async def admin_required(
    user: User = Depends(get_current_user),
) -> User:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user
