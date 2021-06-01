from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class JWTMeta(BaseModel):
    exp: datetime
    sub: str


class User(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None


class JWTUser(User):
    pass

    def is_public_user(self):
        return self.username == "public"
