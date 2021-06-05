from typing import Any

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1.auth.model import UserLoginIn, UserLoginOut
from app.core import depends
from app.schemas.message import Message

from .service import login as login_service
from .service import recover_password as recover_password_service
from .service import reset_password as reset_password_service

router = APIRouter()


@router.post("/login", response_model=UserLoginOut)
async def login(
    *,
    db: AsyncSession = Depends(depends.get_session),
    user_login: UserLoginIn,
) -> Any:
    """
    Get an access token for future requests
    """
    return await login_service(db, user_login)


@router.post("/password-recovery/{email}", response_model=Message)
async def recover_password(
    email: str, db: AsyncSession = Depends(depends.get_session)
) -> Any:
    """
    Password Recovery will send an email for user to reset password.
    """
    return await recover_password_service(db, email)


@router.post("/reset-password/", response_model=Message)
async def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: AsyncSession = Depends(depends.get_session),
) -> Any:
    """
    Reset password
    """
    return await reset_password_service(db, token, new_password)
