from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.db import User as UserDB

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    return {"status": "healthy"}


@router.get("/info")
async def app_info():
    from ..config import get_settings

    settings = get_settings()
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
