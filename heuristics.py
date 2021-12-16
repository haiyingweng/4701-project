from enum import Enum


class Color(Enum):
    BLACK = 0
    WHITE = 1


def disc_difference(color):
    print("calculate disc difference")
    # TODO: count white and black on board
    white_count = 0
    black_count = 0

    curr_count = white_count if color is Color.WHITE else black_count
    opponent_count = white_count if color is Color.BLACK else white_count

    return 100 * (curr_count - opponent_count) / (curr_count + opponent_count)


def immediate_mobility(color):
    print("calculate immediate mobility")
    # TODO: find number of possible moves for black and white
    white_moves = 0
    black_moves = 0

    curr_moves = white_moves if color is Color.WHITE else black_moves
    opponent_moves = white_moves if color is Color.BLACK else white_moves

    if curr_moves + opponent_moves != 0:
        return 100 * (curr_moves - opponent_moves) / (curr_moves + opponent_moves)
    else:
        return 0


def potential_mobility(color):
    print("calculate potential mobility")
    # TODO: find number of potential  moves for black and white
    white_moves = 0
    black_moves = 0

    curr_moves = white_moves if color is Color.WHITE else black_moves
    opponent_moves = white_moves if color is Color.BLACK else white_moves

    if curr_moves + opponent_moves != 0:
        return 100 * (curr_moves - opponent_moves) / (curr_moves + opponent_moves)
    else:
        return 0
