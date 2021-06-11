from pydantic import BaseModel
from typing import Optional
from typing import List


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    class Config:
        orm_mode = True


class UserShow(BaseModel):
    id: int
    name: str
    email: str
    blogs: List[Blog] = []

    class Config:
        orm_mode = True


class BlogShow(BaseModel):
    id: int
    title: str
    body: str
    user: UserShow

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
