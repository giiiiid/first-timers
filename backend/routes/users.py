from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from config.config import get_db, oauth2_scheme, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRES_MINUTES
from utils.schema import AdminIn, AdminOut, LoginDb, Token, TokenData
from utils.utils import get_password_hash, verify_password, create_access_token
from sqlalchemy.orm import Session
from db.models import Admin, AgendaDb
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import  timedelta

users = APIRouter()


# admin creation
@users.post("/v1/admin/create", response_model=AdminOut, tags=["Admin"])
async def create_admin(userin: AdminIn, db: Session = Depends(get_db)):
    hash_pwd = get_password_hash(userin.password)
    new_admin = Admin(
        first_name = userin.first_name, last_name = userin.last_name,
        email = userin.email, role = userin.role, password = hash_pwd
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {
        "status_code": status.HTTP_201_CREATED,
        "detail": "Account created successfully",
        "admin": new_admin
    }


# get current user
async def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "Could not validate credentials",
        headers= {"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    current_admin = db.query(Admin).filter(Admin.username == token_data.username).first()
    if current_admin is None:
        raise credentials_exception
    return current_admin


# get current active user
async def get_current_active_admin(current_admin: Admin = Depends(get_current_admin)):
    if current_admin.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive admin")
    return current_admin


# admin login
@users.post("/v1/admin/login", tags=["Admin"])
async def login(form_data: LoginDb, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(form_data.username == Admin.username).first()
    if not admin:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Incorrect username or password"
        )
    verified_password = verify_password(form_data.password, admin.password)
    if not verified_password:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Incorrect username or password"
            )
    return {"access_token": admin.first_name, "token": "bearer"}


# login for access token
@users.post("/v1/login")
async def login_access_token(form_data: LoginDb, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(form_data.username == Admin.username).first()
    verified_password = verify_password(form_data.password, admin.password)
    if not admin or verified_password:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    acess_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=acess_token_expires
        )
    return Token(access_token=access_token, token_type="bearer")

    
# admin agendas
@users.get("/v1/{admin_id}/agenda-list", tags=["Admin"])
async def admin_agenda_list(admin_id: str, db: Session = Depends(get_db)):
    agendas = db.query(AgendaDb).filter(admin_id == AgendaDb.admin_id).all()
    return agendas