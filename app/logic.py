from random import randint
from typing import Optional
from fastapi.param_functions import Depends
from sqlalchemy.orm import Session, Query
from sqlalchemy import create_engine, select, update, MetaData, Table, and_
from sqlalchemy.sql.expression import insert, true

import jsonpickle

import uuid
import time

from app.database import engine, Base, get_db
import app.schemas
import app.models

class Logic():
    class Game():
        # Create pydantic object for game properties with validation
        """
        For the purpouse of this project we assume that
        player1 has ID:1, and player2 has ID:2.
        """
        id: int
        player1: Optional[str]
        player2: Optional[str]

        board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        player_turn: int
        player_win: int
        finished = False

        score_board = dict

        def __init__(self, id: str, player1: str, player2: str) -> None:
            self.id = id
            self.player1 = player1
            self.player2 = player2
            self.player_turn = 0
            self.player_win = 0
            self.score_board = {self.player1: 0, self.player2: 0}
            self.board = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]

    all_possible_winning_combinations = [
        [[0,0], [0,1], [0,2]],
        [[1,0], [1,1], [1,2]],
        [[2,0], [2,1], [2,2]],

        [[0,0], [1,0], [2,0]],
        [[0,1], [1,1], [2,1]],
        [[0,2], [1,2], [2,2]],

        [[0,0], [1,1], [2,2]],
        [[0,2], [1,1], [2,0]]
    ]

    error_codes = {
        "GAME_FINISHED": 100,
        "PLAYER_TURN_MISMATCH": 101,
        "PLACE_ON_BOARD_ALREADY_TAKEN": 102,


    }

    def __init__(self) -> None:
        self.game = False

    def makeUUID(self, text: str = "") -> str:
        timestamp = time.time()
        return str(uuid.uuid5(uuid.NAMESPACE_URL, f"{text}{timestamp}"))

    def create_state(self, db: Session = Depends(get_db)) -> bool:
        stmt = app.models.GameStatus(
            id=self.game.id,
            serialized_game_status=jsonpickle.encode(self.game)
        )
        db.add(stmt)
        db.commit()
        db.refresh(stmt)
        return True

    def save_state(self, id, db: Session = get_db()) -> bool:
        stmt = db.execute(select(app.models.GameStatus).filter_by(id=self.game.id)).scalar_one()
        stmt.serialized_game_status=jsonpickle.encode(self.game)
        print(
            "SELF.ID:", self.game.id,
            "STMT:", stmt,
            "ID", id
        )
        db.add(stmt)
        db.commit()
        db.refresh(stmt)
        return True

    def load_state(self, id, db: Session = Depends(get_db)) -> bool:
        stmt = select([
            GameStatus.columns.id,
            GameStatus.columns.serialized_game_status]
        ).where(
            GameStatus.columns.id == id
        )
        self.game = jsonpickle.decode(result[0]["serialized_game_status"])
        return True

    def draw_player_turn(self) -> None:
        self.game.player_turn = randint(1,2)

    def create(self, player1: str = "player1", player2: str = "player2") -> bool:
        self.game = self.Game(self.makeUUID("id"), player1, player2)
        self.draw_player_turn()
        return True

    def status(self):
        return {
            "id": self.game.id,
            "player1": self.game.player1,
            "player2": self.game.player2,
            "player_turn": self.game.player_turn,
            "board": self.game.board,
            "score_board": self.game.score_board,
            "player_win": self.game.player_win
        }

    def move(self, player_id, coordinate: list) -> int:
        # check game status
        if self.game.finished:
            return self.error_codes["GAME_FINISHED"]

        # check player
        if self.game.player_turn != player_id:
            return self.error_codes["PLAYER_TURN_MISMATCH"]

        # check move
        if self.game.board[coordinate[0]][coordinate[1]] != 0:
            return self.error_codes["PLACE_ON_BOARD_ALREADY_TAKEN"]

        # move
        self.game.board[coordinate[0]][coordinate[1]] = player_id

        # check if someone won
        for x in self.all_possible_winning_combinations:
            if not self.game.finished:
                result = 0
                if (self.game.board[x[0][0]][x[0][1]] == \
                    self.game.board[x[1][0]][x[1][1]] == \
                    self.game.board[x[2][0]][x[2][1]]
                ):
                    result = (
                        self.game.board[x[0][0]][x[0][1]] + \
                        self.game.board[x[1][0]][x[1][1]] + \
                        self.game.board[x[2][0]][x[2][1]]
                    )

                    if result == 3:
                        self.game.player_win = 1
                        self.game.finished = True

                    elif result == 6:
                        self.game.player_win = 2
                        self.game.finished = True

        # check if drawn
        zeros = 0
        for x in range(0,2):
            for y in range(0,2):
                if self.game.board[x][y] == 0:
                    zeros += 1
        if zeros == 0 and not self.game.finished:
            self.game.finished = True

        # swap players
        if not self.game.finished:
            self.game.player_turn = ((self.game.player_turn + 2) % 2) + 1
            # self.game.player_turn = ((1 + 2) % 2) + 1 = 2 | ((2 + 2) % 2) + 1 = 1

        return 0


    def ragequit(self, player_id) -> bool:
        if player_id in range(1,2):
            self.game.finished = True
            self.game.player_win = ((player_id + 2) % 2) + 1
            return True
        else:
            return False
