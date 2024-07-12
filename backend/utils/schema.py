from pydantic import BaseModel, EmailStr
from typing import Optional


# Admin BaseModel
class AdminModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: str


class AdminIn(AdminModel):
    password: str


class AdminOut(AdminModel):
    pass 


class LoginDb(BaseModel):
    email: EmailStr
    password: str


# Agenda BaseModel
class AgendaModel(BaseModel):
    title: str
    description: Optional[str]


# Forms BaseModel
class FormsModel(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    residence: str
    room_number: Optional[str]
    likes: Optional[str]
    dislikes: Optional[str]
    brought_by: str

