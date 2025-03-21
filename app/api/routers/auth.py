from fastapi import APIRouter,status, Depends, HTTPException
from app.api.schemas import UserCreate, UserOut
from app.db.database import get_db
from app.db import models
from app.util import utils
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)


@router.post("/")
def login():
    pass