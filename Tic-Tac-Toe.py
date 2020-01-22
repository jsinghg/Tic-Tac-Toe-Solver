#!/usr/bin/env python3
from math import inf as infinity
from random import choice

# Global variable representing the game of the board
board = [
         [' ', ' ', ' '],
         [' ', ' ', ' '],
         [' ', ' ', ' ']
]

# Human has the value -1, and Computer has +1
HUMAN = -1
COMP = +1


# game_win checks if the "player" has won the game by checking for
#   all the possible winning states
# Param:
#   state: current state of the board
#   player:  of which player you want to check
def game_win(state, player):
    # There are 8 winning possibilities:
    # - 3 Rows
    # - 3 Columns
    # - 2 Diagonals

    winning_states = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[0][2], state[1][1], state[2][0]]
    ]
    if [player, player, player] in winning_states:
        return True
    return False


# empty_cells returns the positions of the empty cells
#   in the current state
# Param:
#   state : Current State
def empty_cells(state):
    cells = [] # List containing the positions of empty cell
    for x in range(0, 3):
        for y in range(0, 3):
            if state[x][y] == ' ':
                cells.append([x, y])
    return cells


# print_board() prints the whole board
def print_board(state):
    str_line = '---------------'
    print('\n' + str_line)
    for row in state:
        for cell in range(0,3):
            print(f'| {row[cell]} |', end='')
        print('\n' + str_line)


# board_filled() returns true if the all the positions of the board are occupied
#   otherwise it returns false
def board_filled(state):
    for row in state:
        for j in range(0, 3):
            if row[j] == ' ':
                return False
    return True


# Checks if the desired position is not pre-occupied
# Param : posn - position to move to
#              - of the form [x, y]
def check_move(posn):
    if board[posn[0]][posn[1]] == ' ':
        return True
    return False


def game_over(state):
    return board_filled(state) or game_win(state, 'X') or game_win(state, 'O')


def result(state, h_choice, c_choice):
    if game_win(state, c_choice):
        score = +1
    elif game_win(state, h_choice):
        score = -1
    else:
        score = 0
    return score


def invert_player(player):
    if player == 'X':
        return 'O'
    return 'X'


def minimax(state, depth, player_choice, h_choice, c_choice):
    # Worst case possible
    best = [-1, -1, -infinity] if player_choice == c_choice else [-1, -1, +infinity]
    # best : best move possible
    # format : [x, y, value]
    if depth == 0 or game_over(state):
        score = result(state, h_choice, c_choice)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player_choice
        #print_board(state)
        #print(best)
        #print(depth)
        #input("Continue ? ")
        score = minimax(state, depth - 1, invert_player(player_choice), h_choice, c_choice)
        state[x][y] = ' '
        score[0], score[1] = x, y
        if player_choice == c_choice:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score
    return best


def human_move(h_choice, c_choice):
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2]
    }

    # ERROR HANDLING
    # CASES:
    # 1: THE CHOICE IS NOT BETWEEN 1 AND 9
    # 2: THE POSITION IS ALREADY OCCUPIED
    # 3. CHECK FOR KEYBOARD INTERRUPT KEYBOARD ERROR
    # EASIEST APPROACH : MAKE A FUNCTION TO CHECK
    try:
        move = int(input("Its your turn Human, choose 1-9 : "))
        # Checks if the input is between 1 and 9
        print(move)
        while move > 9 or move < 1 or not check_move(moves[move]):
            move = int(input("Bad Choice, choose 1-9 : "))
        new_posn = moves[move]
        board[new_posn[0]][new_posn[1]] = h_choice
    except (KeyboardInterrupt, KeyError, EOFError):
        print("You Fucked Up")
        exit()


def comp_move(h_choice, c_choice):
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    print(f'Computer turn [{c_choice}]')

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, c_choice, h_choice, c_choice)
        print(move)
        x, y = move[0], move[1]
    board[x][y] = c_choice
    print_board(board)


# Driver Function
def main():
    human_choice = '' # the symbol that represents the choice of the Human
    comp_choice = '' # the symbol that represents the choice of the Computer
    first = '' # Represents if the player wants to have the first turn or not
    turn = '' # Takes care of the whose turn it is
    while human_choice != '0' and human_choice != 'X':
        try:
            human_choice = input("Enter your choice of the symbol X or O: ").upper()
            first = input("Do you want to play first? (Y/N) :").upper()
        except(KeyboardInterrupt, EOFError):
            print("The game has been executed")
            exit()
        except(KeyError, ValueError):
            print("Bad choice of the value")
    print(human_choice)
    # assigning the value of comp_choice according to the choice made by human
    comp_choice = 'O' if human_choice == 'X' else 'O'
    turn = 0 if first == 'Y' else 1
    if board_filled(board):
        exit()
    while not game_over(board):
        human_move(human_choice, comp_choice)
        comp_move(human_choice, comp_choice)
        #print_board(board)


if __name__ == "__main__":
    main()