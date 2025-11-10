from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
import psycopg
from psycopg.rows import dict_row

app = FastAPI()

class PostBase(BaseModel):
    title: str = Field(..., max_length=100)
    content: str 
    published: bool = True

class PostUpdate(PostBase):
    pass


try:
    conn = psycopg.connect(dbname='fast-social', user ='postgres', password='adjoa', row_factory=dict_row) 
    cur = conn.cursor()
    print("Connected to the database successfully")
    cur.execute("SELECT current_database();")
    print(cur.fetchone())


except Exception as error: 
    print("Error connecting to the database:", error)


available_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2},
            {"title": "title of post 3", "content": "content of post 3", "id": 3}]

@app.get("/posts")
def get_posts():
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id:int):
    cur.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cur.fetchone()
    if post:
        return {"post_detail": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found")


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: PostBase):
    cur.execute(
       "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (post.title, post.content, post.published))
    new_post = cur.fetchone()
    conn.commit()
    return {"data": new_post}



@app.put("/posts/{id}")
def update_post(id:int, post: PostUpdate):
    for idx, existing_post in enumerate(available_posts):
        if existing_post["id"] == id:
            updated_post = {**post.model_dump(), "id": id}
            available_posts[idx] = updated_post
            return {"data": updated_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    for idx, post in enumerate(available_posts):
        if post['id'] == id:
            del available_posts[idx]
            return 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
