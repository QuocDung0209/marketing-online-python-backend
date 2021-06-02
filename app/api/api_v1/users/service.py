from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.core.messages import USER_NOT_EXISTS
from app.utils import send_new_account_email


async def create_user(db: Session, user_in: schemas.UserCreate):
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail=USER_NOT_EXISTS,
        )
    user = crud.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        await send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user
