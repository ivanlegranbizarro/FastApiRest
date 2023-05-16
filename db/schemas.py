from datetime import datetime

from pydantic import BaseModel, EmailStr, conint


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    user_email: EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    author: UserResponse

    class Config:
        orm_mode = True


class VoteSchema(BaseModel):
    user_id: int
    post_id: int
    dir: conint(ge=0, le=1)

    class Config:
        orm_mode = True
