from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt

from ..config import get_settings
from . import get_pwd_context

settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_pwd_context().verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return get_pwd_context().hash(password)


def create_access_token(data: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    payload = {"sub": data, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None
