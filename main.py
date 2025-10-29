from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel, Field

app = FastAPI()

class PostBase(BaseModel):
    title: str = Field(..., max_length=100)
    content: str 
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def root():
    return {"message": "Welcome to my blog API!"}


@app.post('/posts')
def create_post(post: PostBase):
    print(post)
    return {"message": "Post created successfully!"}

