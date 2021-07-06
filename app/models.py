from typing import Optional

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

    # check game status
    @validator()
    def check_game_status(self):
        if self.game.finished:
            return False

    # check player
    @validator("player_id")
    def check_player(self, player_id):
        if self.game.player_turn != player_id or player_id not in range(1,2):
            return False

    # check move
    @validator("coordinate")
    def check_move(self, coordinate):
        if (
            len(coordinate) != 2 or \
            coordinate[0] not in range(0,2) or \
            coordinate[1] not in range(0,2) or \
            self.game.board[coordinate[0]][coordinate[1]] != 0
        ):
            return False

    # move
    @validator("coordinate", "player_id")
    def move(self, coordinate):
        if self.game.board[coordinate[0]][coordinate[1]] = player_id
