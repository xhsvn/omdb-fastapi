from pydantic import Field
from src.core.schema import BaseModel


class AuthData(BaseModel):
    username: str
    password: str


class JWTData(BaseModel):
    user_id: int = Field(alias="sub")
    is_admin: bool = False


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
