from typing import Optional
from fastapi import FastAPI, status,HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class PostBase(BaseModel):
    title: str = Field(..., max_length=100)
    content: str 
    published: bool = True
    rating: Optional[int] = None

available_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2},
            {"title": "title of post 3", "content": "content of post 3", "id": 3}]

@app.get("/posts")
def get_posts():
    return {"data": available_posts}


@app.get("/posts/{id}")
def get_post(id:int):
    for post in available_posts:
        if post['id'] == id:
            return {"post_detail": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: PostBase):
    new_id = max([current_post['id'] for current_post in available_posts]) + 1
    new_post = {**post.model_dump(), "id": new_id}
    available_posts.append(new_post)
    return {"data": post}


@app.delete("/posts/{id}")
def delete_post(id:int):
    for idx, post in enumerate(available_posts):
        if post['id'] == id:
            del available_posts[idx]
            return {"message": f"post with id: {id} was deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
