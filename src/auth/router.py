from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import create_access_token, hash_password, verify_password
from .dependencies import get_current_active_user
from ..database import get_db
from ..models.db import User as UserDB
from ..models.user import Token, User, UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=Token, tags=["Auth"])
async def signup(user: UserCreate = Body(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserDB).where(UserDB.email == user.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    if user.password != user.password_confirmation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    hashed = hash_password(user.password)
    new_user = UserDB(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed,
        disabled=False,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = create_access_token(user.email)
    return Token(access_token=token)


@router.post("/login", response_model=Token, tags=["Auth"])
async def login(
    email: EmailStr = Body(...),
    password: str = Body(...),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UserDB).where(UserDB.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(user.email)
    return Token(access_token=token)


@router.get("/me", response_model=User, tags=["Auth"])
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user
