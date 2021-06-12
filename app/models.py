from typing import Optional

from pydantic import BaseModel

class GamePlayers(BaseModel):
    player1: Optional[str] = None
    player2: Optional[str] = None
