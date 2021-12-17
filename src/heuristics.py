import numpy as np
from board import *

# all methods' arg color should be Color.WHITE or Color.BLACK

# TODO: calculate the weighted score of the current state of board
def calculate_state_score(board, color):
    # print("calculate score of state")
    if board.is_end_game():
        white_count = np.count_nonzero(board.board_status == -1)
        black_count = np.count_nonzero(board.board_status == 1)
        curr_count = white_count - black_count if color is Color.WHITE else black_count - white_count
        return 1000*curr_count
    
    discs_count = np.count_nonzero(board.board_status)
    # print('disc_difference',disc_difference(board, color))
    # print('immediate_mobility',immediate_mobility(board, color))
    # print('potential_mobility',potential_mobility(board, color))
    # print('corner_difference',corner_difference(board, color))
    # print('corner_value',corner_value(board, color))
    # print('stability',stability(board, color))

    if discs_count <= 20: # start of game
        return 100*immediate_mobility(board, color) \
        +100*potential_mobility(board, color) \
        +1000*corner_difference(board, color) \
        +100*corner_value(board, color) \
        +1000*stability(board, color)
    elif discs_count <= 56: # mid game
        return 100*disc_difference(board, color) \
        +10*immediate_mobility(board, color) \
        +10*potential_mobility(board, color) \
        +1000*corner_difference(board, color) \
        +100*corner_value(board, color) \
        +1000*stability(board, color)
    else: # towards end of game
       return 1000*disc_difference(board, color) \
        +100*corner_difference(board, color) \
        +100*corner_value(board, color) \
        +100*stability(board, color)


def disc_difference(board, color):
    white_count = np.count_nonzero(board.board_status == -1)
    black_count = np.count_nonzero(board.board_status == 1)

    curr_count = white_count if color is Color.WHITE else black_count
    opponent_count = white_count if color is Color.BLACK else black_count

    return 100 * (curr_count - opponent_count) / (curr_count + opponent_count)


def immediate_mobility(board, color):
    white_moves = board.get_num_possible_moves(-1)
    black_moves = board.get_num_possible_moves(1)

    curr_moves = white_moves if color is Color.WHITE else black_moves
    opponent_moves = white_moves if color is Color.BLACK else black_moves

    if curr_moves + opponent_moves != 0:
        return 100 * (curr_moves - opponent_moves) / (curr_moves + opponent_moves)
    else:
        return 0


def potential_mobility(board, color):
    white_moves = board.get_num_potential_moves(-1)
    black_moves = board.get_num_potential_moves(1)

    curr_moves = white_moves if color is Color.WHITE else black_moves
    opponent_moves = white_moves if color is Color.BLACK else black_moves

    if curr_moves + opponent_moves != 0:
        return 100 * (curr_moves - opponent_moves) / (curr_moves + opponent_moves)
    else:
        return 0


def corner_difference(board, color):
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
    weights = np.array(
        [
            [20, -10, 10, 5, 5, 10, -10, 20],
            [-10, -20, -5, -5, -5, -5, -20, -10],
            [10, -5, 10, 0, 0, 10, -5, 10],
            [5, -5, 0, 0, 0, 0, -5, 5],
            [5, -5, 0, 0, 0, 0, -5, 5],
            [10, -5, 10, 0, 0, 10, -5, 10],
            [-10, -20, -5, -5, -5, -5, -20, -10],
            [20, -10, 10, 5, 5, 10, -10, 20],
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


def stability(board, color):
    white_stability = board.get_num_stable_discs(-1)
    black_stability = board.get_num_stable_discs(1)

    curr_stb = white_stability if color is Color.WHITE else black_stability
    opponent_stb = white_stability if color is Color.BLACK else black_stability

    return 100 * (curr_stb - opponent_stb) / (curr_stb + opponent_stb + 1)
