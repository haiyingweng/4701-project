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


def corner_difference(board, color):
    print("calculate corner count difference")
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    white_corner_val = 0
    black_corner_val = 0

    for i, j in corners:
        if board.board_status[i][j] == 1:
            black_corner_val += 1
        elif board.board_status[i][j] == -1:
            white_corner_val += 1

    curr_corner_val = white_corner_val if color is Color.WHITE else black_corner_val
    opponent_corner_val = white_corner_val if color is Color.BLACK else black_corner_val

    return (
        100
        * (curr_corner_val - opponent_corner_val)
        / (curr_corner_val + opponent_corner_val + 1)
    )


# corners and potential corners weighted positively and giving opponent corners weighted negatively
def corner_value(board, color):
    print("calculate corner value")
    weights = np.array(
        [
            [200, -100, 100, 50, 50, 100, -100, 200],
            [-100, -200, -50, -50, -50, -50, -200, -100],
            [100, -50, 100, 0, 0, 100, -50, 100],
            [50, -50, 0, 0, 0, 0, -50, 50],
            [50, -50, 0, 0, 0, 0, -50, 50],
            [100, -50, 100, 0, 0, 100, -50, 100],
            [-100, -200, -50, -50, -50, -50, -200, -100],
            [200, -100, 100, 50, 50, 100, -100, 200],
        ]
    )

    if board.board_status[0][0] != 0:
        for i in range(len(weights) // 2):
            for j in range(len(weights[i]) // 2):
                if i != 0 and j != 0:
                    weights[i][j] = 0
    if board.board_status[0][7] != 0:
        for i in range(len(weights) // 2):
            for j in range(len(weights[i]) // 2, len(weights[i])):
                if i != 0 and j != 7:
                    weights[i][j] = 0
    if board.board_status[7][0] != 0:
        for i in range(len(weights) // 2, len(weights)):
            for j in range(len(weights[i]) // 2):
                if i != 7 and j != 0:
                    weights[i][j] = 0
    if board.board_status[7][7] != 0:
        for i in range(len(weights) // 2, len(weights)):
            for j in range(len(weights[i]) // 2, len(weights[i])):
                if i != 7 and j != 7:
                    weights[i][j] = 0

    sum = np.sum(board.board_status * weights)
    white_corner_val = -1 * sum
    black_corner_val = sum

    return white_corner_val if color is Color.WHITE else black_corner_val
