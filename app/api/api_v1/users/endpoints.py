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


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(depends.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(depends.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_all(db, skip=skip, limit=limit)
    return users


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


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(depends.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(depends.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user