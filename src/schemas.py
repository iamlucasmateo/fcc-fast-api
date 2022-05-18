from typing import List

from pydantic import BaseModel, EmailStr

# pydantic models are for Requests and Responses
# we could create one for each type of request, if we need different types of behavior
# also useful could be creating a "PostBase" class and then extend it
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    title: str
    content: str
    published: bool

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
