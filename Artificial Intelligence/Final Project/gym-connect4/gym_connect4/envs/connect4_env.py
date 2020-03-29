# Base game code from tutorial at https://www.youtube.com/watch?v=XpYz-q1lxu8&t=812s

import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding


class connect4(gym.Env):
  #create board, initialize any variables that are needed in order to keep track of the state
  def __init__(self):
    print("init success")
    self.action_space = [0, 1, 2, 3, 4, 5, 6]
    self.row_count = 6
    self.col_count = 7
    self.board = np.zeros((self.row_count, self.col_count))

  def drop_piece(self, board, row, col, piece):
    board[row][col] = piece

  def is_valid_location(self, board, col):
    return board[self.row_count - 1][col] == 0


  def get_next_open_row(self, board, col):
    for r in range(self.row_count):
        if board[r][col] == 0:
            return r


  def get_valid_locations(self, board):
    valid_locations = []
    for col in range(self.col_count):
        if self.is_valid_location(board, col):
            valid_locations.append(col)

    return valid_locations


  def winning_move(self, board, piece):
  # check for horizontal win
    for col in range(self.col_count-3):
        for row in range(self.row_count):
            if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                return True

    # check for vertical win
    for col in range(self.col_count):
        for row in range(self.row_count-3):
            if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                return True

    # check for positively-sloped diagonal win
    for col in range(self.col_count-3):
        for row in range(self.row_count-3):
            if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                return True

    for col in range(self.col_count-3):
        for row in range(3, self.row_count):
            if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                return True

  def is_terminal_state(self, board):
    return self.winning_move(board, 1) or self.winning_move(board, 2) or len(self.get_valid_locations(board)) == 0

  def evaluate_window(self, window, piece):
    OPPONENT = 1
    if piece == 1:
        OPPONENT = 2

    score = 0
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 1:
        score += 2

    if window.count(OPPONENT) == 3 and window.count(0) == 1:
        score -= 4

    return score


  def score_position(self, board, piece):
    score = 0

    # score center column
    center_array = [int(i) for i in list(board[:, self.col_count//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # score horizontal
    for row in range(self.row_count):
        row_array = [int(i) for i in list(board[row, :])]
        for col in range(self.col_count-3):
            window = row_array[col:col+4]
            score += self.evaluate_window(window, piece)

    # score vertical
    for col in range(self.col_count):
        col_array = [int(i) for i in list(board[:, col])]
        for row in range(self.row_count-3):
            window = col_array[row:row+4]
            score += self.evaluate_window(window, piece)

    # score positive-sloped diagonal
    for row in range(self.row_count-3):
        for col in range(self.col_count-3):
            window = [board[row+i][col+i] for i in range(4)]
            score += self.evaluate_window(window, piece)

    # score negatively-sloped diagonal
    for row in range(self.row_count-3):
        for col in range(self.col_count-3):
            window = [board[row+3-i][col+i] for i in range(4)]
            score += self.evaluate_window(window, piece)

    return score


  #perform action
  #return new state, reward, whether or not the game is over (in terminal state?), & debug info (can be None)
  #if attemping illegal move, then do nothing
  def step(self, action):
    print("step success")
    chosen_col = action
    if self.is_valid_location(self.board, chosen_col):
      row = self.get_next_open_row(self.board, chosen_col)
      self.drop_piece(self.board, row, chosen_col, 1)
      reward = self.score_position(self.board, 1)
      return self.board, reward, self.is_terminal_state(self.board), None

    else:
      return self.board, 0, self.is_terminal_state(self.board), None # may need to change the reward here

  def reset(self):
    #reset the board state to all 0s & also agent's current position
    #return agent position
    print("reset success")
    self.board = np.zeros((self.row_count, self.col_count))
    return self.board
  


  # print the current board state
  # doesn't need to return anything
  def render(self):
      print(np.flip(self.board, 0))
      
