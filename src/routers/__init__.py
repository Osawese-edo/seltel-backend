from fastapi import APIRouter

from .products import router as products_router
from .users import router as users_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(products_router)
api_router.include_router(users_router)
