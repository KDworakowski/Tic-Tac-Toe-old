from typing import List, Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Integer)
    email = Column(Integer)
    password = Column(Integer)
class GameStatus(Base):
    __tablename__ = "game_status"
    id = Column(String, primary_key=True, index=True)
    serialized_game_status = Column(String)

# class GameMove(Base):
#     player_id: int
#     coordinate: list

#     # check player
#     @validator("player_id")
#     def check_player(cls, y):
#         if y not in range(1,3):
#             raise ValueError("player_id out of the range; got: " + str(y))
#         return y

#     # check move
#     @validator("coordinate")
#     def check_move(cls, y):
#         if (
#             len(y) != 2 or
#             y[0] not in range(0,3) or \
#             y[1] not in range(0,3)
#         ):
#             raise ValueError("coordinate out of the range; got: " + str(y))
#         return y
