from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import depends
from app.core.messages import NOT_ENOUGH_PRIVILEGES

from .service import create_user as create_user_service

router = APIRouter()


@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    db: Session = Depends(depends.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(depends.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    return await create_user_service(db, user_in)
