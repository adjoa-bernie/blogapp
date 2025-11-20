from fastapi import FastAPI
from . import models, database
from .routers import post, user


# Create tables
models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)





