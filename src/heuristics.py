import numpy as np
from board import *

# TODO: calculate the weighted score of the current state of board
def calculate_state_score(board):
    print("calculate score of state")


def disc_difference(board, color):
    print("calculate disc difference")
    white_count = np.count_nonzero(board.board_status == -1)
    black_count = np.count_nonzero(board.board_status == 1)

    curr_count = white_count if color is Color.WHITE else black_count
    opponent_count = white_count if color is Color.BLACK else black_count

    return 100 * (curr_count - opponent_count) / (curr_count + opponent_count)


def immediate_mobility(board, color):
    print("calculate immediate mobility")
    white_moves = board.get_num_possible_moves(-1)
    black_moves = board.get_num_possible_moves(1)

    curr_moves = white_moves if color is Color.WHITE else black_moves
    opponent_moves = white_moves if color is Color.BLACK else black_moves

    if curr_moves + opponent_moves != 0:
        return 100 * (curr_moves - opponent_moves) / (curr_moves + opponent_moves)
    else:
        return 0


def potential_mobility(board, color):
    print("calculate potential mobility")
    white_moves = board.get_num_potential_moves(-1)
    black_moves = board.get_num_potential_moves(1)

    curr_moves = white_moves if color is Color.WHITE else black_moves
    opponent_moves = white_moves if color is Color.BLACK else black_moves

    if curr_moves + opponent_moves != 0:
        return 100 * (curr_moves - opponent_moves) / (curr_moves + opponent_moves)
    else:
        return 0


def corner_value(color):
    print("calculate corner")
    # TODO: find corner values for black and white
    white_corner_val = 0
    black_corner_val = 0

    curr_corner_val = white_corner_val if color is Color.WHITE else black_corner_val
    opponent_corner_val = white_corner_val if color is Color.BLACK else black_corner_val

    if curr_corner_val + opponent_corner_val != 0:
        return (
            100
            * (curr_corner_val - opponent_corner_val)
            / (curr_corner_val + opponent_corner_val)
        )
    else:
        return 0
