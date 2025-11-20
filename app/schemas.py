from pydantic import BaseModel, Field,EmailStr
from datetime import datetime

class Post(BaseModel):
    title: str = Field(..., max_length=100)
    content: str 
    published: bool = True

    class Config:
        orm_mode = True 

class PostUpdate(Post):
    pass

class PostResponse(Post):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class User(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True