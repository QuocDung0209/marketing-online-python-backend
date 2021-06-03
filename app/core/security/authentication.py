from typing import Callable, Generator, Optional

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from starlette import requests, status
from starlette.exceptions import HTTPException as StarletteHTTPException

from app import crud
from app.core.config import settings
from app.db.session import SessionLocal

from .jwt import get_user_id_from_token

HEADER_KEY = "Authorization"


# Dependency to get DB session.
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class RWAPIKeyHeader(APIKeyHeader):
    # noqa: WPS610
    async def __call__(
        self,
        request: requests.Request,
    ) -> Optional[str]:
        try:
            return await super().__call__(request)
        except StarletteHTTPException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
            )


def _get_authorization_header(
    api_key: str = Security(RWAPIKeyHeader(name=HEADER_KEY)),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unsupported authorization type",
        )

    if token_prefix != settings.TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unsupported authorization type",
        )

    return token


def _get_authorization_header_optional(
    authorization: Optional[str] = Security(
        RWAPIKeyHeader(name=HEADER_KEY, auto_error=False)
    )
) -> str:
    if authorization:
        return _get_authorization_header(authorization)

    return ""


def _get_authorization_header_retriever(
    *,
    required: bool = True,
) -> Callable:  # type: ignore
    return _get_authorization_header if required else _get_authorization_header_optional


async def _get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(_get_authorization_header_retriever()),
) -> Optional[str]:
    try:
        user_id = get_user_id_from_token(token, settings.SECRET_KEY)
        user = crud.user.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token's user not exists in system.",
            )
        return user
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


async def _get_current_user_optional(
    token: str = Depends(_get_authorization_header_retriever(required=False)),
) -> Optional[str]:
    if token:
        return await _get_current_user(token)

    return None


def get_current_user_authorizer(*, required: bool = True) -> Callable:  # type: ignore
    return _get_current_user if required else _get_current_user_optional
