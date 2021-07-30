from typing import List, Optional

from pydantic import BaseModel
from pydantic.class_validators import validator

class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode = True


class GamePlayers(BaseModel):
    player1: str
    player2: str


class RageQuit(BaseModel):
    player_id: int

class GameStatus(BaseModel):
    id: str
    serialized_game_status: str
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
