import tictactoe as ttt

X = 'X'
O = "O"
EMPTY = None

board0 = [[O, X, O],[O, X, X],[X, EMPTY, EMPTY]]
board1 = [[None, 'X', 'O'], [None, 'X', None], [None, None, None]]
board2 = [['O', 'X', 'O'], ['X', 'X', None], ['X', 'O', None]] 
board3 = [['X', 'X', 'X'], ['O', 'O', None], [None, None, None]]
board4 = [[None, None, None], ['X', 'O', 'O'], [None, 'X', None]] 
board5 = [['X', 'X', 'X'], ['O', 'O', None], [None, None, None]]

print(ttt.player(board5))
print(ttt.minimax(board5))

