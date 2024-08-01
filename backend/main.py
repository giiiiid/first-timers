from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import run, users, forms, agenda
from models import models
from db.databaseConnect import engine


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(run.run)
app.include_router(users.users)
app.include_router(forms.forms)
app.include_router(agenda.agenda)
