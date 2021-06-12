class Logic():

    class Game():
        player1 = ""
        player2 = ""

        board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        player_turn = 0

        score_board = {}

        def __init__(self, player1: str, player2: str) -> None:
            self.player1 = player1
            self.player2 = player2
            self.score_board = {self.player1: 0, self.player2: 0}


    def __init__(self) -> None:
        self.game = False

    def create(self, player1: str = "player1", player2: str = "player2") -> bool:
        self.game = self.Game(player1, player2)
        return True

    def status(self):
        return {
            "player1": self.game.player1,
            "player2": self.game.player2,
            "player_turn": self.game.player_turn,
            "board": self.game.board,
            "score_board": self.game.score_board
        }
"""
This function is responsible for printing tic tac toe.
"""
def print_tic_tac_toe(values):
    print("\n")
    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(values[0], values[1], values[2]))
    print('\t_____|_____|_____')

    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(values[3], values[4], values[5]))
    print('\t_____|_____|_____')

    print("\t     |     |")

    print("\t  {}  |  {}  |  {}".format(values[6], values[7], values[8]))
    print("\t     |     |")
    print("\n")

"""
This function is responsible for printing scoreboard, scoreboard is printed after every game.
"""
def print_scoreboard(score_board):
    print("\t--------------------------------")
    print("\t              SCOREBOARD       ")
    print("\t--------------------------------")

    players = list(score_board.keys())
    print("\t   ", players[0], "\t    ", score_board[players[0]])
    print("\t   ", players[1], "\t    ", score_board[players[1]])

    print("--------------------------------\n")

"""
This function is responsible for checking which player won.
It contains winning combinations, while "X" or "O" will be on
these places then one of the players that have his "X" or "O" on these places will win.
Basically if the current player will place his "X" or "O" and after this move player meet the requirements the player win.
"""
def check_win(player_position, current_player):

    all_possible_winning_combinations = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8]]

    for x in all_possible_winning_combinations:
        # return all(y in player_position[current_player] for y in x):
        if all(y in player_position[current_player] for y in x):
            return True
    return False

"""
This function is responsible for checking is there a draw.
When all of the player placed "X" or "O" 9 times in total, and there's no win, there's draw.
"""
def check_draw(player_position):
    return len(player_position['X']) + len(player_position['O']) == 9

"""
This function is responsible for every single game.
It asks the player for input where he want to place his "X" or "O", if the player will
put the wrong number, there's an error which asks the player to try again with chosing
where the player want to put his "X" or "O". Also, if the player will want to place his "X" or "O" in
the place that is already ocupied, there will be a similar error. If one of the players won the game or
there is a draw, then it's saying which player won or there is a draw. After ecery move it's changing
which player is moving next.
"""
def single_game(current_player):

    values = [' ' for x in range(9)]

    player_position = {'X':[], 'O':[]}

    while True:
        print_tic_tac_toe(values)

        try:
            print("Player ", current_player, " turn. Which box? : ", end="")
            move = int(input())
        except ValueError:
            print("Wrong input! Try again!")
            continue

        if move < 1 or move > 9:
            print("Wrong input! Try again!")
            continue

        if values[move-1] != ' ':
            print("Place already filled. Try again!")
            continue

        values[move-1] = current_player

        player_position[current_player].append(move)

        if check_win(player_position, current_player):
            print_tic_tac_toe(values)
            print("Player ", current_player, " has won the game!")
            print("\n")
            return current_player

        if check_draw(player_position):
            print_tic_tac_toe(values)
            print("Game drawn")
            print("\n")
            return 'D'

        if current_player == 'X':
            current_player = 'O'
        else:
            current_player = 'X'

if __name__ == "__main__":

    print("Player 1")
    player1 = input("Enter the name : ")
    print("\n")

    print("Player 2")
    player2 = input("Enter the name : ")
    print("\n")

    current_player = player1

    player_choice = {'X' : "", 'O' : ""}

    options = ['X', 'O']

    score_board = {player1: 0, player2: 0}
    print_scoreboard(score_board)

    while True:
        print("Turn to choose for", current_player)
        print("Enter 1 for X")
        print("Enter 2 for O")
        print("Enter 3 to Quit")

        try:
            choice = int(input())
        except ValueError:
            print("Wrong number! Try Again!\n")
            continue

        if choice == 1:
            player_choice['X'] = current_player
            if current_player == player1:
                player_choice['O'] = player2
            else:
                player_choice['O'] = player1

        elif choice == 2:
            player_choice['O'] = current_player
            if current_player == player1:
                player_choice['X'] = player2
            else:
                player_choice['X'] = player1

        elif choice == 3:
            print("Final scores")
            print_scoreboard(score_board)
            break

        else:
            print("Wrong choice! Try again!\n")

        winner = single_game(options[choice-1])

        if winner != 'D' :
            player_won = player_choice[winner]
            score_board[player_won] = score_board[player_won] + 1

        print_scoreboard(score_board)

        if current_player == player1:
            current_player = player2
        else:
            current_player = player1

# After every game it change the "X" or "O" selection
# so if player 1 was chosing do he wants to be an "X" or "O", then in the next game player 2 will be
# chosing do he wants to be an "X" or "O".
