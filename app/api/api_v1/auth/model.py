from fastapi_camelcase import CamelModel
from pydantic import BaseModel

from app.schemas.token import Token


class UserLoginIn(BaseModel):
    user: str
    password: str


class UserLoginOut(Token):
    username: str


class ResetPasswordPayload(CamelModel):
    token: str
    new_password: str
