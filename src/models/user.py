from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    full_name: Optional[str] = Field(None, max_length=200, description="User full name")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128, description="User password")
    password_confirmation: str = Field(..., min_length=8, max_length=128)


class User(UserBase):
    id: int
    disabled: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserInDB(UserBase):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
