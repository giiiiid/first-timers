from pydantic import BaseModel, EmailStr
from typing import Optional


# Admin BaseModel
class AdminDetails(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: str


class AdminIn(AdminDetails):
    password: str


class AdminOut(AdminDetails):
    pass 




# Forms BaseModel
class AdminForms(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    residence: str
    room_number: Optional[str]
    likes: Optional[str]
    dislikes: Optional[str]
    brought_by: str



class LoginDb(BaseModel):
    email: EmailStr
    password: str
