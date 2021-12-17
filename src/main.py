from board import *
from heuristics import *
from tkinter import *
from search import *
import numpy as np
import time

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
        self.label = Label(self.window, text="It's your turn!", font=("Arial", 25))
        self.canvas.pack()
        self.label.pack()

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
                0, (i + 1) * board_size /
                8, board_size, (i + 1) * board_size / 8
            )

        for i in range(3, 5):
            for j in range(3, 5):
                board_position = np.array([i, j])
                color = -1 if i == j else 1
                self.draw_piece(board_position, color)

    def mainloop(self):
        self.window.mainloop()

    # color is -1 if white, 1 if black
    def draw_piece(self, board_position, color):
        board_position = np.array(board_position)
        pixel_position = self.board_to_pixel_position(board_position)
        color = 'black' if color == 1 else 'white'
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
        self.label["text"] = ""
        if not self.board.is_end_game():
            pixel_position = [event.x, event.y]
            board_position = self.pixel_to_board_position(pixel_position)
            print("tile position:", board_position)
            color = 1 if self.player_Bs_move else -1
            is_valid_move = self.board.is_valid_move(board_position, color)
            if not is_valid_move:
                self.label["text"] = "sorry you can't put your piece there ;-; \n pls try another spot!"
            else:
                self.draw_piece(board_position, color)
                self.board.board_status[board_position[1]][board_position[0]] = (
                    color
                )
                self.flip_pieces(board_position)
                self.player_Bs_move = not self.player_Bs_move
                self.num_moves += 1
                print("number of moves made:", self.num_moves)
                print(self.board.board_status)

                # ai move
                if (not self.board.is_end_game() and self.board.get_num_possible_moves(-1) > 0):
                    self.window.after(100, self.computer_turn)
                    # if user player has no possible moves
                    while self.board.get_num_possible_moves(1) == 0 and not self.board.is_end_game():
                        self.window.after(100, self.computer_turn)
            if (self.board.get_num_possible_moves(-1) == 0):
                self.label["text"] = "AI has no possible moves ;-; you can go again!" 
                print("AI has no possible moves ;-; you can go again!")

            # print possible moves for white
            print("possible moves", self.board.get_possible_moves(-1))

            if (self.board.is_end_game()):
                print("END OF GAME")
                white_count = np.count_nonzero(self.board_status == -1)
                black_count = np.count_nonzero(self.board_status == 1)
                print("white discs:", white_count)
                print("black discs:", black_count)
                if white_count > black_count:
                    print("YOU LOST! :'(")
                    self.label["text"] = "YOU LOST! :'("
                else:
                    print("YOU WON! XD")
                    self.label["text"] = "YOU WON! XD"
                
    def computer_turn(self):
        self.label["text"] = "It's the computer's turn"
        i, j = ai_move(self.board)
        # self.window.after(2000, self.draw_piece([j, i], color))
        self.draw_piece([j,i], -1)
        self.board.board_status[i][j] = -1
        # self.window.after(3000, self.flip_pieces([j,i]))
        self.flip_pieces([j,i])
        self.num_moves += 1
        self.player_Bs_move = True
        self.label["text"] = "It's your turn"

    def flip_pieces(self, board_position):
        color = 1 if self.player_Bs_move else -1
        indices = self.board.get_flippable_pieces(board_position, color)
        for [r, c] in indices:
            self.draw_piece([c, r], color)
            self.board.board_status[r, c] = color


game = Othello()
game.mainloop()
