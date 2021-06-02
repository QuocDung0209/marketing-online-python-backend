from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import crud
from app.api.api_v1.auth.model import UserLoginIn, UserLoginOut
from app.core import security
from app.core.config import settings
from app.core.messages import (INACTIVE_USER, INVALID_ACCOUNT, INVALID_TOKEN,
                               USER_NOT_EXISTS)
from app.core.security.base import get_password_hash
from app.core.security.jwt import (generate_password_reset_token,
                                   verify_password_reset_token)
from app.schemas.jwt import JWTUser
from app.utils import send_reset_password_email


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


async def recover_password(db: Session, email: str):
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail=USER_NOT_EXISTS,
        )
    password_reset_token = generate_password_reset_token(email=email)
    await send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Password recovery email sent"},
    )


def reset_password(db: Session, token: str, new_password: str):
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail=INVALID_TOKEN)
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=USER_NOT_EXISTS,
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail=INACTIVE_USER)
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Password updated successfully"},
    )
