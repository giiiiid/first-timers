from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.databaseConnect import Base
import uuid
from datetime import datetime, timezone


class Admin(Base):
    __tablename__ = "admin"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)

    # admin_forms = relationship("Forms", back_populates="owner")
    admin_agenda = relationship("AgendaDb", back_populates="owner")



class AgendaDb(Base):
    __tablename__ = "agenda"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String, default="Agenda title")
    description = Column(String, default="A description")
    # url = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    admin_id = Column(Integer, ForeignKey("admin.id"))

    owner = relationship("Admin", back_populates="admin_agenda")
    agenda_forms = relationship("FormsDb", back_populates="assigned_agenda")
    

class FormsDb(Base):
    __tablename__ = "forms"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    residence = Column(String)
    room_number = Column(String)
    likes = Column(String)
    dislikes = Column(String)
    brought_by = Column(String)
    agenda_id = Column(Integer, ForeignKey("agenda.id"))

    assigned_agenda = relationship("AgendaDb", back_populates="agenda_forms")

