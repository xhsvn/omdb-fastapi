from pydantic import Field


from src.core.schema import BaseModel


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_-]+$")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=20)


class User(UserBase):
    pass

