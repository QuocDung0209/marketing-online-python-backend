from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from jose import jwt
from pydantic import ValidationError

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


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def get_user_from_token(token: str, secret_key: str) -> JWTUser:
    try:
        return JWTUser(**jwt.decode(token, secret_key, algorithms=[ALGORITHM]))
    except jwt.JWTError as decode_error:
        raise ValueError("Unable to decode JWT token") from decode_error
    except ValidationError as validation_error:
        raise ValueError("Malformed payload in token") from validation_error


def get_user_id_from_token(token: str, secret_key: str) -> int:
    return get_user_from_token(token, secret_key).id


def get_username_from_token(token: str, secret_key: str) -> str:
    return get_user_from_token(token, secret_key).username


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token["email"]
    except jwt.JWTError:
        return None
