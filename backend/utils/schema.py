from pydantic import BaseModel, EmailStr
from typing import Optional, Union


# Admin BaseModel
class AdminModel(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    role: str


class AdminIn(AdminModel):
    password: str


class AdminOut(AdminModel):
    pass 


class LoginDb(BaseModel):
    username: str
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


# Tokendata BaseModel
class TokenData(BaseModel):
    username: Union[str, None] = None



class Token(BaseModel):
    access_token: str
    token_type: str