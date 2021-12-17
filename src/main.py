from board import *
from heuristics import *
from tkinter import *
import numpy as np

board_size = 560
board_color = "#485d3f"
piece_size = (board_size / 8 - 10) / 2


class Othello:
    def __init__(self):
        self.window = Tk()
        self.window.title("Othello")
        self.canvas = Canvas(
            self.window, width=board_size, height=board_size, bg=board_color
        )
        self.canvas.pack()
        self.window.bind("<Button-1>", self.click)

        self.init_board()
        self.player_Bs_move = (
            True  # track which player's turn. Black always moves first.
        )
        self.num_moves = 0
        self.board = Board()
        # self.board_status = np.zeros(shape=(8, 8))  # white = -1, empty = 0, black = 1
        for i in range(3, 5):
            for j in range(3, 5):
                status = -1 if i == j else 1
                self.board.board_status[i][j] = status

    def init_board(self):
        for i in range(7):
            self.canvas.create_line(
                (i + 1) * board_size / 8, 0, (i + 1) * board_size / 8, board_size
            )

        for i in range(7):
            self.canvas.create_line(
                0, (i + 1) * board_size / 8, board_size, (i + 1) * board_size / 8
            )

        for i in range(3, 5):
            for j in range(3, 5):
                board_position = np.array([i, j])
                color = "white" if i == j else "black"
                self.draw_piece(board_position, color)

    def mainloop(self):
        self.window.mainloop()

    def draw_piece(self, board_position, color):
        board_position = np.array(board_position)
        pixel_position = self.board_to_pixel_position(board_position)
        self.canvas.create_oval(
            pixel_position[0] - piece_size,
            pixel_position[1] - piece_size,
            pixel_position[0] + piece_size,
            pixel_position[1] + piece_size,
            fill=color,
            outline=color,
        )

    # returns pixel coords of center of board tile, e.g. [35. 35.] for board_position = [0 0]
    def board_to_pixel_position(self, board_position):
        board_position = np.array(board_position, dtype=int)
        return (board_size / 8) * board_position + board_size / 16

    # returns coords of board tile [col, row], e.g. [0 0]
    def pixel_to_board_position(self, pixel_position):
        pixel_position = np.array(pixel_position)
        return np.array(pixel_position // (board_size / 8), dtype=int)

    def click(self, event):
        pixel_position = [event.x, event.y]
        board_position = self.pixel_to_board_position(pixel_position)
        print("tile position:", board_position)

        is_valid_move = self.board.is_valid_move(board_position, 1 if self.player_Bs_move else -1)
        if not is_valid_move: print("sorry you can't put your piece there ;-;")

        if not self.board.is_tile_taken(board_position) \
            and is_valid_move:
            color = "black" if self.player_Bs_move else "white"
            self.draw_piece(board_position, color)
            self.board.board_status[board_position[1]][board_position[0]] = (
                1 if color == "black" else -1
            )
            self.player_Bs_move = not self.player_Bs_move
            self.num_moves += 1
            print("number of moves made:", self.num_moves)
            print(self.board.board_status)

    # TODO def flip_pieces(self, board_position):


game = Othello()
game.mainloop()
