from typing import Any, Dict, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.base import get_password_hash, verify_password
from app.crud.base import BaseActions
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(BaseActions[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        query = select(User).filter(User.email == email)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_username(
        self, db: AsyncSession, *, username: str
    ) -> Optional[User]:
        query = select(User).filter(User.username == username)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_email_or_username(
        self, db: AsyncSession, *, email_or_username: str
    ) -> Optional[User]:
        query = select(User).filter(
            (User.email == email_or_username) | (User.username == email_or_username)
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(
        self, db: AsyncSession, *, email_or_username: str, password: str
    ) -> Optional[User]:
        user = await self.get_by_email_or_username(
            db, email_or_username=email_or_username
        )
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
