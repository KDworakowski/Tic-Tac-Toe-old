from pydantic.main import BaseModel
from sqlalchemy import Boolean, Column, Integer, String

from .database import Base

from pydantic import BaseModel

class User(BaseModel):
    name: str
    password: str

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
