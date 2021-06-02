from typing import Generator

from fastapi import Depends, HTTPException, status
from starlette import status

from app import crud, models
from app.core.messages import INACTIVE_USER, NOT_ENOUGH_PRIVILEGES
from app.db.session import SessionLocal

from .security.authentication import get_current_user_authorizer


# Dependency to get DB session.
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_active_user(
    current_user: models.User = Depends(get_current_user_authorizer()),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail=INACTIVE_USER)
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user_authorizer()),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=NOT_ENOUGH_PRIVILEGES,
        )
    return current_user
