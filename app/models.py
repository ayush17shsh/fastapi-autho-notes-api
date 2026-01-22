from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    age = Column(Integer)
    password = Column(String(255), nullable = False)

class NotesDB(Base):
    __tablename__ = "notes"

    id = Column( Integer, primary_key=True, index= True)
    title = Column(String(100), nullable= False)
    content = Column(String(500), nullable= False)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UserDB")
