import tkinter as tk
import random

from general import add_to_widgets_list, resizer, page_cleaner
from variables import widgets
from main_page import main_page_loader

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
        self.solver_func = lambda : 0
        self.validate_int = self.window.register(lambda x: self.enforce_int(x))
        self.mode = tk.StringVar(value="input")
        self.selected_group = None
        self.selected_cell = None
        if self.board_type in self.bigger_boards:
            self.board_size += 1

        

        self.window.bind("<Configure>", lambda event: self.placer())
        if self.board_type == "numsums":
            self.window.bind("<FocusIn>", self.on_cell_selected)
            self.window.bind("<FocusOut>", self.on_cell_deselected)
    

    def build(self):
        self.build_lists()
        self.calc_size()
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
                        self.board[i].append(BoardCell(self.window, bgcolor="gray", validate_int=self.validate_int, selected_group=self.selected_group))
                        self.columns[j].append(self.board[i][j])
                    elif j == 0 and i != 0:
                        self.board[i].append(BoardCell(self.window, bgcolor="gray", validate_int=self.validate_int, selected_group=self.selected_group))
                        self.rows[i].append(self.board[i][j])
                    else:
                        self.board[i].append(BoardCell(self.window, validate_int=self.validate_int, selected_group=self.selected_group))
                        self.rows[i].append(self.board[i][j])
                        self.columns[j].append(self.board[i][j])
                else:
                    self.board[i].append(BoardCell(self.window, bgcolor="gray", validate_int=self.validate_int, selected_group=self.selected_group))
                    self.rows[i].append(self.board[i][j])
                    self.columns[j].append(self.board[i][j])

    def placer(self):
        if self.board != []:
            self.calc_size()
            self.cell_placer()
            self.place_side_board()
            self.place_groups()
            resizer(self.window, True)
        

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
    

    def calc_size(self):
        self.board_width = int(self.window.winfo_width() * 0.6) - 10 if int(self.window.winfo_width() * 0.6) - 10 <= self.window.winfo_height() else self.window.winfo_height() - 10
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

        self.canvas_work_width = self.side_board_cell_space - 20
        self.canvas_start_y = self.cell_start_y
        self.canvas_curr_y = self.canvas_start_y
        if hasattr(self,"scrollable_canvas_index"):
            self.canvas_total_height = len(self.side_board[self.scrollable_canvas_index].groups) * self.cell_width
        else:
            self.canvas_total_height = 0
    

    def build_side_board(self):
        if self.board_type == "numsums":
            self.build_numsums_side_board()

    def place_side_board(self):
        if self.board_type == "numsums":
            self.place_numsums_side_board()

    def build_numsums_side_board(self):
        self.radio_index = 0
        self.create_group_index = 1
        self.return_index = 2
        self.solve_index = 3
        self.scrollable_canvas_index = 4


        self.side_board.append(BoardCell(self.window, "white", cell_type="radio", radio_info=[("Input", "input"), ("Groups", "groups")], mode=self.mode))
        self.side_board.append(BoardCell(self.window, "white", cell_type="button", command=self.create_group, text="Create Group"))
        self.side_board.append(BoardCell(self.window, "white", cell_type="button", text="Return"))
        self.side_board.append(BoardCell(self.window, "white", cell_type="button", text="Solve"))
        self.side_board.append(ScrollableCanvas(self.window, on_delete=self.place_groups, validate_int=self.validate_int))
        self.side_board[self.return_index].cell.config(command=(self.return_button))
        self.side_board[self.solve_index].cell.config(command=(self.solver))

    def place_numsums_side_board(self):
        for radio in self.side_board[self.radio_index].radio:
            radio.place(x=self.side_board_cell_curr_x, y=self.side_board_cell_curr_y, width=int(self.side_board_cell_space / 2), height=self.cell_width)
            self.side_board_cell_curr_x += int(self.side_board_cell_space / 2)
        self.side_board_cell_curr_x = self.side_board_cell_start_x
        self.side_board_cell_curr_y += self.cell_width
        self.side_board[self.create_group_index].cell.place(x=self.side_board_cell_curr_x, y=self.side_board_cell_curr_y, width=self.side_board_cell_space, height=self.cell_width)
        self.side_board_cell_curr_y += self.cell_width
        self.side_board[self.return_index].cell.place(x=self.side_board_cell_curr_x, y=(self.cell_width * (self.board_size - 1)) + self.side_board_cell_start_y, width=self.side_board_cell_space, height=self.cell_width)
        self.side_board[self.solve_index].cell.place(x=self.side_board_cell_curr_x, y=(self.cell_width * (self.board_size - 2)) + self.side_board_cell_start_y, width=self.side_board_cell_space, height=self.cell_width)
        self.side_board[self.scrollable_canvas_index].canvas.place(x=self.side_board_cell_start_x, y=self.side_board_cell_curr_y, width=self.side_board_cell_space, height=self.cell_width * (self.board_size - 4))
        self.side_board[self.scrollable_canvas_index].scrollbar.place(x=(self.side_board_cell_start_x + self.side_board_cell_space) - 20, y=self.side_board_cell_curr_y + self.cell_start_y, width=20, height=(self.cell_width * (self.board_size - 4)) - (self.cell_start_y * 2))
        self.place_groups()


    def place_groups(self, recalc=False, deselect=False):
        if deselect:
            self.selected_group = None
        if recalc:
            self.calc_size()
        
        current_y = self.cell_start_x
        for entry, button in self.side_board[self.scrollable_canvas_index].groups:
            entry.place(x=0, y=current_y, width=self.cell_width, height=self.cell_width)
            button.place(x=self.cell_width, y=current_y, width=self.canvas_work_width - self.cell_width, height=self.cell_width)
            current_y += self.cell_width
        
        self.canvas_curr_y = current_y
        self.side_board[self.scrollable_canvas_index].scrollable_frame.configure(height=self.canvas_total_height, width=self.canvas_work_width)
        self.side_board[self.scrollable_canvas_index].canvas.configure(scrollregion=(0, 0, 0, self.canvas_total_height))
            

    def create_group(self):
        self.side_board[self.scrollable_canvas_index].create_group()
        self.side_board[self.scrollable_canvas_index].groups[-1][0].place(x=0, y=self.canvas_curr_y, width=self.cell_width, height=self.cell_width)
        self.side_board[self.scrollable_canvas_index].groups[-1][1].place(x=self.cell_width, y=self.canvas_curr_y, width=self.canvas_work_width - self.cell_width, height=self.cell_width)
        self.canvas_curr_y += self.cell_width
        self.canvas_total_height += self.cell_width
        self.side_board[self.scrollable_canvas_index].scrollable_frame.configure(height=self.canvas_total_height, width=self.canvas_work_width)
        self.side_board[self.scrollable_canvas_index].canvas.configure(scrollregion=(0, 0, 0, self.canvas_total_height))
    

    def on_cell_selected(self, event=None):
        selected_widget = event.widget
        if isinstance(selected_widget, tk.Entry):
            if self.mode.get() == "input":
                if hasattr(selected_widget, "color") == False:
                    selected_widget.config(state="normal")
            if self.mode.get() == "groups":
                if hasattr(selected_widget, "color"):
                    self.selected_group = selected_widget
                elif self.selected_group == None:
                    pass
                elif selected_widget.cget("bg") == "gray":
                    pass
                elif selected_widget.cget("bg") == self.selected_group.color:
                    selected_widget.config(bg="white")
                    self.selected_group.nums.pop(self.selected_group.nums.index(selected_widget))
                elif selected_widget.cget("bg") == "white":
                    selected_widget.config(bg=self.selected_group.color)
                    self.selected_group.nums.append(selected_widget)
                else:
                    for entry, _ in self.side_board[self.scrollable_canvas_index].groups:
                        if entry.color == selected_widget.cget("bg"):
                            entry.nums.pop(entry.nums.index(selected_widget))
                            selected_widget.config(bg=self.selected_group.color)
                            self.selected_group.nums.append(selected_widget)
                            break
    
    
    def on_cell_deselected(self, event=None):
        selected_widget = event.widget
        if isinstance(selected_widget, tk.Entry):
            if self.mode.get() == "input":
                if hasattr(selected_widget, "color") == False:
                    selected_widget.config(state="readonly")
            if self.mode.get() == "groups":
                if self.selected_group != None:
                    pass

    
    def return_button(self):
        self.board.clear()
        self.rows.clear() 
        self.columns.clear()
        self.side_board.clear()
        del self.scrollable_canvas_index
        page_cleaner(widgets)
        main_page_loader(self.window)


    def solver(self):
        self.solver_func(self)
    

    def enforce_int(self, value):
        if value == "":
            return True
        return value.isdigit()

class BoardCell:
    def __init__(self, window, bgcolor="white", state="readonly", cell_type="entry", text = None, radio_info = None, mode = None, command = "", validate_int=None, selected_group=None):
        self.window = window
        self.selected_group = selected_group
        if cell_type == "entry":
            self.cell = tk.Entry(self.window, justify="center", bg=bgcolor, disabledbackground="", validate="key", validatecommand=(validate_int, "%P"), readonlybackground="", state=state, bd=1, font=("default", 20))
            add_to_widgets_list(self.cell, "Entry", default_font_size=20)
        if cell_type == "radio":
            self.cell = None
            self.radio = []
            for text, value in radio_info:
                radio_button = tk.Radiobutton(self.window, justify="center", bg=bgcolor, indicatoron=0, text=text, value=value, variable=mode, font=("default", 20))
                add_to_widgets_list(radio_button, "Radio", default_font_size=20)
                self.radio.append(radio_button)
        if cell_type == "button":
            self.cell = tk.Button(self.window, justify="center", bg=bgcolor, text=text, command=command, font=("default", 20))
            add_to_widgets_list(self.cell, "Button", default_font_size=20)
        if cell_type == "canvas":
            self.cell = tk.Canvas(window)
    
    


class ScrollableCanvas:
    def __init__(self, window, orient="vertical", on_delete=None, validate_int=None):
        self.window = window
        self.orient = orient
        self.groups = []
        self.colors = []
        self.on_delete = on_delete
        self.validate_int = validate_int
        self.create_canvas()

    def create_canvas(self):
        self.canvas = tk.Canvas(self.window)
        self.scrollbar = tk.Scrollbar(self.window, orient=self.orient, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        
        

    def create_group(self):
        while True:
            randcolor = f"#{random.randrange(0x1000000):06x}"
            if randcolor not in self.colors:
                self.colors.append(randcolor)
                break
        entry = tk.Entry(self.scrollable_frame, bg=randcolor, justify="center", validate="key", validatecommand=(self.validate_int, "%P"), font=("default", 20))
        entry.nums = []
        entry.color = randcolor
        add_to_widgets_list(entry, "Entry", default_font_size=20)
        button = tk.Button(self.scrollable_frame, bg="white", justify="center", text="Delete group", font=("default", 20))
        button.info = [len(self.groups), randcolor, len(widgets)]
        button.config(command=lambda b=button: self.delete_group(b.info))
        add_to_widgets_list(button, "Button", default_font_size=20)
        self.groups.append((entry, button))


    def delete_group(self, info):
        for entry in self.groups[info[0]][0].nums:
            entry.config(bg="white")
        self.groups[info[0]][0].destroy()
        self.groups[info[0]][1].destroy()
        self.colors.pop(self.colors.index(info[1]))
        widgets.pop(info[2])
        widgets.pop(info[2] - 1)
        self.groups.pop(info[0])
        if len(self.groups) >= info[0]:
            for i in range(info[0], len(self.groups)):
                self.groups[i][1].info[0] -= 1
                self.groups[i][1].info[2] -= 2
        
        if self.on_delete:
            self.on_delete(True,True)

