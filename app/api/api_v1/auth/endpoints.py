from typing import Any

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.api.api_v1.auth.model import UserLoginIn, UserLoginOut
from app.core import depends
from app.schemas.message import Message

from .service import login as login_service
from .service import recover_password as recover_password_service
from .service import reset_password as reset_password_service

router = APIRouter()


@router.post("/login", response_model=UserLoginOut)
def login(
    *,
    db: Session = Depends(depends.get_db),
    user_login: UserLoginIn,
) -> Any:
    """
    Get an access token for future requests
    """
    return login_service(db, user_login)


@router.post("/password-recovery/{email}", response_model=Message)
async def recover_password(email: str, db: Session = Depends(depends.get_db)) -> Any:
    """
    Password Recovery will send an email for user to reset password.
    """
    return await recover_password_service(db, email)


@router.post("/reset-password/", response_model=Message)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(depends.get_db),
) -> Any:
    """
    Reset password
    """
    return reset_password_service(db, token, new_password)
