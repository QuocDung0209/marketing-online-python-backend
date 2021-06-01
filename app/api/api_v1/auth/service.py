from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.api_v1.auth.model import UserLoginIn, UserLoginOut
from app.core import security
from app.core.config import settings
from app.core.messages import INACTIVE_USER, INVALID_ACCOUNT
from app.schemas.jwt import JWTUser


def login(db: Session, user_login: UserLoginIn):
    user = crud.user.authenticate(
        db, email_or_username=user_login.user, password=user_login.password
    )
    if not user:
        raise HTTPException(status_code=400, detail=INVALID_ACCOUNT)
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail=INACTIVE_USER)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        JWTUser(id=user.id, username=user.username),
        user.id,
        expires_delta=access_token_expires,
    )
    return UserLoginOut(
        username=user.username,
        access_token=access_token,
        token_type=settings.TOKEN_TYPE,
    )
