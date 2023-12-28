from fastapi import FastAPI
from . import models
from .database import engin
from .routers import blog, user, authentication

app = FastAPI()

models.Base.metadata.create_all(engin)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(blog.router)
