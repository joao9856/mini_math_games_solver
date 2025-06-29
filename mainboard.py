import tkinter as tk
import random

random.randrange(0, 255) #test usage for future implementation into macking random colors using f"#{rand}{rand}{rand}"
class Board:
    def __init__(self, window, board_size, board_type):
        self.window = window
        self.board_size = board_size
        self.board_type = board_type
        self.board = []
        self.rows = []
        self.columns = []

    

    def build(self):
        self.calc_width()
        self.create_board()
        self.cell_placer()



    def create_board(self):
        self.build_lists()
        for i in range(self.board_size + 1):
            for j in range(self.board_size + 1):
                if i == 0 and j == 0:
                    self.board[i].append(BoardCell(self.window, bgcolor="black", state="disabled"))
                elif i == 0 and j != 0:
                    self.board[i].append(BoardCell(self.window, bgcolor="gray"))
                    self.columns[j].append(self.board[i][j])
                elif j == 0 and i != 0:
                    self.board[i].append(BoardCell(self.window, bgcolor="gray"))
                    self.rows[i].append(self.board[i][j])
                else:
                    self.board[i].append(BoardCell(self.window))
                    self.rows[i].append(self.board[i][j])
                    self.columns[j].append(self.board[i][j])
    

    def cell_placer(self):
        for i in range(self.board_size + 1):
            for j in range(self.board_size + 1):
                if i == 0 and j == 0:
                    self.board[i][j].cell.place(x=self.cell_curr_x, y=self.cell_curr_y, width=self.cell_width, height=self.cell_width)
                    self.cell_curr_x += self.cell_width
                elif i == 0 and j != 0:
                    self.board[i][j].cell.place(x=self.cell_curr_x, y=self.cell_curr_y, width=self.cell_width, height=self.cell_width)
                    self.cell_curr_x += self.cell_width
                elif j == 0 and i != 0:
                    self.board[i][j].cell.place(x=self.cell_curr_x, y=self.cell_curr_y, width=self.cell_width, height=self.cell_width)
                    self.cell_curr_x += self.cell_width
                else:
                    self.board[i][j].cell.place(x=self.cell_curr_x, y=self.cell_curr_y, width=self.cell_width, height=self.cell_width)
                    self.cell_curr_x += self.cell_width
            self.cell_curr_y += self.cell_width
            self.cell_curr_x = self.cell_start_x


    def build_lists(self):
        for i in range(self.board_size + 1):
            self.board.append([])
            self.rows.append([])
            self.columns.append([])
    

    def calc_width(self):
        self.board_width = int(self.window.winfo_width() * 0.8) - 10 if int(self.window.winfo_width() * 0.8) - 10 <= self.window.winfo_height() else self.window.winfo_height() - 10
        self.cell_width = int(self.board_width / (self.board_size + 1))
        self.cell_start_x = int((self.board_width - (self.cell_width * (self.board_size + 1))) / 2)
        self.cell_curr_x = self.cell_start_x
        self.cell_start_y = self.cell_start_x
        self.cell_curr_y = self.cell_start_x

class BoardCell:
    def __init__(self, window, bgcolor="white", state="readonly"):
        self.window = window
        self.cell = tk.Entry(window, justify="center", bg=bgcolor,disabledbackground="",readonlybackground="", state=state, bd=1)
    def on_click(self, event):
        pass


