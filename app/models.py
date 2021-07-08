from typing import List, Optional

from pydantic import BaseModel
from pydantic.class_validators import validator

class GamePlayers(BaseModel):
    player1: str
    player2: str


class RageQuit(BaseModel):
    player_id: int


class GameMove(BaseModel):
    player_id: int
    coordinate: list

    # check player
    @validator("player_id")
    def check_player(cls, y):
        if y not in range(1,3):
            raise ValueError("player_id out of the range; got: " + str(y))
        return y

    # check move
    @validator("coordinate")
    def check_move(cls, y):
        if (
            len(y) != 2 or
            y[0] not in range(0,3) or \
            y[1] not in range(0,3)
        ):
            raise ValueError("coordinate out of the range; got: " + str(y))
        return y

# class GameStatus(Base):
#     __tablename__ = "game_status"

#     player1 = Column(Integer)
#     player2 = Column(Integer)
#     player_turn = Column(Integer)
#     board = Column(List)
#     score_board = Column(List)
#     player_win = Column(Integer)
