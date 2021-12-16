import numpy as np


class Color(Enum):
    BLACK = 1
    WHITE = -1


class Board:
    def __init__(self):
        self.board_status = np.zeros(shape=(8, 8))

    def is_tile_taken(self, board_position):
        return not self.board_status[board_position[1]][board_position[0]] == 0

    # TODO: check horizontals, verticals, diagonals
    def is_valid_move(self, board_position, color):  # color is -1 if white, 1 if black
        row = board_position[0]
        col = board_position[1]

    def get_num_possible_moves(self, color):
        count = 0
        for i in range(self.board_status.size):
            for j in range(self.board_status[i].size):
                if self.board_status[i][j] == color and self.is_valid_move(
                    (i, j), color
                ):
                    count += 1
        return count
