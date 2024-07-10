from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from config.config import get_db
from utils.schema import AdminIn, AdminOut, LoginDb
from utils.utils import get_password_hash, verify_password
from sqlalchemy.orm import Session
from db.models import Admin


users = APIRouter()


# admin creation
@users.post("/v1/admin/create", response_model=AdminOut, tags=["Admin"])
async def create_admin(userin: AdminIn, db: Session = Depends(get_db)):
    hash_pwd = get_password_hash(userin.hashed_password)
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


@users.post("/v1/admin/login", tags=["Admin"])
async def login(form_data: LoginDb, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(form_data.email == Admin.email).first()
    if not admin:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            details = "Incorrect username or password"
        )
    verified_password = verify_password(form_data.password, admin.password)
    if not verified_password:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Incorrect username or password"
            )
    
    return {"access_token": admin.first_name, "token": "bearer"}
