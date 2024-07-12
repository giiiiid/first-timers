from fastapi import FastAPI
from routes import run, users, forms, agenda
from db import models
from db.databaseConnect import engine


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


app.include_router(run.run)
app.include_router(users.users)
app.include_router(forms.forms)
app.include_router(agenda.agenda)
