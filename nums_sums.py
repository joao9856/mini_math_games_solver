from mainboard import Board, BoardCell

def load_num_sums_page(window, board_size):
    board = Board(window, board_size, "numsums")
    board.build()
    #print(board.side_board[0].radio)