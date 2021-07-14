from pydantic.networks import stricturl
from sqlalchemy import Boolean, Column, Integer, String, Table

from .database import Base

# User_db = Table(
#    'users', meta,
#     Column("id", Integer, primary_key=True, index=True),
#     Column("name", String),
#     Column("email", String),
#     Column("password", String)
# )

# GameStatus_db = Table(
#    'game_status', meta,

#     Column("id", String, primary_key=True, index=True),
#     Column("serialized_game_status", String),
# )

class User_db(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Integer)
    email = Column(Integer)
    password = Column(Integer)

class GameStatus_db(Base):
    __tablename__ = "game_status"
    id = Column(String, primary_key=True, index=True)
    serialized_game_status = Column(String)
