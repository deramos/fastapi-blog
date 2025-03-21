import logging
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from app.db import models
from app.db.database import engine, get_db
from .schemas import PostCreate, Post, User
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)


@app.get("/")
def home():
    return {"message": "Backend Roadmap"}


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts", response_model=List[Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{post_id}", response_model=Post)
async def get_posts(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with id {post_id} found"
        )
    return post


@app.delete("/posts/{post_id}")
async def get_posts(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with id {post_id} found"
        )
    post.delete(synchronize_session=False)
    db.commit()
    return {"message": f"post {post_id} deleted successfully"}


@app.put("/posts/{post_id}", response_model=Post)
async def get_posts(post_id: int, post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    update_post = post_query.first()

    if not update_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post with id {post_id} found"
        )

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return update_post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
