from fastapi import APIRouter,status, Depends, HTTPException
from app.api.schemas import UserLogin
from app.db import database
from app.db import models
from app.utils import utils
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)


@router.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid credentials")

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid credentials")

    return {"token": "example_token"}
