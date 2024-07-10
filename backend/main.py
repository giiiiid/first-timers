from fastapi import FastAPI
from routes.run import run
from routes.users import users
from db import models
from db.databaseConnect import engine


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


app.include_router(run)
app.include_router(users)