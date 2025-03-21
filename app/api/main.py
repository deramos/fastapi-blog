import logging
from fastapi import FastAPI, Depends, HTTPException, status
from app.db import models
from app.db.database import engine, get_db
from .schemas import PostCreate, Post, UserCreate, UserOut
from sqlalchemy.orm import Session
from app.util import utils
from .routers.post import router as post_router

models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

app = FastAPI()
app.include_router(post_router)


@app.get("/")
def home():
    return {"message": "Backend Roadmap"}
