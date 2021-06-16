from typing import Optional, List

from pydantic import BaseModel

class GamePlayers(BaseModel):
    player1: Optional[str] = None
    player2: Optional[str] = None


class RageQuit(BaseModel):
    player_id: int

class GameMove(BaseModel):
    player_id: int
    coordinate: list
