from fastapi import APIRouter, Depends, HTTPException, status
from utils.schema import AgendaModel, FormsModel
from config.config import get_db
from models.models import AgendaDb, Admin
from sqlalchemy.orm import Session
from .users import get_current_admin
from typing import List


agenda = APIRouter()


# create agenda
@agenda.post("/v1/agendas/create", response_model=AgendaModel, tags=["Agenda"])
async def create_agenda(
    agenda_item: AgendaModel, 
    user: Admin = Depends(get_current_admin), 
    db: Session = Depends(get_db)
):
    if not db.query(Admin).filter(user.id == Admin.id).first():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unauthorised admin"
        )
    new_agenda = AgendaDb(
        title = agenda_item.title, 
        description = agenda_item.description, 
        admin_id = user.id
    )
    db.add(new_agenda)
    db.commit()
    db.refresh(new_agenda)

    return new_agenda


# view agenda
@agenda.get("/v1/agendas/{agenda_id}/get", response_model=AgendaModel, tags=["Agenda"])
async def get_agenda(
    agenda_id: str, 
    user: Admin = Depends(get_current_admin), 
    db: Session = Depends(get_db)
):
    if not db.query(Admin).filter(user.id == Admin.id).first():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Unauthorised user"
        )
    if not db.query(AgendaDb).filter(agenda_id == AgendaDb.id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Agenda not found"
        )
    selected_agenda = db.query(AgendaDb).filter(
        AgendaDb.id == agenda_id, AgendaDb.admin_id == user.id
    ).first()
    if selected_agenda is None:
        return {
          "status_code": status.HTTP_200_OK,
          "detail": "You do not have any agenda"  
        }
    return selected_agenda


# update agenda
@agenda.put("/v1/agendas/{agenda_id}/update", response_model=AgendaModel, tags=["Agenda"])
async def update_agenda(
    agenda_id: str, 
    agenda_item: AgendaModel, 
    user: Admin = Depends(get_current_admin), 
    db: Session = Depends(get_db)
):
    selected_agenda = db.query(AgendaDb).filter(
        AgendaDb.id == agenda_id, 
        AgendaDb.admin_id == user.id
    ).first()
    if not selected_agenda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail = "User or agenda could not be found"
        )
    else:
        selected_agenda.title = agenda_item.title
        selected_agenda.description = agenda_item.description
        db.commit()
        db.refresh(selected_agenda)

    return selected_agenda


# delete agenda
@agenda.delete("/v1/agendas/{agenda_id}/delete", tags=["Agenda"])
async def delete_agenda(
    agenda_id: str, 
    user: Admin = Depends(get_current_admin), 
    db: Session = Depends(get_db)
):
    selected_agenda = db.query(AgendaDb).filter(
        user.id == AgendaDb.admin_id, 
        agenda_id == AgendaDb.id
    ).first()
    if not selected_agenda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail = "User or agenda could not be found"
        )
    db.delete(selected_agenda)
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "Agenda has been successfully deleted"
    }


# get-agenda-forms
@agenda.get("/v1/agendas/{agenda_id}/forms", response_model=List[FormsModel], tags=["Agenda"])
async def get_agenda_forms(
    agenda_id: str, 
    db: Session = Depends(get_db)
):
    selected_agenda = db.query(AgendaDb).filter(AgendaDb.id == agenda_id).first()
    if not selected_agenda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Agenda is not found"
        )
    return selected_agenda.agenda_forms

