from pydantic import BaseModel, Field

class Post(BaseModel):
    title: str = Field(..., max_length=100)
    content: str 
    published: bool = True

    class Config:
        orm_mode = True 

class PostUpdate(Post):
    pass