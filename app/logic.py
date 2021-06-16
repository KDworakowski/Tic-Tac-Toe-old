from random import randint
class Logic():

    class Game():
        """
        For the purpouse of this project we assume that
        player1 has ID:1, and player2 has ID:2.
        """
        player1 = ""
        player2 = ""

        board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        player_turn = 0
        player_win = 0
        finished = False

        score_board = {}

        def __init__(self, player1: str, player2: str) -> None:
            self.player1 = player1
            self.player2 = player2
            self.score_board = {self.player1: 0, self.player2: 0}

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

    def __init__(self) -> None:
        self.game = False

    def draw_player_turn(self) -> None:
        self.game.player_turn = randint(1,2)

    def create(self, player1: str = "player1", player2: str = "player2") -> bool:
        self.game = self.Game(player1, player2)
        self.draw_player_turn()
        return True

    def status(self):
        return {
            "player1": self.game.player1,
            "player2": self.game.player2,
            "player_turn": self.game.player_turn,
            "board": self.game.board,
            "score_board": self.game.score_board,
            "player_win": self.game.player_win
        }

    def move(self, player_id, coordinate: list) -> bool:
        # check game status
        if self.game.finished:
            return False

        # check player
        if self.game.player_turn != player_id or player_id not in range(1,2):
            return False

        # check move
        if (
            len(coordinate) != 2 or \
            coordinate[0] not in range(0,2) or \
            coordinate[1] not in range(0,2) or \
            self.game.board[coordinate[0]][coordinate[1]] != 0 \
        ):
            return False

        # move
        self.game.board[coordinate[0]][coordinate[1]] = player_id

        # check if someone won
        for x in self.all_possible_winning_combinations:
            if not self.game.finished:
                result = 0
                for y in x:
                    result += self.game.board[y[0]][y[1]]

                if result == 3:
                    self.game.player_win = 1
                    self.game.finished = True

                elif result == 6:
                    self.game.player_win = 2
                    self.game.finished = True

        # check i§ drawn
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

        return True


    def ragequit(self, player_id) -> bool:
        if player_id in range(1,2):
            self.game.finished = True
            self.game.player_win = ((player_id + 2) % 2) + 1
            return True
        else:
            return False
