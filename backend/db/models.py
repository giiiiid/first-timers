from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.databaseConnect import Base
import uuid
from datetime import datetime


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)

    # admin_forms = relationship("Forms", back_populates="owner")
    admin_agenda = relationship("Admin", back_populates="owner")



class AgendaDb(Base):
    __tablename__ = "agenda"
    id = Column(Integer, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, default="Agenda title")
    description = Column(String, default="A description")
    # url = Column(String)
    admin_id = Column(Integer, ForeignKey("admin.id"))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    owner = relationship("Admin", back_populates="admin_agenda")
    agenda_forms = relationship("Forms", back_populates="assigned_agenda")
    

class FormsDb(Base):
    __tablename__ = "forms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    hostel_or_hall = Column(String)
    room_number = Column(String)
    likes = Column(String)
    dislikes = Column(String)
    brought_by = Column(String)
    agenda_id = Column(Integer, ForeignKey("agenda.id"))

    assigned_agenda = relationship("Admin", back_populates="agenda_forms")

