from .. import models, schemas, database,utils
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter

router = APIRouter()

@router.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id:int, db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user with id: {id} was not found")

@router.post('/users', status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user: schemas.User, db: Session = Depends(database.get_db)):
    user.password = utils.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user