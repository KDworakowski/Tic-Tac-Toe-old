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

def print_scoreboard(score_board):
    print("--------------------------------")
    print("            SCOREBOARD       ")
    print("--------------------------------")

    players = list(score_board.keys())
    print("   ", players[0], "    ", score_board[players[0]])
    print("   ", players[1], "    ", score_board[players[1]])

    print("--------------------------------\n")

def check_win(player_position, current_player):

    all_possible_winning_combinations = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8]]

    for x in all_possible_winning_combinations:
        if all(y in player_position[current_player] for y in x):
            return True
        return False

def check_draw(player_position):
    if len(player_position['X'] + len(player_position['O'])) == 9:
        return True
    return False

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

        print_scoreboard(score_boards)

        if current_player == player1:
            current_player = player2
        else:
            current_player = player1
