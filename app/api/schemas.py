from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False


class PostCreate(PostBase):
    pass


class Post(PostBase):
    title: str
    content: str
    published: bool
    created_at: datetime


class UserBase(BaseModel):
    email: EmailStr


class UserOut(UserBase):
    created_at: datetime


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str
