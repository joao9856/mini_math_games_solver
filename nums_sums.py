from mainboard import Board
import tkinter as tk

def load_num_sums_page(window, board_size):
    board = Board(window, board_size, "numsums")
    board.build()
    board.solver_func = solver
    



def solver(board):
    remove_impossible(board)




def remove_impossible(board):
    for row in board.rows:
        for cell in row[1:]:
            user_input = cell.cell.get()
            row_sum = row[0].cell.get()
            if user_input != "":
                if int(user_input) > int(row_sum):
                    cell.cell.config(state="normal")
                    cell.cell.delete(0, tk.END)
                    cell.cell.config(state="readonly")
    for column in board.columns:
        for cell in column[1:]:
            user_input = cell.cell.get()
            column_sum = column[0].cell.get()
            if user_input != "":
                if int(user_input) > int(column_sum):
                    cell.cell.config(state="normal")
                    cell.cell.delete(0, tk.END)
                    cell.cell.config(state="readonly")
    for group, _ in board.side_board[board.scrollable_canvas_index].groups:
        for cell in group.nums:
            user_input = cell.get()
            group_sum = group.get()
            if user_input != "":
                if int(user_input) > int(group_sum):
                    cell.config(state="normal")
                    cell.delete(0, tk.END)
                    cell.config(state="readonly")