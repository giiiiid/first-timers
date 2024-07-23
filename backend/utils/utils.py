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
<<<<<<< HEAD
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt
=======
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')
    return encoded_jwt
>>>>>>> 08db9fa80fb7eb5f9a4c05bd1341fd14fb62b7eb
