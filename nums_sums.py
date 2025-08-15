from mainboard import Board
import tkinter as tk

def load_num_sums_page(window, board_size):
    board = Board(window, board_size, "numsums")
    board.build()
    board.solver_func = solver
    



def solver(board):
    remove_larger_than_sum(board)

    check_biggest_value_need(board)

    odd_even_need_and_selection(board)


def add_to_sum_so_far(board, cell, value):

    board.rows[cell.row_index][0].cell.sum_so_far += value

    if board.rows[cell.row_index][0].cell.sum_so_far == int(board.rows[cell.row_index][0].get()):
        excess_numbers_cleaner(board.rows[cell.row_index])
        board.rows[cell.row_index][0].cell.not_solved = False

    board.columns[cell.column_index][0].cell.sum_so_far += value

    if board.columns[cell.column_index][0].cell.sum_so_far == int(board.columns[cell.column_index][0].cell.get()):
        excess_numbers_cleaner(board.columns[cell.column_index])
        board.columns[cell.column_index][0].cell.not_solved = False

    for group, _ in board.side_board[board.scrollable_canvas_index].groups:
        if cell in group.nums:
            group.sum_so_far += value
            if group.sum_so_far == int(group.get()):
                excess_numbers_cleaner(group)
                group.not_solved = False
    
    

def excess_numbers_cleaner(group):
    if hasattr(group, "cell"):
        for cell in group[1:]:
            if not cell.cell.num_to_keep:
                cell.cell.config(state="normal")
                cell.cell.delete(0, tk.END)
                cell.cell.config(state="readonly")
    else:
        for cell in group.nums:
            if not cell.num_to_keep:
                cell.config(state="normal")
                cell.delete(0, tk.END)
                cell.config(state="readonly")


def remove_larger_than_sum(board):
    for row in board.rows[1:]:
        if row[0].cell.not_solved:
            for cell in row[1:]:
                user_input = cell.cell.get()
                row_sum = int(row[0].cell.get())
                if user_input != "":
                    user_input = int(user_input)
                    if user_input > row_sum - row[0].cell.sum_so_far and cell.cell.num_to_keep == False:
                        cell.cell.config(state="normal")
                        cell.cell.delete(0, tk.END)
                        cell.cell.config(state="readonly")
    for column in board.columns[1:]:
        if column[0].cell.not_solved:
            for cell in column[1:]:
                user_input = cell.cell.get()
                column_sum = int(column[0].cell.get())
                if user_input != "":
                    user_input = int(user_input)
                    if user_input > column_sum - column[0].cell.sum_so_far and cell.cell.num_to_keep == False:
                        cell.cell.config(state="normal")
                        cell.cell.delete(0, tk.END)
                        cell.cell.config(state="readonly")
    for group, _ in board.side_board[board.scrollable_canvas_index].groups:
        if group.not_solved:
            for cell in group.nums:
                user_input = cell.get()
                group_sum = int(group.get())
                if user_input != "":
                    user_input = int(user_input)
                    if user_input > group_sum - group.sum_so_far and cell.num_to_keep == False:
                        cell.config(state="normal")
                        cell.delete(0, tk.END)
                        cell.config(state="readonly")

def check_biggest_value_need(board):
    
    for row in board.rows[1:]:
        if row[0].cell.not_solved:
            row_sum = int(row[0].cell.get())
            loop_break = 1
            iteration = 0
            repeat_nums = []
            while loop_break == 1 and iteration < 50:
                iteration += 1
                print(f"Iteration {iteration} on Rows")
                biggest_value = 0
                total_sum = 0
                sum_so_far = row[0].cell.sum_so_far
                for cell in row[1:]:
                    num_to_keep = cell.cell.num_to_keep
                    user_input = cell.cell.get()
                    if not num_to_keep and user_input != "":
                        user_input = int(user_input)
                        total_sum += user_input
                        if user_input == biggest_value:
                            repeat_nums.append(user_input)
                            biggest_value = 0
                        if user_input in repeat_nums:
                            continue
                        if user_input > biggest_value:
                            biggest_value = user_input
                            cell_to_keep = cell
                print(f"biggest_value: {biggest_value}, total_sum: {total_sum}, sum_so_far: {sum_so_far}, sum_objective: {row_sum}")
                print(f"Condition: {total_sum - biggest_value} < {row_sum - sum_so_far}")
                if total_sum - biggest_value < row_sum - sum_so_far and biggest_value != 0:
                    print(f"Action taken on cell with value {biggest_value}")
                    cell_to_keep.cell.num_to_keep = True
                    add_to_sum_so_far(board, cell_to_keep.cell, biggest_value)
                    loop_break += 1
                loop_break -= 1

    for column in board.columns[1:]:
        if column[0].cell.not_solved:
            column_sum = int(column[0].cell.get())
            loop_break = 1
            iteration = 0
            repeat_nums = []
            while loop_break == 1 and iteration < 50:
                iteration += 1
                print(f"Iteration {iteration} on Columns")
                biggest_value = 0
                total_sum = 0
                sum_so_far = column[0].cell.sum_so_far
                for cell in column[1:]:
                    num_to_keep = cell.cell.num_to_keep
                    user_input = cell.cell.get()
                    if not num_to_keep and user_input != "":
                        user_input = int(user_input)
                        total_sum += user_input
                        if user_input == biggest_value:
                            repeat_nums.append(user_input)
                            biggest_value = 0
                        if user_input in repeat_nums:
                            continue
                        if user_input > biggest_value:
                            biggest_value = user_input
                            cell_to_keep = cell
                print(f"biggest_value: {biggest_value}, total_sum: {total_sum}, sum_so_far: {sum_so_far}, sum_objective: {column_sum}")
                print(f"Condition: {total_sum - biggest_value} < {column_sum - sum_so_far}")
                if total_sum - biggest_value < column_sum - sum_so_far and biggest_value != 0:
                    print(f"Action taken on cell with value {biggest_value}")
                    cell_to_keep.cell.num_to_keep = True
                    add_to_sum_so_far(board, cell_to_keep.cell, biggest_value)
                    loop_break += 1
                loop_break -= 1
    
    for group, _ in board.side_board[board.scrollable_canvas_index].groups:
        if group.not_solved:
            group_sum = int(group.get())
            loop_break = 1
            iteration = 0
            repeat_nums = []
            while loop_break == 1 and iteration < 50:
                iteration += 1
                print(f"Iteration {iteration} on Groups")
                biggest_value = 0
                total_sum = 0
                sum_so_far = group.sum_so_far
                for cell in group.nums:
                    num_to_keep = cell.num_to_keep
                    user_input = cell.get()
                    if not num_to_keep and user_input != "":
                        user_input = int(user_input)
                        total_sum += user_input
                        if user_input == biggest_value:
                            repeat_nums.append(user_input)
                            biggest_value = 0
                        if user_input in repeat_nums:
                            continue
                        if  user_input > biggest_value:
                            biggest_value = user_input
                            cell_to_keep = cell
                
                print(f"biggest_value: {biggest_value}, total_sum: {total_sum}, sum_so_far: {sum_so_far}, sum_objective: {group_sum}")
                print(f"Condition: {total_sum - biggest_value} < {group_sum - sum_so_far}")
                if total_sum - biggest_value < group_sum - sum_so_far and biggest_value != 0:
                    print(f"Action taken on cell with value {biggest_value}")
                    cell_to_keep.num_to_keep = True
                    add_to_sum_so_far(board, cell_to_keep, biggest_value)
                    loop_break += 1
                loop_break -= 1


def odd_even_need_and_selection(board):
    for row in board.rows[1:]:
        if row[0].cell.not_solved:
            sum_left = int(row[0].cell.get()) - row[0].cell.sum_so_far
            oddeven = bool(sum_left+1 % 2)
            odd = []
            for cell in row[1:]:
                num_to_keep = cell.cell.num_to_keep
                user_input = cell.cell.get()
                if user_input != "" and not num_to_keep:
                    user_input = int(user_input)
                    if user_input % 2 == 1:
                        odd.append(cell)
            if oddeven:
                if len(odd) == 1:
                    odd[0].cell.num_to_keep = True
                    add_to_sum_so_far(board, odd[0].cell, int(odd[0].cell.get()))

    for column in board.columns[1:]:
        if column[0].cell.not_solved:
            sum_left = int(column[0].cell.get()) - column[0].cell.sum_so_far
            oddeven = bool(sum_left+1 % 2)
            odd = []
            for cell in column[1:]:
                num_to_keep = cell.cell.num_to_keep
                user_input = cell.cell.get()
                if user_input != "" and not num_to_keep:
                    user_input = int(user_input)
                    if user_input % 2 == 1:
                        odd.append(cell)
            if oddeven:
                if len(odd) == 1:
                    odd[0].cell.num_to_keep = True
                    add_to_sum_so_far(board, odd[0].cell, int(odd[0].cell.get()))

    for group, _ in board.side_board[board.scrollable_canvas_index].groups:
        if group.not_solved:
            sum_left = int(group.get()) - group.sum_so_far
            oddeven = bool(sum_left+1 % 2)
            odd = []
            for cell in group.nums:
                num_to_keep = cell.num_to_keep
                user_input = cell.get()
                if user_input != "" and not num_to_keep:
                    user_input = int(user_input)
                    if user_input % 2 == 1:
                        odd.append(cell)
            if oddeven:
                if len(odd) == 1:
                    odd[0].num_to_keep = True
                    add_to_sum_so_far(board, odd[0], int(odd[0].get()))
