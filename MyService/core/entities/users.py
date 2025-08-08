from typing import Optional

from pydantic import BaseModel, Field
from pydantic import ConfigDict


class UserBase(BaseModel):
    username: str = Field(..., max_length=25)
    email: str = Field(..., max_length=25)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=25)


class UserCreateDB(UserBase):
    password_hash: str


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, max_length=25)
    email: Optional[str] = Field(default=None, max_length=25)
    password: Optional[str] = Field(default=None, max_length=25, min_length=8)


class UserPublic(BaseModel):
    id: int
    username: str
    role: str
    model_config = ConfigDict(from_attributes=True)
