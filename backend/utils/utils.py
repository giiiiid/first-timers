from passlib.context import CryptContext


# hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# func to hash password
def get_password_hash(password):
    return pwd_context.hash(password)


# func to verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


