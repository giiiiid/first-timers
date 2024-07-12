from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from config.config import SECRET_KEY, ALGORITHM
from typing import Union
import jwt


# hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# func to hash password
def get_password_hash(password):
    return pwd_context.hash(password)


# func to verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# create access token
async def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt