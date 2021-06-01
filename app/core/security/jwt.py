from datetime import datetime, timedelta
from typing import Any, Dict, Union

from jose import jwt

from app.core.config import settings
from app.schemas.jwt import JWTMeta, JWTUser

ALGORITHM = "HS256"


def create_jwt_token(
    *,
    jwt_content: Dict[str, str],
    secret_key: str,
    expires_delta: timedelta = None,
    subject: str
) -> str:
    to_encode = jwt_content.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update(JWTMeta(exp=expire, sub=subject))
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(
    jwt_user: JWTUser, subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    return create_jwt_token(
        jwt_content=jwt_user.dict(),
        secret_key=settings.SECRET_KEY,
        expires_delta=expires_delta,
        subject=str(subject),
    )
