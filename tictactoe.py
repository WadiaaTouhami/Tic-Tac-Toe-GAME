# Tic Tac Toe Player

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    X_count = 0
    O_count = 0
    for row in board:
        for col in range(len(row)):
            if row[col] == "X":
                X_count += 1
            if row[col] == "O":
                O_count += 1
    return O if X_count > O_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                possible_actions.add((row, col))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("NOT VALID ACTION!")

    row, col = action
    board_copy = copy.deepcopy(board)
    # put X or O on [row][col] position in the board copy
    board_copy[row][col] = player(board)
    return board_copy


def check_rows(board, player):
    for row in range(len(board)):
        if (
            board[row][0] == player
            and board[row][1] == player
            and board[row][2] == player
        ):
            return True
    return False

def check_cols(board, player):
    for col in range(len(board)):
        if (
            board[0][col] == player
            and board[1][col] == player
            and board[2][col] == player
        ):
            return True
    return False

def check_1st_diag(board, player):
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    return False

def check_2nd_diag(board, player):
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for player in [X, O]:
        if (
            check_rows(board, player)
            or check_cols(board, player)
            or check_1st_diag(board, player)
            or check_2nd_diag(board, player)
        ):
            return player

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v

def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v

def minimax(board):

    if terminal(board):
        return None
    
    # if player is X (max_player)
    elif player(board) == X:
        plays = []
        alpha = -math.inf
        beta = math.inf
        for action in actions(board):
            v = min_value(result(board, action), alpha, beta)
            plays.append([v, action])
            alpha = max(alpha, v)
        return sorted(plays, key=lambda x: x[0], reverse=True)[0][1]
    
    # if player is O (min_player)
    elif player(board) == O:
        plays = []
        alpha = -math.inf
        beta = math.inf
        for action in actions(board):
            v = max_value(result(board, action), alpha, beta)
            plays.append([v, action])
            beta = min(beta, v)
        return sorted(plays, key=lambda x: x[0])[0][1]