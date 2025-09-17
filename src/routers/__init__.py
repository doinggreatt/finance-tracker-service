from fastapi import APIRouter

from .users import router as user_router
from .finances import router as finance_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(user_router)
api_router.include_router(finance_router)