from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, database


# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.get("/posts")
def get_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post, db: Session = Depends(database.get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id:int,db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first();
    if post:
        return {"post_detail": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found")


@app.put("/posts/{id}")
def update_post(id:int, post_schema: schemas.PostUpdate, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post.first()
    if post_to_update:
        post.update(post_schema.model_dump())
        db.commit()
        return {"data": post.first()}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(database.get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    db.delete(deleted_post)
    db.commit()
    if deleted_post:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
