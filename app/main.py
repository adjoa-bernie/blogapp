from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from . import models, schemas, database


# Create tables
models.Base.metadata.create_all(bind=database.engine)

password_hash = PasswordHash.recommended()

app = FastAPI()

@app.get("/posts", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post, db: Session = Depends(database.get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@app.get("/posts/{id}")
def get_post(id:int,db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first();
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found")


@app.put("/posts/{id}")
def update_post(id:int, post_schema: schemas.PostUpdate, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post.first()
    if post_to_update:
        post.update(post_schema.model_dump())
        db.commit()
        return post.first()
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


@app.post('/users', status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user: schemas.User, db: Session = Depends(database.get_db)):
    user.password = password_hash.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users

@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id:int, db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user