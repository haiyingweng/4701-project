from enum import Enum
import numpy as np


class Color(Enum):
    BLACK = 1
    WHITE = -1


class Board:
    def __init__(self):
        self.board_size = 8
        self.board_status = np.zeros(shape=(8, 8))

    def is_tile_taken(self, board_position):
        return not self.board_status[board_position[1]][board_position[0]] == 0

    # checks whether there are flippable tiles in arr1 or arr2
    # where:
    #  arr1 = array of values "before" the placed piece
    #  arr2 = array of values "after" the placed piece
    def contains_sandwich(self, arr1, arr2, color):
        # indices of [color] pieces in arr1, arr2 respectively
        idx1 = len(arr1) - np.where(arr1[::-1] == color)[0] - 1
        idx2 = np.where(arr2 == color)[0]

        return ((len(idx1) > 0 and idx1[0] != (len(arr1) - 1) and np.all(arr1[(idx1[0] + 1):] == -color))
                or (len(idx2) > 0 and idx2[0] != 0 and np.all(arr2[:idx2[0]] == -color)))

    def is_valid_move(self, board_position, color):  # color is -1 if white, 1 if black
        col_idx = board_position[0]
        row_idx = board_position[1]

        if self.is_tile_taken(board_position):
            return False

        # check horizontals
        row_front = self.board_status[row_idx, :col_idx]
        row_back = self.board_status[row_idx, col_idx+1:]
        if self.contains_sandwich(row_front, row_back, color):
            return True

        # check verticals
        col_top = self.board_status[:row_idx, col_idx]
        col_bottom = self.board_status[row_idx+1:, col_idx]
        if self.contains_sandwich(col_top, col_bottom, color):
            return True

        # check diagonals
        offset = col_idx - row_idx
        diag = np.diagonal(self.board_status, offset)
        upper_left_diag = diag[:(col_idx if offset < 0 else row_idx)]
        lower_right_diag = diag[(col_idx if offset < 0 else row_idx)+1:]
        if self.contains_sandwich(upper_left_diag, lower_right_diag, color):
            return True

        flipped_offset = len(self.board_status) - 1 - col_idx - row_idx
        opposite_diag = np.diagonal(
            np.fliplr(self.board_status), flipped_offset)
        upper_right_diag = opposite_diag[:(
            len(self.board_status) - col_idx - 1 if flipped_offset < 0 else row_idx)]
        lower_left_diag = opposite_diag[(
            len(self.board_status) - col_idx - 1 if flipped_offset < 0 else row_idx) + 1:]
        if self.contains_sandwich(upper_right_diag, lower_left_diag, color):
            return True

    # returns array of indices of flippable pieces
    def get_flippable_pieces(self, board_position, color):
        col_idx = board_position[0]
        row_idx = board_position[1]
        indices = []

        # flip horizontals
        row_front = self.board_status[row_idx, :col_idx]
        row_back = self.board_status[row_idx, col_idx+1:]

        if self.contains_sandwich(row_front, [], color):
            sandwich_idx = (len(row_front) -
                            np.where(row_front[::-1] == color)[0] - 1)[0]
            for i in range(sandwich_idx+1, col_idx):
                indices.append([row_idx, i])

        if self.contains_sandwich([], row_back, color):
            sandwich_idx = np.where(row_back == color)[0][0]
            for i in range(col_idx + 1, sandwich_idx + col_idx + 1):
                indices.append([row_idx, i])

        # flip verticals
        col_top = self.board_status[:row_idx, col_idx]
        col_bottom = self.board_status[row_idx+1:, col_idx]

        if self.contains_sandwich(col_top, [], color):
            sandwich_idx = (
                len(col_top) - np.where(col_top[::-1] == color)[0] - 1)[0]
            for i in range(sandwich_idx + 1, row_idx):
                indices.append([i, col_idx])

        if self.contains_sandwich([], col_bottom, color):
            sandwich_idx = (len(col_bottom) -
                            np.where(col_bottom[::-1] == color)[0] - 1)[0]
            for i in range(row_idx + 1, sandwich_idx + row_idx + 1):
                indices.append([i, col_idx])

        # flip diagonals
        offset = col_idx - row_idx
        diag = np.diagonal(self.board_status, offset)
        upper_left_diag = diag[:(col_idx if offset < 0 else row_idx)]
        lower_right_diag = diag[(col_idx if offset < 0 else row_idx)+1:]

        if self.contains_sandwich(upper_left_diag, [], color):
            sandwich_idx = (
                len(upper_left_diag) - np.where(upper_left_diag[::-1] == color)[0] - 1)[0]
            for i in range(1, len(upper_left_diag) - sandwich_idx):
                indices.append([row_idx - i, col_idx - i])

        if self.contains_sandwich([], lower_right_diag, color):
            sandwich_idx = (len(lower_right_diag) -
                            np.where(lower_right_diag[::-1] == color)[0] - 1)[0]
            for i in range(1, sandwich_idx + 1):
                indices.append([row_idx + i, col_idx + i])

        flipped_offset = len(self.board_status) - 1 - col_idx - row_idx
        opposite_diag = np.diagonal(
            np.fliplr(self.board_status), flipped_offset)
        upper_right_diag = opposite_diag[:(
            len(self.board_status) - col_idx - 1 if flipped_offset < 0 else row_idx)]
        lower_left_diag = opposite_diag[(
            len(self.board_status) - col_idx - 1 if flipped_offset < 0 else row_idx) + 1:]

        if self.contains_sandwich(upper_right_diag, [], color):
            sandwich_idx = (
                len(upper_right_diag) - np.where(upper_right_diag[::-1] == color)[0] - 1)[0]
            for i in range(1, len(upper_right_diag) - sandwich_idx):
                indices.append([row_idx - i, col_idx + i])

        if self.contains_sandwich([], lower_left_diag, color):
            sandwich_idx = (len(lower_left_diag) -
                            np.where(lower_left_diag[::-1] == color)[0] - 1)[0]
            for i in range(1, sandwich_idx + 1):
                indices.append([row_idx + i, col_idx - i])
                
        return indices

    # end game if no more empty tiles or impossible for either player to make another move
    def is_end_game(self):
        is_end = not 0 in self.board_status or (self.get_num_possible_moves(1) == 0 and self.get_num_possible_moves(0) == 0)
        return is_end

    def get_possible_moves(self, color):
        moves = []
        for i in range(len(self.board_status)):
            for j in range(len(self.board_status[i])):
                if self.board_status[i][j] == 0 and self.is_valid_move((j, i), color):
                    moves.append((i, j))
        return moves

    def get_num_possible_moves(self, color):
        return len(self.get_possible_moves(color))

    # count number of opponent's discs that are next to an empty space
    def get_num_potential_moves(self, color):
        count = 0
        for i in range(len(self.board_status)):
            for j in range(len(self.board_status[i])):
                if (
                    i - 1 >= 0
                    and self.board_status[i - 1][j] == -color
                    and self.board_status[i][j] == 0
                ):
                    count += 1
                elif (
                    j - 1 >= 0
                    and self.board_status[i][j - 1] == -color
                    and self.board_status[i][j] == 0
                ):
                    count += 1
                elif (
                    i + 1 < len(self.board_status)
                    and self.board_status[i + 1][j] == -color
                    and self.board_status[i][j] == 0
                ):
                    count += 1
                elif (
                    j + 1 < len(self.board_status[i])
                    and self.board_status[i][j + 1] == -color
                    and self.board_status[i][j] == 0
                ):
                    count += 1
                elif (
                    i - 1 >= 0
                    and j - 1 >= 0
                    and self.board_status[i - 1][j - 1] == -color
                    and self.board_status[i][j] == 0
                ):
                    count += 1
                elif (
                    i - 1 >= 0
                    and j + 1 < len(self.board_status[i])
                    and self.board_status[i - 1][j + 1] == -color
                    and self.board_status[i][j] == 0
                ):
                    count += 1
                elif (
                    i + 1 < len(self.board_status)
                    and j - 1 >= 0
                    and self.board_status[i + 1][j - 1] == -color
                    and self.board_status[i][j] == 0
                ):
                    count += 1
                elif (
                    i + 1 < len(self.board_status)
                    and j + 1 < len(self.board_status[i])
                    and self.board_status[i + 1][j + 1] == -color
                    and self.board_status[i][j] == 0
                ):
                    count += 1
        return count

    # count number of stable discs
    def get_num_stable_discs(self, color): 
      res1 = self.get_top_left_stable_discs(color)
      res2 = self.get_top_right_stable_discs(color)
      res3 = self.get_bottom_left_stable_discs(color)
      res4 = self.get_bottom_right_stable_discs(color)
      stable_discs = res1 | res2 | res3 | res4
      stable_discs = set(stable_discs)
      return len(stable_discs)

    # count stable discs starting from corner (0, 0)
    def get_top_left_stable_discs(self, color):
      stable_discs = set()
      # iterate horizontally 
      for j in range(self.board_size):
          if (self.board_status[0][j] == color):
              # iterate vertically 
              for i in range(self.board_size):
                  if (self.board_status[i][j] == color):
                      stable_discs.add((i, j))
                  else:
                      break
          else:
              break
      return stable_discs

    # count stable discs starting from corner (0, 7)
    def get_top_right_stable_discs(self, color):
      stable_discs = set()
      for j in range(self.board_size-1, -1, -1):
          if (self.board_status[0][j] == color):
              for i in range(self.board_size):
                  if (self.board_status[i][j] == color):
                      stable_discs.add((i, j))
                  else:
                      break
          else:
              break
      return stable_discs

    # count stable discs starting from corner (7, 0)
    def get_bottom_left_stable_discs(self, color):
      stable_discs = set()
      for j in range(self.board_size):
          if (self.board_status[self.board_size-1][j] == color):
              for i in range(self.board_size-1, -1, -1):
                  if (self.board_status[i][j] == color):
                      stable_discs.add((i, j))
                  else:
                      break
          else:
              break
      return stable_discs

    # count stable discs starting from corner (7, 7)
    def get_bottom_right_stable_discs(self, color):
      stable_discs = set()
      for j in range(self.board_size-1, -1, -1):
          if (self.board_status[self.board_size-1][j] == color):
              for i in range(self.board_size-1, -1, -1):
                  if (self.board_status[i][j] == color):
                      stable_discs.add((i, j))
                  else:
                      break
          else:
              break
      return stable_discs

