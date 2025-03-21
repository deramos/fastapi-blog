import logging
from fastapi import FastAPI
from app.db import models
from app.db.database import engine
from .routers.post import router as post_router
from .routers.user import router as user_router
from .routers.auth import router as auth_router

models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

app = FastAPI()
app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "Backend Roadmap"}
