import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.api import schemas
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, HTTPException, Depends

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
TOKEN_EXPIRES = 30


def hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=TOKEN_EXPIRES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=JWT_SECRET,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, ALGORITHM)
        _id: str = decoded_token.get("user_id")

        if _id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=_id)
    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    verify_access_token(token, credentials_exception)