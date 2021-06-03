from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic import BaseModel


class Token(CamelModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
