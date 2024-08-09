from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from config.config import get_db, oauth2_scheme, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRES_MINUTES
from utils.schema import *
from utils.main_utils import verify_password, create_access_token, pwd_context
from utils.email_utils import send_email, send_password_reset_request_email
from utils.password_reset import generate_password_reset_token
from sqlalchemy.orm import Session
from models.models import Admin, AgendaDb
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import  timedelta



users = APIRouter()



# Helper functions
def get_admin_by_username(username: str, db: Session):
    return db.query(Admin).filter(Admin.username == username).first()


def get_admin_by_email(email: str, db: Session):
    return db.query(Admin).filter(Admin.email == email).first()


def authenticate_admin(username: str, password: str, db: Session):
    admin = get_admin_by_username(username, db)
    if not admin:
        return False
    if not verify_password(password, admin.password):
        return False
    return admin

def create_admin(user: AdminIn, db: Session):
    hashed_pwd = pwd_context.hash(user.password)
    db_admin = Admin(
        first_name=user.first_name, last_name=user.last_name, email=user.email, 
        username=user.username, role=user.role, password=hashed_pwd
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


# admin creation
@users.post("/v1/admin/create", tags=["Admin"])
async def create_admin_route(
    userin: AdminIn, 
    # background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    db_admin = get_admin_by_username(userin.username, db)
    db_admin_email = get_admin_by_email(userin.email, db)

    if db_admin:
        raise HTTPException(status_code=400, detail="Username already exists")
    # if db_admin_email:
    #     raise HTTPException(status_code=400, detail="Email already exists")
    if userin.password != userin.confirm_password:
        raise HTTPException(status_code=404, detail="Passwords do not match")
    
    await send_email(
        subject="We're happy to have you worship with us",
        email_to=userin.email,
        # template="first-timers/backend/utils/templates/new_admin_notification.html",
        # context={"name": userin.username, "email": userin.email}
    )
    new_admin = create_admin(userin, db)

    # background_tasks.add_task(send_notification, new_admin.email, message="trial notif")
    return new_admin


# admin login
@users.post("/v1/admin/login", tags=["Admin"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    db_admin = get_admin_by_username(form_data.username, db)
    if not db_admin:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, db_admin.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {
        "access_token":db_admin.username, "id": db_admin.id, 
        "token":"bearer", "message": "Login successfully"
    }


# payload to get current admin
async def get_current_admin(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
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
    admin = get_admin_by_username(username=token_data.username, db=db)
    if admin is None:
        raise credentials_excepton
    return admin


# get current active admin
# async def get_current_active_admin(current_admin: Admin = Depends(get_current_admin)):
#     if current_admin:
#         raise HTTPException(status_code=400, detail="Inactive admin")
#     return current_admin


# login for access token
@users.post("/v1/admin/login/oauth", tags=["Oauth Login"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
) -> Token:
    admin = authenticate_admin(form_data.username, form_data.password, db)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = await create_access_token(
        data={"sub":admin.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# read admin details
@users.get("/v1/admin/me", response_model=AdminOut, tags=["Admin"])
async def read_admin_me(current_admin: Admin = Depends(get_current_admin)):
    return current_admin


# admin agenda-list
@users.get("/v1/admin/agenda-list", tags=["Admin"])
async def admin_agenda_list(
    current_admin: Admin = Depends(get_current_admin), 
    db:Session = Depends(get_db)
):
    agendas = db.query(AgendaDb).filter(AgendaDb.admin_id==current_admin.id).all()
    if len(agendas) == 0:
        return {"message": "You do not have any agenda yet"}
    return agendas


@users.post("/v1/admin/reset-password", tags=["Admin"])
async def password_reset_request(
    reset_request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    admin = db.query(Admin).filter(Admin.email == reset_request.email).first()
    if not admin:
        raise HTTPException(
            status_code = 200,
            detail= "Admin not found"
        )
    token = generate_password_reset_token(admin.email)
    reset_url = f"http://127.0.0.1:8000/v1/admin/password-reset/{token}"

    await send_password_reset_request_email(
        subject="Reset Your Password",
        email_to=admin.email,
        template="backend/utils/templates/password_reset_request.html",
        context={"reset_url": reset_url}
    )
    return {"message": "Password reset email sent"}