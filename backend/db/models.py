from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.databaseConnect import Base
import uuid


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)

    admin_forms = relationship("Forms", back_populates="owner")


class Forms(Base):
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
    url = Column(String)

    author_id = Column(Integer, ForeignKey("admin.id"))
    owner = relationship("Admin", back_populates="admin_owner")

