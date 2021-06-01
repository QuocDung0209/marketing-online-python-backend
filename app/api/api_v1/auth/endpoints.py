from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.api_v1.auth.model import UserLoginIn, UserLoginOut
from app.core import depends

from .service import login as login_service

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
