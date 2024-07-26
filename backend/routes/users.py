from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from config.config import get_db, oauth2_scheme, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRES_MINUTES
from utils.schema import AdminIn, AdminOut, LoginDb, Token, TokenData, AgendaModel
from utils.utils import get_password_hash, verify_password, create_access_token, pwd_context
from sqlalchemy.orm import Session
from db.models import Admin, AgendaDb
import jwt
from typing import List
from jwt.exceptions import InvalidTokenError
from datetime import  timedelta



users = APIRouter()



# Helper functions
def get_admin(username: str, db: Session):
    return db.query(Admin).filter(Admin.username == username).first()

def authenticate_admin(username: str, password: str, db: Session):
    admin = get_admin(username, db)
    if not admin:
        return False
    if not verify_password(password, admin.password):
        return False
    return admin

def create_admin(user: AdminIn, db: Session):
    hashed_pwd = pwd_context.hash(user.password)
    db_admin = Admin(first_name=user.first_name, last_name=user.last_name, email=user.email,
                     username=user.username, role=user.role, password=hashed_pwd
                    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


# admin creation
@users.post("/v1/admin/create", response_model=AdminOut, tags=["Admin"])
async def create_admin_route(userin: AdminIn, db: Session = Depends(get_db)):
    db_admin = get_admin(userin.username, db)
    if db_admin:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_admin = create_admin(userin, db)
    return {
        "username": new_admin.username,
        "id": new_admin.id
    }


# admin login
@users.post("/v1/admin/login", tags=["Admin"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_admin = get_admin(form_data.username, db)
    if not db_admin:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, db_admin.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"access_token":db_admin.username, "id": db_admin.id, "token":"bearer","message": "Login successfully"}


# payload to get current admin
async def get_current_admin(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_excepton = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_excepton
        token_data = TokenData(username = username)
    except InvalidTokenError:
        raise credentials_excepton
    admin = get_admin(username=token_data.username, db=db)
    if admin is None:
        raise credentials_excepton
    return admin


# get current active admin
async def get_current_active_admin(current_admin: Admin = Depends(get_current_admin)):
    if current_admin.disabled:
        raise HTTPException(status_code=400, detail="Inactive admin")
    return current_admin


# login for access token
@users.post("/v1/admin/login/oauth", tags=["Oauth Login"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    admin = authenticate_admin(form_data.username, form_data.password, db)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = await create_access_token(data={"sub":admin.username}, expires_delta=access_token_expires)
    
    return Token(access_token=access_token, token_type="bearer")


# read admin details
@users.get("/v1/admin/me", response_model=AdminOut, tags=["Admin"])
async def read_admin_me(current_admin: Admin = Depends(get_current_admin)):
    return current_admin


# admin agenda-list
@users.get("/v1/admin/agenda-list", response_model=List[AgendaModel], tags=["Admin"])
async def admin_agenda_list(current_admin: Admin = Depends(get_current_admin), db:Session = Depends(get_db)):
    agendas = db.query(AgendaDb).filter(AgendaDb.admin_id==current_admin.id).all()
    if agendas is None:
        return {"message": "You do not have any agenda"}
    return agendas