
from datetime import datetime, timedelta, timezone
from http.client import HTTPException
from typing import Literal

from fastapi import HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt

from app.config import settings


def _create_token(
    data: dict,
    expires_delta: timedelta,
    token_type: Literal["access", "refresh"],
) -> str:
    to_encode = data.copy()
    to_encode.update({
        "exp": datetime.now(timezone.utc) + expires_delta,
        "type": token_type,
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


def create_access_token(data: dict) -> str:
    return _create_token(data, timedelta(minutes=15), "access")


def create_refresh_token(data: dict) -> str:
    return _create_token(data, timedelta(days=7), "refresh")


def decode_token(
    token: str,
    expected_type: Literal["access", "refresh"] = "access",
) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    if payload.get("type") != expected_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Expected {expected_type} token",
        )

    return payload
