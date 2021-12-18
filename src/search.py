from heuristics import *
from board import *
import math

def flip_color(color):
    if color == Color.WHITE:
        return Color.BLACK
    return Color.WHITE
       
# where color is Color.WHITE or Color.BLACK
def min_max(board, depth, color):
    if color == Color.WHITE:
        best = [-1, -1, float('-inf')]
    else:
        best = [-1, -1, float('inf')]

    moves = board.get_possible_moves(-1 if Color.WHITE else 1)

    if depth == 0 or board.is_end_game() or len(moves) == 0:
        score = calculate_state_score(board, color)
        return [-1, -1, score]

    for (i, j) in moves:
        board.board_status[i][j] = -1 if Color.WHITE else 1
        score = min_max(board, depth - 1, flip_color(color))
        board.board_status[i][j] = 0
        score[0], score[1] = i, j
    
        if color == Color.WHITE:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best

def ai_move(board):
    if board.get_num_possible_moves == 1:
        return board.get_possible_moves[0]

    [i, j, score] = min_max(board, 3, Color.WHITE)
    return (i, j)
