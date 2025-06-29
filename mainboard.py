import tkinter as tk
import random

random.randrange(0, 255) #test usage for future implementation into macking random colors using f"#{rand}{rand}{rand}"
class Board:
    def __init__(self, window, board_size, board_type):
        self.window = window
        self.board_size = board_size
        self.board_type = board_type
        self.bigger_boards = ["numsums", "nonogram"]
        self.board = []
        self.rows = []
        self.columns = []
        self.side_board = []
        self.mode = tk.StringVar(value="input")
        if self.board_type in self.bigger_boards:
            self.board_size += 1
    

    def build(self):
        self.build_lists()
        self.calc_width()
        self.create_board()
        self.cell_placer()
        self.build_side_board()
        self.place_side_board()
        



    def create_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board_type in self.bigger_boards:
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
                else:
                    self.board[i].append(BoardCell(self.window, bgcolor="gray"))
                    self.rows[i].append(self.board[i][j])
                    self.columns[j].append(self.board[i][j])

    

    def cell_placer(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.board[i][j].cell.place(x=self.cell_curr_x, y=self.cell_curr_y, width=self.cell_width, height=self.cell_width)
                self.cell_curr_x += self.cell_width
            self.cell_curr_y += self.cell_width
            self.cell_curr_x = self.cell_start_x


    def build_lists(self):
        for i in range(self.board_size):
            self.board.append([])
            self.rows.append([])
            self.columns.append([])
    

    def calc_width(self):
        self.board_width = int(self.window.winfo_width() * 0.8) - 10 if int(self.window.winfo_width() * 0.8) - 10 <= self.window.winfo_height() else self.window.winfo_height() - 10
        self.cell_width = int(self.board_width / (self.board_size))
        self.cell_start_x = int((self.board_width - (self.cell_width * (self.board_size))) / 2)
        self.cell_curr_x = self.cell_start_x
        self.cell_start_y = self.cell_start_x
        self.cell_curr_y = self.cell_start_x
        
        self.side_board_cell_start_x = ((self.cell_start_x * 2) + (self.cell_width * self.board_size)) 
        self.side_board_cell_curr_x = self.side_board_cell_start_x
        self.side_board_cell_space = (self.window.winfo_width() - self.side_board_cell_start_x)
        self.side_board_cell_start_y = self.cell_start_y
        self.side_board_cell_curr_y = self.cell_start_y
    

    def build_side_board(self):
        if self.board_type == "numsums":
            self.build_numsums_side_board()

    def place_side_board(self):
        if self.board_type == "numsums":
            self.place_numsums_side_board()

    def build_numsums_side_board(self):
        self.side_board.append(BoardCell(self.window, "white", cell_type="radio", radio_info=[("Input", "input"), ("Groups", "groups")], mode=self.mode))

    def place_numsums_side_board(self):
        for radio in self.side_board[0].radio:
            radio.place(x=self.side_board_cell_curr_x, y=self.side_board_cell_curr_y, width=int(self.side_board_cell_space / 2), height=self.cell_width)
            print(self.side_board_cell_curr_x, self.side_board_cell_curr_y, int(self.side_board_cell_space / 2), self.cell_width, self.side_board_cell_space)
            self.side_board_cell_curr_x += int(self.side_board_cell_space / 2)
        self.side_board_cell_curr_x = self.side_board_cell_start_x
        self.side_board_cell_curr_y += self.cell_width


    def numsums_side_board_add_group(self):

        pass


    def numsuns_side_board_delete_group(self):

        pass


class BoardCell:
    def __init__(self, window, bgcolor="white", state="readonly", cell_type="entry", radio_info = None, mode = None):
        self.window = window
        if cell_type == "entry":
            self.cell = tk.Entry(self.window, justify="center", bg=bgcolor, disabledbackground="", readonlybackground="", state=state, bd=1)
        if cell_type == "radio":
            self.cell = None
            self.radio = []
            for text, value in radio_info:
                radio_button = tk.Radiobutton(self.window, justify="center", bg=bgcolor, indicatoron=0, text=text, value=value, variable=mode)
                self.radio.append(radio_button)
        
    
    def on_click(self, event):
        pass


