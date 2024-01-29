"""
Tic Tac Toe Player
"""

import math
from collections import defaultdict
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None
MOVES_TAKEN = set()
FILLED_BOARD = { 
    "xRows": defaultdict(lambda: 0), 
    "xCols": defaultdict(lambda: 0),
    "oRows": defaultdict(lambda: 0), 
    "oCols": defaultdict(lambda: 0),
    "xDiag": 0,
    "xAntiDiag": 0,
    "oDiag": 0,
    "oAntiDiag": 0
}
OUT_OF_BOUND_EXCEPTION = "out of bound error"
MOVE_TAKEN_EXCEPTION = "move taken"
WINNER = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def throw_exception_or_continue(condition, exception):
    if (condition):
        raise exception

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

    nextMoves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (board[i][j] == EMPTY):
                curMove = (i, j)
                nextMoves.append(curMove)

    nextMoves = set(nextMoves)
    return nextMoves

def check_bounds(i, j, board):
    return i < 0 or i > len(board) - 1 or j < 0 or j > len(board) - 1

def check_move(i, j, board):
    return board[i][j] != EMPTY

def record_move(i, j, board):
    MOVES_TAKEN.add((i, j))
    FILLED_BOARD["xRows"][i] += board[i][j] == X
    FILLED_BOARD["xCols"][j] += board[i][j] == X
    FILLED_BOARD["xDiag"] += board[i][j] == X and i == j
    FILLED_BOARD["xAntiDiag"] += board[i][j] == X and i + j == len(board) - 1
    FILLED_BOARD["oRows"][i] += board[i][j] == O
    FILLED_BOARD["oCols"][j] += board[i][j] == O
    FILLED_BOARD["oDiag"] += board[i][j] == O and i == j
    FILLED_BOARD["oAntiDiag"] += board[i][j] == O and i + j == len(board) - 1

def count_moves(board):
    count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            count += (board[i][j] == X or board[i][j] == O)

    return count
            

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    i, j = action
    throw_exception_or_continue(check_bounds(i, j, board), BufferError)
    throw_exception_or_continue(check_move(i, j, board), LookupError)

    newBoard = deepcopy(board)
    nextPlayer = player(board) 
    newBoard[i][j] = nextPlayer
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    xRows, xCols = defaultdict(lambda: 0), defaultdict(lambda: 0)
    xDiag, xAntiDiag = 0, 0
    oRows, oCols = defaultdict(lambda: 0), defaultdict(lambda: 0)
    oDiag, oAntiDiag = 0, 0

    def check(xRows, xCols, oRows, oCols, xDiag, oDiag):
        for i in range(len(board)):
            if xRows[i] == len(board) or xCols[i] == len(board):
                return X
            if oRows[i] == len(board) or oCols[i] == len(board):
                return O
            if xDiag == len(board) or xAntiDiag == len(board):
                return X
            if oDiag == len(board) or oAntiDiag == len(board):
                return O
        return None 

    for i in range(len(board)):
        for j in range(len(board)):                
            xRows[i] += board[i][j] == X
            xCols[j] += board[i][j] == X
            xDiag += board[i][j] == X and i == j
            xAntiDiag += board[i][j] == X and i + j == len(board) - 1

            oRows[i] += board[i][j] == O
            oCols[j] += board[i][j] == O
            oDiag += board[i][j] == O and i == j
            oAntiDiag += board[i][j] == O and i + j == len(board) - 1
    
    return check(xRows, xCols, oRows, oCols, xDiag, oDiag)

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    currentPlayer = winner(board)
    if currentPlayer != None:
        WINNER = currentPlayer
        return True

    if (count_moves(board) == len(board) * len(board[0])):
        return True

    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    currentPlayer = winner(board)
    if currentPlayer == X:
        return 1
    if currentPlayer == O:
        return -1

    return 0

def immediateThreeInARowThreatResponse(threat, options, board):
    source, location = threat
    for option in options:
        if source == "row" and option[0] == location[0] and option[1] > location[1]:
            return option
        if source == "col" and option[1] == location[1] and option[0] > location[0]:
            return option
        if source == "diag" and option[0] == option[1] and option[0] > location[0]:
            return option
        if source == "antiDiag" and option[0] + option[1] == len(board) - 1 and option[0] > location[0]:
            return option

    return None

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    currentPlayer = player(board)
    options = actions(board)
    optimal = None
    if currentPlayer == X:
        value, optimal = maxValue(board)
        if value != 1:
            threat = openImmediateThreeInARowThreat(board, X)
            if threat != None:
                option = immediateThreeInARowThreatResponse(threat, options, board)
                optimal = option if option != None else optimal

    if currentPlayer == O:
        value, optimal = minValue(board)
        if optimal != -1:
            threat = openImmediateThreeInARowThreat(board, O)
            if threat != None:
                option = immediateThreeInARowThreatResponse(threat, options, board)
                optimal = option if option != None else optimal

    return optimal

def openImmediateThreeInARowThreat(board, currentPlayer):

    opponentRowCount, selfRowCount = defaultdict(lambda: 0), defaultdict(lambda: 0)
    opponentColCount, selfColCount = defaultdict(lambda: 0), defaultdict(lambda: 0)
    opponentDiagCount, selfDiagCount = 0, 0
    opponentAntiDiagCount, selfAntiDiagCount = 0, 0
    threat = None

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                continue
            opponentRowCount[i] += board[i][j] != currentPlayer
            opponentColCount[j] += board[i][j] != currentPlayer
            selfRowCount[i] += board[i][j] == currentPlayer
            selfColCount[j] += board[i][j] == currentPlayer
            if i == j:
                opponentDiagCount += (board[i][j] != currentPlayer)
                selfDiagCount += board[i][j] == currentPlayer
            if i + j == len(board) - 1:
                opponentAntiDiagCount += (board[i][j] != currentPlayer)
                selfAntiDiagCount += board[i][j] == currentPlayer

            if opponentRowCount[i] == len(board) - 1 and selfRowCount[i] == 0:
                threat = ("row", (i, j))
                break

            if opponentColCount[j] == len(board) - 1 and selfColCount[j] == 0:
                threat = ("col", (i, j))
                break

            if opponentDiagCount == len(board) - 1 and selfDiagCount == 0:
                threat = ("diag", (i, j))
                break

            if opponentAntiDiagCount == len(board) - 1 and selfAntiDiagCount == 0:
                threat = ("antiDiag", (i, j))
                break

    return threat

def maxValue(board):
    choice = None
    if terminal(board):
        return (utility(board), choice)
    v = -1 * math.inf
    choices = actions(board)
    currentPlayer = player(board)
    for action in choices:
        opponentValue = minValue(result(board, action))[0]
        print(currentPlayer, action)
        curMax = max(v, opponentValue)
        if v < curMax:
            choice = action
        v = curMax
        if v == 1:
            break

    return (v, choice)

def minValue(board):
    choice = None
    if terminal(board):
        return (utility(board), choice)
    v = math.inf
    choices = actions(board)
    currentPlayer = player(board)
    for action in choices:
        print(currentPlayer, action)
        opponentValue = maxValue(result(board, action))[0]
        curMin = min(v, opponentValue)
        if v > curMin:
            choice = action
        v = curMin
        if v == -1:
            break

    return (v, choice)
