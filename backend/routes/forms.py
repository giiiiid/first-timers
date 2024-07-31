from fastapi import APIRouter, Depends, HTTPException, status
from models.models import FormsDb, AgendaDb
from config.config import get_db
from utils.schema import FormsModel
from sqlalchemy.orm import Session


forms = APIRouter()


# create or add new form response
@forms.post("/v1/{agenda_id}/fill-form", response_model=FormsModel, tags=["Forms"])
async def add_form_response(
    agenda_id: str, form: FormsModel, 
    db: Session = Depends(get_db)
):
    agenda = db.query(AgendaDb).filter(AgendaDb.id == agenda_id).first()
    if not agenda:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Agenda could not be found"
        )
    
    new_form = FormsDb(
        name=form.name, email=form.email, phone_number=form.phone_number, 
        residence=form.residence, room_number=form.room_number, 
        likes=form.likes, dislikes=form.dislikes, 
        brought_by=form.brought_by, agenda_id=agenda_id
    )
    db.add(new_form)
    db.commit()
    db.refresh(new_form)

    return new_form


# retrieve a form response
@forms.get("/v1/{agenda_id}/{form_id}", response_model=FormsModel, tags=["Forms"])
async def retrieve_form(
    agenda_id: str, form_id: str, 
    db: Session = Depends(get_db)
):
    if not db.query(AgendaDb).filter(AgendaDb.id == agenda_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Could not be found"
        )
    if not db.query(FormsDb).filter(FormsDb.id == form_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Could not be found"
        )
    selected_form =  db.query(FormsDb).filter(
        FormsDb.agenda_id==agenda_id, FormsDb.id==form_id
    ).first()
    return selected_form


# update a form response
# @forms.put("/v1/{agenda_id}/{forms_id}/update", response_model=FormsModel, tags=["Forms"])
# async def update_agenda(agenda_id: str, forms_id: str, form: FormsModel, db: Session = Depends(get_db)):
#     selected_forms = db.query(FormsDb).filter(FormsDb.id == forms_id, FormsDb.agenda_id == agenda_id).first()
#     if not selected_forms:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail = "User or agenda could not be found")
#     else:
#         selected_forms.title = form.title
#         selected_forms.description = form.description
#         db.commit()
#         db.refresh(selected_forms)
    
#     return selected_forms


# delete a form response
@forms.delete("/v1/{agenda_id}/{form_id}/delete", tags=["Forms"])
async def delete_agenda(
    agenda_id: str, form_id: str, 
    db: Session = Depends(get_db)
):
    selected_agenda = db.query(FormsDb).filter(
        FormsDb.id == form_id, FormsDb.agenda_id == agenda_id
    ).first()
    if not selected_agenda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail = "Form could not be found"
        )
    db.delete(selected_agenda)
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "detail": "Form has been successfully deleted"
    }