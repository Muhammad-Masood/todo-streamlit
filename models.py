from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Todo(Base):
    __tablename__ = "todos"
    id = Column(String, primary_key=True, index=True, unique=True, default=str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String)
    isDone = Column(Boolean, default=False)
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User", back_populates="todos")

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True, default=str(uuid.uuid4()), unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    todos = relationship("Todo", back_populates="user")