from fastapi import FastAPI
from routes.run import run
from db import models
from db.databaseConnect import engine


app = FastAPI()


models.Base.metadata.create_all(bind=engine)
app.include_router(run)