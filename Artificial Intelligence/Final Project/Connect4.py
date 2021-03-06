# Base game code from tutorial at https://www.youtube.com/watch?v=XpYz-q1lxu8&t=812s

import numpy as np
import matplotlib.pyplot as plt
import math
import time
import random
import pygame

#ROW_COUNT = 6
#COLUMN_COUNT = 7
ROW_COUNT = 8
COLUMN_COUNT = 8
COLUMN_SPACING = 50
ROW_SPACING = 50
LEFT_MARGIN = 250
TOP_MARGIN = 750
EGGSHELL = (240, 234, 214)  # used for the screen's background color
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
MINIMAX_AI = 2
NON_MINIMAX_AI = 1
EXPECTIMAX_AI = 2
NON_EXPECTIMAX_AI = 1
names = list()


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def drop_piece(board, col, piece):
    row = get_next_open_row(board, col)
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


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
    return False


def evaluate(board, player):
    """
    Returns a heuristic value for the current board
    Board is evaluated on the number of 4-in-a-rows that can potentially be made from each of the next open slots
    """

    opponent = 2
    if player == 2:
        opponent = 1
    score = 0

    valid = get_valid_locations(board)

    for col in valid:
        row = get_next_open_row(board, col)
        score += fitness(board, [row, col], player)

    return score


def minimax(board, depth, alpha, beta, maximizingPlayer):
    # performs minimax algorithm to find best move
    # code based upon pseudocode found here https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode

    # check for terminal node or depth=0
    if depth == 0:
        return (0, evaluate(board, MINIMAX_AI))
    elif winning_move(board, MINIMAX_AI):
        return (0, 100000)
    elif winning_move(board, NON_MINIMAX_AI):
        return (0, -100000)
    elif len(get_valid_locations(board)) == 0:
        return (0, 0)

    if maximizingPlayer:
        value = -math.inf
        valid = get_valid_locations(board)
        column = random.choice(valid)
        for col in valid:
            board_copy = board.copy()
            drop_piece(board_copy, col, MINIMAX_AI)
            score = minimax(board_copy, depth-1, alpha, beta, False)[1]
            if score > value:
                column = col
                value = score
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:
        value = math.inf
        valid = get_valid_locations(board)
        column = random.choice(valid)
        for col in valid:
            board_copy = board.copy()
            drop_piece(board_copy, col, NON_MINIMAX_AI)
            score = minimax(board_copy, depth-1, alpha, beta, True)[1]
            if score < value:
                value = score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def expectimax(board, depth, maximizingPlayer):

    # check for terminal node or depth=0
    if depth == 0:
        return (0, evaluate(board, EXPECTIMAX_AI))
    elif winning_move(board, EXPECTIMAX_AI):
        return (0, 100000)
    elif winning_move(board, NON_EXPECTIMAX_AI):
        return (0, -100000)
    elif len(get_valid_locations(board)) == 0:
        return (0, 0)

    if maximizingPlayer:
        value = -math.inf
        valid = get_valid_locations(board)
        column = random.choice(valid)
        for col in valid:
            board_copy = board.copy()
            drop_piece(board_copy, col, EXPECTIMAX_AI)
            score = expectimax(board_copy, depth-1, False)[1]
            if score > value:
                value = score
                column = col
        return column, value

    else:
        value = math.inf
        valid = get_valid_locations(board)
        column = random.choice(valid)
        nodes = []
        for col in valid:
            board_copy = board.copy()
            drop_piece(board_copy, col, NON_EXPECTIMAX_AI)
            score = expectimax(board_copy, depth-1, True)[1]
            nodes.append(score)
            if score < value:
                value = score
                column = col

        total = sum(nodes)
        return column, (total/len(valid))


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
        temp_board = board.copy()
        drop_piece(temp_board, col, piece)
        score = evaluate(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def fitness(board, pos, piece):
    # returns the fitness score of a given position (used for algorithms other than PSO)
    row = pos[0]
    col = pos[1]

    opponent = 2
    if piece == 2:
        opponent = 1

    horizontal_score = 0
    vertical_score = 0
    pos_diag_score = 0
    neg_diag_score = 0
    extra_points = 0

    # get the lower and upper bounds for the columns for a 4-in-a-row horizontal win from curr position
    lower_col = col - 3
    if lower_col < 0:
        lower_col = 0

    upper_col = col + 3
    if upper_col > COLUMN_COUNT-1:
        upper_col = COLUMN_COUNT-1

    curr_col = lower_col

    # add +1 to horizontal_score for every horiz. 4-in-a-row that can potentially happen from given pos
    while curr_col <= col and curr_col+3 <= upper_col:
        if board[row][curr_col] != opponent and board[row][curr_col+1] != opponent and board[row][curr_col+2] != opponent and board[row][curr_col+3] != opponent:
            horizontal_score += 1
        curr_col += 1

    if col+1 < COLUMN_COUNT and col-1 >= 0:
        if board[row][col+1] == opponent and board[row][col-1] == opponent:
            extra_points += 10  # give extra points for this position because it prevents the opponent from getting 3 in a row horizontally

    # get the lower and upper bounds for rows for a 4-in-a-row vertical win from curr position
    lower_row = row - 3
    if lower_row < 0:
        lower_row = 0

    upper_row = row + 3
    if upper_row > ROW_COUNT-1:
        upper_row = ROW_COUNT-1

    # add +1 to vertical_score for every vert. 4-in-a-row that can potentially occur from given pos
    curr_row = lower_row
    while curr_row <= row and curr_row+3 <= upper_row:
        if board[curr_row][col] != opponent and board[curr_row+1][col] != opponent and board[curr_row+2][col] != opponent and board[curr_row+3][col] != opponent:
            vertical_score += 1
        curr_row += 1

    # reset these values
    curr_col = col
    curr_row = row

    # now need to determine the upper_row and upper_col values for use in scoring the negatively-sloped diagonals
    done = False
    while not done:
        curr_col += 1
        curr_row += 1
        if curr_col > COLUMN_COUNT-1 or curr_row > ROW_COUNT-1 or curr_col == col+4:
            upper_row = curr_row-1
            upper_col = curr_col-1
            done = True

    curr_row = upper_row
    curr_col = upper_col

    # add +1 to pos_diag_score for every positively-sloped 4-in-a-row that can potentially occur from given pos
    # traverse board right->left from upper right diagonal position
    while curr_row >= row and curr_row-3 >= 0 and curr_col >= col and curr_col-3 >= 0:
        if board[curr_row][curr_col] != opponent and board[curr_row-1][curr_col-1] != opponent and board[curr_row-2][curr_col-2] != opponent and board[curr_row-3][curr_col-3] != opponent:
            pos_diag_score += 1
        curr_row -= 1
        curr_col -= 1

    # reset these values
    curr_col = col
    curr_row = row

    # now we determine the lower_col and upper_row values which are used when scoring the postiively-sloped diagonals
    done = False
    while not done:
        curr_col -= 1
        curr_row += 1
        if curr_col < 0 or curr_row > ROW_COUNT-1 or curr_col == col-4:
            lower_col = curr_col+1
            upper_row = curr_row-1
            done = True

    curr_col = lower_col
    # want to start at the highest row and move down, since we are looking for negative diagonals
    curr_row = upper_row

    # add +1 to neg_diag_score for every negatively-sloped 4-in-a-row that can potentially occur from given pos
    # traverse board left->right from upper left position
    while curr_row >= row and curr_row-3 >= 0 and curr_col <= col and curr_col+3 <= COLUMN_COUNT-1:
        #print("[x][y]==[{}][{}]".format(curr_col, curr_row))
        if board[curr_row][curr_col] != opponent and board[curr_row-1][curr_col+1] != opponent and board[curr_row-2][curr_col+2] != opponent and board[curr_row-3][curr_col+3] != opponent:
            neg_diag_score += 1
        curr_row -= 1
        curr_col += 1

    return horizontal_score + vertical_score + pos_diag_score + neg_diag_score + extra_points


def pso_fitness(board, pos, piece):
    # returns the fitness score of a particle at a given position

    row = pos[0]
    col = pos[1]

    # make sure that the position is onoccupied
    if board[row][col] != 0:
        return -math.inf

    # check whether the move is legal by making sure it is not floating above empty space
    i = 1
    while i <= row:
        if board[row-i][col] == 0:
            return -math.inf
        i += 1

    opponent = 2
    if piece == 2:
        opponent = 1

    horizontal_score = 0
    vertical_score = 0
    pos_diag_score = 0
    neg_diag_score = 0
    extra_points = 0

    # check whether placing a piece in this position will win the game
    board_copy = board.copy()
    drop_piece(board_copy, col, piece)

    if winning_move(board_copy, piece):
        return math.inf
    else:
        if get_next_open_row(board_copy, col) is not None:
            drop_piece(board_copy, col, opponent)
            if winning_move(board_copy, opponent):
                # dropping this piece will set the opponent up for a win, which we don't want
                return -math.inf

    # check whether this position will stop the opponent from winning
    board_copy = board.copy()
    drop_piece(board_copy, col, opponent)
    if winning_move(board_copy, opponent):
        return math.inf

    # get the lower and upper bounds for the columns for a 4-in-a-row horizontal win from curr position
    lower_col = col - 3
    if lower_col < 0:
        lower_col = 0

    upper_col = col + 3
    if upper_col > COLUMN_COUNT-1:
        upper_col = COLUMN_COUNT-1

    curr_col = lower_col

    # add +1 to horizontal_score for every horiz. 4-in-a-row that can potentially happen from given pos
    while curr_col <= col and curr_col+3 <= upper_col:
        if board[row][curr_col] != opponent and board[row][curr_col+1] != opponent and board[row][curr_col+2] != opponent and board[row][curr_col+3] != opponent:
            horizontal_score += 1
        curr_col += 1

    if col+1 < COLUMN_COUNT and col-1 >= 0:
        if board[row][col+1] == opponent and board[row][col-1] == opponent:
            extra_points += 10  # give extra points for this position because it prevents the opponent from getting 3 in a row horizontally

    # get the lower and upper bounds for rows for a 4-in-a-row vertical win from curr position
    lower_row = row - 3
    if lower_row < 0:
        lower_row = 0

    upper_row = row + 3
    if upper_row > ROW_COUNT-1:
        upper_row = ROW_COUNT-1

    # add +1 to vertical_score for every vert. 4-in-a-row that can potentially occur from given pos
    curr_row = lower_row
    while curr_row <= row and curr_row+3 <= upper_row:
        if board[curr_row][col] != opponent and board[curr_row+1][col] != opponent and board[curr_row+2][col] != opponent and board[curr_row+3][col] != opponent:
            vertical_score += 1
        curr_row += 1

    # reset these values
    curr_col = col
    curr_row = row

    # now need to determine the upper_row and upper_col values for use in scoring the negatively-sloped diagonals
    done = False
    while not done:
        curr_col += 1
        curr_row += 1
        if curr_col > COLUMN_COUNT-1 or curr_row > ROW_COUNT-1 or curr_col == col+4:
            upper_row = curr_row-1
            upper_col = curr_col-1
            done = True

    curr_row = upper_row
    curr_col = upper_col

    # add +1 to pos_diag_score for every positively-sloped 4-in-a-row that can potentially occur from given pos
    # traverse board right->left from upper right diagonal position
    while curr_row >= row and curr_row-3 >= 0 and curr_col >= col and curr_col-3 >= 0:
        if board[curr_row][curr_col] != opponent and board[curr_row-1][curr_col-1] != opponent and board[curr_row-2][curr_col-2] != opponent and board[curr_row-3][curr_col-3] != opponent:
            pos_diag_score += 1
        curr_row -= 1
        curr_col -= 1

    # reset these values
    curr_col = col
    curr_row = row

    # now we determine the lower_col and upper_row values which are used when scoring the postiively-sloped diagonals
    done = False
    while not done:
        curr_col -= 1
        curr_row += 1
        if curr_col < 0 or curr_row > ROW_COUNT-1 or curr_col == col-4:
            lower_col = curr_col+1
            upper_row = curr_row-1
            done = True

    curr_col = lower_col
    # want to start at the highest row and move down, since we are looking for negative diagonals
    curr_row = upper_row

    # add +1 to neg_diag_score for every negatively-sloped 4-in-a-row that can potentially occur from given pos
    # traverse board left->right from upper left position
    while curr_row >= row and curr_row-3 >= 0 and curr_col <= col and curr_col+3 <= COLUMN_COUNT-1:
        #print("[x][y]==[{}][{}]".format(curr_col, curr_row))
        if board[curr_row][curr_col] != opponent and board[curr_row-1][curr_col+1] != opponent and board[curr_row-2][curr_col+2] != opponent and board[curr_row-3][curr_col+3] != opponent:
            neg_diag_score += 1
        curr_row -= 1
        curr_col += 1

    return horizontal_score + vertical_score + pos_diag_score + neg_diag_score + extra_points


def PSO(board, piece):
    # based around pseudocode found here https://en.wikipedia.org/wiki/Particle_swarm_optimization

    c1 = 2
    c2 = 2
    r1 = np.random.random()
    r2 = np.random.random()
    b_copy = board.copy()
    population_size = 50
    max_generation = 250
    swarm = []

    # initialize particle swarm
    for i in range(population_size):
        p_curr_coord = [random.choice(range(ROW_COUNT)),
                        random.choice(range(COLUMN_COUNT))]
        p_best_coord = [random.choice(range(ROW_COUNT)),
                        random.choice(range(COLUMN_COUNT))]
        p_veloc = [np.random.random(), np.random.random()]

        swarm.append([p_curr_coord, p_best_coord, p_veloc])

    # set gbest arbitrarily to the first particle's coordinates
    gbest = swarm[0][0]

    for i in range(max_generation):
        for j in range(population_size):
            p = swarm[j]

            # adjust the particle's current position using its velocity
            for k in range(2):
                p[2][k] = math.floor(p[2][k] + c1 * np.random.random() * (
                    p[1][k] - p[0][k]) + c2 * np.random.random() * (gbest[k] - p[0][k]))
                #print("p[2][{}]: {}".format(k, p[2][k]))
                p[0][k] += p[2][k]

            # make sure the particle's position coordinates are within the board's dimensions
            if p[0][0] > ROW_COUNT-1:
                p[0][0] = ROW_COUNT-1
            elif p[0][0] < 0:
                p[0][0] = 0

            if p[0][1] > COLUMN_COUNT-1:
                p[0][1] = COLUMN_COUNT-1
            elif p[0][1] < 0:
                p[0][1] = 0

            # check whether the particle's current position is it's best position thus far
            if pso_fitness(b_copy, p[0], piece) > pso_fitness(b_copy, p[1], piece):
                p[1] = p[0].copy()
                # check whether the particle's current position is the global best for the swarm thus far
                if pso_fitness(b_copy, p[1], piece) > pso_fitness(b_copy, gbest, piece):
                    gbest = p[1].copy()
            swarm[j] = p

    return gbest  # return the global best coordinate of the swarm


def draw_piece(screen, row, col, piece):
    global names  # this contains the names of the AI in the current game

    if piece == 1:
        color = RED
        name = names[0]
    else:
        color = YELLOW
        name = names[1]
    message = "{} chooses column {}".format(name, col+1)

    font = pygame.font.SysFont('Comic Sans MS', 35)
    pygame.draw.rect(screen, EGGSHELL, (250, 250, 400, 100))
    num = font.render(message, True, color)
    screen.blit(num, (250, 300))

    if piece == 1:
        color = (255, 0, 0)
    else:
        color = (255, 255, 0)

    x = col * COLUMN_SPACING + LEFT_MARGIN
    y = TOP_MARGIN - row * ROW_SPACING
    print("drawing piece at row {} and col {}".format(row, col))
    pygame.display.update(pygame.draw.circle(screen, color, (x, y), 10, 0))


def draw_board(board, screen):
    font = pygame.font.SysFont('Comic Sans MS', 25)

    for row in range(ROW_COUNT):
        # Loop for each column
        for column in range(COLUMN_COUNT):
            # Calculate our location
            x = column * COLUMN_SPACING + LEFT_MARGIN
            y = TOP_MARGIN - row * ROW_SPACING

            pygame.draw.circle(screen, (255, 255, 255), (x, y), 10, 3)

    for col in range(COLUMN_COUNT):
        x = col * (COLUMN_SPACING) + LEFT_MARGIN-3
        y = TOP_MARGIN - ROW_COUNT * ROW_SPACING
        num = font.render(str(col+1), True, (0, 0, 0))
        screen.blit(num, (x, y))

    pygame.display.update()


def display_wins(screen, player_one_wins, player_two_wins, ties, names):
    font = pygame.font.SysFont('Comic Sans MS', 25)
    p1_wins = font.render(
        names[0] + ": "+str(player_one_wins), True, (0, 0, 0))
    screen.blit(p1_wins, (0, 0))

    p2_wins = font.render(
        names[1] + ": "+str(player_two_wins), True, (0, 0, 0))
    screen.blit(p2_wins, (300, 0))

    ties = font.render("Ties: "+str(ties), True, (0, 0, 0))
    screen.blit(ties, (600, 0))


def display_win_message(screen, piece, col):
    global names  # this contains the names of the AI in the current game

    if piece == 1:
        color = RED
        name = names[0]
    else:
        color = YELLOW
        name = names[1]
    message = "{} wins by dropping piece in column {}".format(name, col+1)

    font = pygame.font.SysFont('Comic Sans MS', 35)
    pygame.draw.rect(screen, EGGSHELL, (250, 250, 400, 100))
    num = font.render(message, True, color)
    screen.blit(num, (250, 300))


def run_game_with_graphics():
    player1_wins = 0
    player2_wins = 0
    tie_games = 0
    first_AI = None
    second_AI = None
    global names
    global MINIMAX_AI
    global NON_MINIMAX_AI
    global EXPECTIMAX_AI
    global NON_EXPECTIMAX_AI

    while first_AI != 1 and first_AI != 2 and first_AI != 3 and first_AI != 4:
        first_AI = int(input("Please enter a number to indicate your first AI choice: \n(1) Minimax w/ alpha beta pruning \
            \n(2) Expectimax \n(3) Particle Swarm Optimization \n(4) Random\n"))

    if first_AI == 1:
        names.append('Minimax')
        MINIMAX_AI = 1
        NON_MINIMAX_AI = 2
    elif first_AI == 2:
        names.append('Expectimax')
        EXPECTIMAX_AI = 1
        NON_EXPECTIMAX_AI = 2
    elif first_AI == 3:
        names.append('PSO')
    else:
        names.append('Random')

    while second_AI != 1 and second_AI != 2 and second_AI != 3 and second_AI != 4 or second_AI == first_AI:
        second_AI = int(input("Please enter a different number to indicate your second AI choice: \n(1) Minimax w/ alpha beta pruning \
            \n(2) Expectimax \n(3) Particle Swarm Optimization \n(4) Random\n"))

    if second_AI == 1:
        names.append('Minimax')
        MINIMAX_AI = 2
        NON_MINIMAX_AI = 1
    elif second_AI == 2:
        names.append('Expectimax')
        EXPECTIMAX_AI = 2
        NON_EXPECTIMAX_AI = 1
    elif second_AI == 3:
        names.append('PSO')
    else:
        names.append('Random')

    print("names: {}".format(names))

    # Open the window and set the background
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    screen.fill(EGGSHELL)
    last_turn = 1
    # while player1_wins != 100 or player2_wins != 100:
    while player1_wins + player2_wins + tie_games < 100:
        board = create_board()
        game_over = False
        turn_num = 0
        # do this so that it switches of which player starts each game
        if last_turn == 1:
            turn = 0
            last_turn = 0
        else:
            turn = 1
            last_turn = 1

        screen.fill(EGGSHELL)
        display_wins(screen, player1_wins, player2_wins, tie_games, names)
        draw_board(board, screen)

        while True:
            col = None
            # Player's turn
            if len(get_valid_locations(board)) == 0:
                game_over = True
                print("Tie game")
                tie_games += 1
                break

            if turn == 0:
                if turn_num < 2:  # if first or second turn, then drop random piece in order to spice up the game
                    col = random.choice(get_valid_locations(board))
                    print("Randomly placing a chip...")
                    row = get_next_open_row(board, col)
                    drop_piece(board, col, 1)
                    draw_piece(screen, row, col, 1)

                    turn_num += 1
                else:
                    if first_AI == 1:
                        col = minimax(board, 6, -math.inf, math.inf, True)[0]
                    elif first_AI == 2:
                        col = expectimax(board, 4, True)[0]
                    elif first_AI == 3:
                        col = PSO(board, 1)[1]
                    else:
                        col = random.choice(get_valid_locations(board))

                    print("P1 chooses column {}".format(col))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, col, 1)
                        draw_piece(screen, row, col, 1)

                        if winning_move(board, 1):
                            player1_wins += 1
                            display_win_message(screen, 1, col)
                            game_over = True

            # ai's turn
            else:
                if turn_num < 2:  # if first or second turn, then drop random piece in order to spice up the game
                    col = random.choice(get_valid_locations(board))
                    print("Randomly placing a chip...")
                    row = get_next_open_row(board, col)
                    drop_piece(board, col, 2)
                    draw_piece(screen, row, col, 2)

                    turn_num += 1
                else:
                    if second_AI == 1:
                        col = minimax(board, 6, -math.inf, math.inf, True)[0]
                    elif second_AI == 2:
                        col = expectimax(board, 4, True)[0]
                    elif second_AI == 3:
                        col = PSO(board, 1)[1]
                    else:
                        col = random.choice(get_valid_locations(board))

                    print("P2 chooses column {}".format(col))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, col, 2)
                        draw_piece(screen, row, col, 2)

                        if winning_move(board, 2):
                            player2_wins += 1
                            display_win_message(screen, 2, col)
                            game_over = True
            print("-----------")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            time.sleep(.5)
            print_board(board)
            if game_over:
                time.sleep(3)
                break

            turn = (turn+1) % 2

    print("{} wins: {}".format(names[0], player1_wins))
    print("{} wins: {}".format(names[1], player2_wins))
    print("Ties: {}".format(tie_games))


if __name__ == '__main__':

    run_game_with_graphics()
