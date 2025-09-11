from fastapi import APIRouter

from .users import router as user_router

api_router = APIRouter(prefix="/finance/api/v1")
api_router.include_router(user_router)