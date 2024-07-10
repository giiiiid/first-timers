from fastapi import FastAPI
from routes.run import run

app = FastAPI()


app.include_router(run)