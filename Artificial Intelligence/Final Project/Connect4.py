# Base game code from tutorial at https://www.youtube.com/watch?v=XpYz-q1lxu8&t=812s
# Used this video for help on setting up the OpenAI environment https://www.youtube.com/watch?v=w1jd0Dpbc2o&t=8s and training loop

import numpy as np
import matplotlib.pyplot as plt
import math
import time
import random
import gym
import gym_connect4

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # check for horizontal win
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT):
            if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                return True

    # check for vertical win
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT-3):
            if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                return True

    # check for positively-sloped diagonal win
    for col in range(COLUMN_COUNT-3):
        for row in range(ROW_COUNT-3):
            if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                return True

    for col in range(COLUMN_COUNT-3):
        for row in range(3, ROW_COUNT):
            if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                return True


def evaluate_window(window, piece):
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


def score_position(board, piece):

    score = 0

    # score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # score horizontal
    for row in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[row, :])]
        for col in range(COLUMN_COUNT-3):
            window = row_array[col:col+4]
            score += evaluate_window(window, piece)

    # score vertical
    for col in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, col])]
        for row in range(ROW_COUNT-3):
            window = col_array[row:row+4]
            score += evaluate_window(window, piece)

    # score positive-sloped diagonal
    for row in range(ROW_COUNT-3):
        for col in range(COLUMN_COUNT-3):
            window = [board[row+i][col+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # score negatively-sloped diagonal
    for row in range(ROW_COUNT-3):
        for col in range(COLUMN_COUNT-3):
            window = [board[row+3-i][col+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_locations(board)) == 0


def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:

        if is_terminal:
            if winning_move(board, 2):
                return (None, 10000000000)
            elif winning_move(board, 1):
                return (None, -1000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, 2))

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, 2)
            new_score = minimax(b_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value

    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, 1)
            new_score = minimax(b_copy, depth-1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value


def expectimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:

        if is_terminal:
            if winning_move(board, 2):
                return (None, 10000000000)
            elif winning_move(board, 1):
                return (None, -1000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, 2))

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, 2)
            new_score = minimax(b_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value

    else:
        value = math.inf
        column = random.choice(valid_locations)
        nodes = []
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, 1)
            new_score = minimax(b_copy, depth-1, True)[1]
            nodes.append(new_score)
            if new_score < value:
                value = new_score
                column = col
        total = sum(nodes)
        return column, (total/len(valid_locations))


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)

    return valid_locations


def choose_best_move(board, piece):
    best_score = 0
    best_col = 0
    valid_locations = get_valid_locations(board)

    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def max_action(Q, state, actions):
    print(Q)
    
    values = np.array([Q[state, a] for a in actions])
    action = np.argmax(values)
    return max(val) #actions[actions]


def Q_learning(board):
    env = gym.make('connect4-v0')  # create gym environment for training agent
    alpha = 0.1
    gamma = 1.0
    epsilon = 1.0

    Q = {}
    for state in range(ROW_COUNT * COLUMN_COUNT):
        for action in range(7):
            Q[state, action] = 0

    num_games = 50000
    total_rewards = np.zeros(num_games)

    for i in range(num_games):
        if i % 5000 == 0:
            print('starting game {}'.format(i))

        done = False
        epRewards = 0
        observation = env.reset()

        while not done:
            rand = np.random.random()
            if rand < (1-epsilon):
                action = max_action(
                    Q, observation, get_valid_locations(observation))
            else:
                action = np.random.choice(get_valid_locations(observation))

            observation_, reward, done, info = env.step(action)
            epRewards += reward
            action_ = max_action(
                Q, observation_, get_valid_locations(observation_))
            Q[observation, action] = Q[observation, action] + alpha*(reward +
                                                                     gamma*Q[observation_, action_] - Q[observation, action])
            observation = observation_ # update observation

        if epsilon - 2 / num_games > 0:
            epsilon -= 2 / num_games
        else:
            epsilon = 0
        total_rewards[i] = epRewards
    plt.plot(total_rewards)
    plt.show()


if __name__ == '__main__':

    board = create_board()
    Q_learning(board)
    game_over = False
    turn = 0
"""
    while not game_over:

        col = None
        # Player's turn
        if turn == 0:
            # while (col is None or col > 7 or col < 1 or not is_valid_location(board, col-1)):
            # col = int(input("Player 1 Make your Selection (1-7): "))
            col, score = minimax(board, 4, True)
            time.sleep(.25)
            print("minimax chooses column {}".format(col))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)

                if winning_move(board, 1):
                    print_board(board)
                    print("minimax wins!")
                    game_over = True
                    break

        # ai's turn
        else:
            #col, score = minimax(board, 4, True)
            col, score = expectimax(board, 4, True)
            time.sleep(.25)
            print("expectimax chooses column {}".format(col))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

                if winning_move(board, 2):
                    print_board(board)
                    print("expectimax wins!")
                    game_over = True
                    break
        print("-----------")
        print_board(board)
        turn = (turn+1) % 2
        """
