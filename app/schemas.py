from pydantic.networks import stricturl
from sqlalchemy import Boolean, Column, Integer, String, Table

from .database import Base, meta


User_db = Table(
   'users', meta,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String),
    Column("email", String),
    Column("password", String)
)

GameStatus_db = Table(
   'game_status', meta,

    Column("id", String, primary_key=True, index=True),
    Column("serialized_game_status", String),
)
