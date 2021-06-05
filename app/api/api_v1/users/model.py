from fastapi_camelcase import CamelModel
from pydantic.networks import EmailStr


class UserUpdatePayload(CamelModel):
    password: str
    full_name: str
    email: EmailStr
