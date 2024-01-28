"""
Tic Tac Toe Player
"""

import math
from collections import defaultdict
from copy import deepcopy

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
    xMoves = 0
    oMoves = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            xMoves += board[i][j] == X
            oMoves += board[i][j] == O
        
    return O if xMoves > oMoves else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != X and board[i][j] != O:
                moves.append((i, j))

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newBoard = deepcopy(board)
    i, j = action
    nextPlayer = player(board) 
    newBoard[i][j] = nextPlayer


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win = utility(board)
    if win == 0:
        return X
    if win == 255:
        return O
    return win


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # raise NotImplementedError
    xRowCount, oRowCount = 0, 0
    xColCount, oColCount = 0, 0
    xDiagCount, xAntiDiagCount = 0, 0
    oDiagCount, oAntiDiagCount = 0, 0
    win = -1

    for i in range(len(board)):
        for j in range(len(board)):
            if (board[i][j] == 0):
                xRowCount += 1
                xColCount += 1
            if (board[i][j] == 255):
                oRowCount += 1
                oColCount += 1

            if i == j:
                xDiagCount += board[i][j] == X
                oDiagCount += board[i][j] == O
            if i + len(board) - 1 == j or j + len(board) - 1 == i:
                xAntiDiagCount += board[i][j] == X
                oAntiDiagCount += board[i][j] == O

            if xRowCount == len(board) or xColCount == len(board) or xDiagCount == len(board) or xAntiDiagCount == len(board):
                win = X
                break
            if oRowCount == len(board) or oColCount == len(board) or oDiagCount == len(board) or oAntiDiagCount == len(board):
                win = O
                break
    
    return win

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board) == X:
        return 1
    if terminal(board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    optimal = 0
    maxResult = -1 * math.inf
    for a, i in enumerate(actions(board)):
        if a > maxResult:
            optimal = i
            
    return optimal

def maxValue(board):
    value = utility(board)
    if value != -1:
        return value
    v = -1 * math.inf
    for a in actions(board):
        v = max(v, minValue(result(board, a)))
    return v

def minValue(board):
    value = utility(board)
    if value != -1:
        return value
    v = math.inf
    for a in actions(board):
        v = min(v, maxValue(result(board, a)))
    return v
