from fastapi import APIRouter, Depends, HTTPException, status
from utils.schema import AgendaModel
from config.config import get_db
from db.models import AgendaDb, Admin
from sqlalchemy.orm import Session


agenda = APIRouter()


# create agenda
@agenda.post("/v1/{user_id}/agenda/create", response_model=AgendaModel)
async def create_agenda(user_id: str, agenda_item: AgendaModel, db: Session = Depends(get_db)):
    if user_id not in Admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised admin")
    new_agenda = AgendaDb(title = agenda_item.title, description = agenda_item.description, admin_id = id)
    db.add(new_agenda)
    db.commit()
    db.refresh(new_agenda)

    return new_agenda


# view agenda
@agenda.get("/v1/{user_id}/{agenda_id}", response_model=AgendaModel)
async def retrieve_agenda(user_id: str, agenda_id: str, db: Session = Depends(get_db)):
    if user_id not in Admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised user")
    if agenda_id not in AgendaDb:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agenda not found")
    selected_agenda = db.query(AgendaDb).filter(AgendaDb.id == agenda_id, AgendaDb.admin_id == user_id).first()
    if selected_agenda is None:
        return {
          "status_code": status.HTTP_200_OK,
          "detail": "You do not have any agenda"  
        }
    return selected_agenda


# update agenda
@agenda.put("/v1/{user_id}/{agenda_id}/update", response_model=AgendaModel)
async def update_agenda(user_id: str, agenda_id: str, 
                        agenda_item: AgendaModel, db: Session = Depends(get_db)):
    selected_agenda = db.query(AgendaDb).filter(AgendaDb.id == agenda_id, 
                                                AgendaDb.admin_id == user_id).first()
    if not selected_agenda:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = "User or agenda could not be found")
    else:
        selected_agenda.title = agenda_item.title
        selected_agenda.description = agenda_item.description
        db.commit()
        db.refresh(selected_agenda)
    
    return selected_agenda


# delete agenda
@agenda.delete("/v1/{user_id}/{agenda_id}/update")
async def delete_agenda(user_id: str, agenda_id: str, db: Session = Depends(get_db)):
    selected_agenda = db.query(AgendaDb).filter(user_id == AgendaDb.admin_id, agenda_id == AgendaDb.id).first()
    if not selected_agenda:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = "User or agenda could not be found")
    db.delete(selected_agenda)
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "Agenda has been successfully deleted"
    }