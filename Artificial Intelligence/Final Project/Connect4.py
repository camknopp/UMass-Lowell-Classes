# Code from tutorial at https://www.youtube.com/watch?v=XpYz-q1lxu8&t=812s

import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((6,7))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[5][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):

    # check for horizontal win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # check for vertical win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # check for positively-sloped diagonal win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # check for negatively-sloped diagonal win
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] and board[r-2][c+2] == piece and board[r- 3][c+3] == piece:
                return True 
    

 

board = create_board()
game_over = False
turn = 0

while not game_over:
    # ask for player 1 input
    if turn == 0:
        col = int(input("Player 1 Make your Selection (0-6): "))
        
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

            if winning_move(board, 1):
                print ("Player 1 wins!")
                game_over = True
                break
        turn = 1

    # ask for player 2 input
    else:
        col = int(input("Player 2 Make your Selection (0-6): "))
       
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, 2):
                print ("Player 1 wins!")
                game_over = True
                break

        turn = 0

    print_board(board)
