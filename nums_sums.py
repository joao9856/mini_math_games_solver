from mainboard import Board, BoardCell

def load_num_sums_page(window, board_size):
    board = Board(window, board_size, "numsums")
    board.build()
    for row in board.rows:
        print(row)
    for col in board.columns:
        print(col)