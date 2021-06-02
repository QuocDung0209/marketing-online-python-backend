from fastapi import APIRouter

from .auth.endpoints import router as auth
from .users.endpoints import router as user

api_router = APIRouter()

api_router.include_router(auth, prefix="/auth", tags=["auth"])
api_router.include_router(user, prefix="/user", tags=["user"])
