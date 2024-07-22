from db.databaseConnect import SessionLocal
from fastapi.security import oauth2
import os
from pathlib import Path
from dotenv import load_dotenv


'''Initializing db'''
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()



'''Loading env''' # loading environmental variables
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


# database settings
class Settings:
    PROJECT_NAME:str = "First Timers"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER : str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_SERVER : str = os.environ.get("POSTGRES_SERVER","localhost")
    POSTGRES_PORT : str = os.environ.get("POSTGRES_PORT",5432)
    POSTGRES_DB : str = os.environ.get("POSTGRES_DB","tdd")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
settings = Settings()



# Oauth setup
oauth2_scheme = oauth2.OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY= os.environ.get("SECRET_KEY")
ALGORITHM= os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRES_MINUTES=30


