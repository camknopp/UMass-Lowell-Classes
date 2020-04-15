# Base game code from tutorial at https://www.youtube.com/watch?v=XpYz-q1lxu8&t=812s
# Used this video for help on setting up the OpenAI environment https://www.youtube.com/watch?v=w1jd0Dpbc2o&t=8s and training loop

import numpy as np
import matplotlib.pyplot as plt
import math
import time
import random
import pygame
from menu_option import Option

#ROW_COUNT = 6
#COLUMN_COUNT = 7
ROW_COUNT = 8
COLUMN_COUNT = 8
COLUMN_SPACING = 50
ROW_SPACING = 50
LEFT_MARGIN = 250
TOP_MARGIN = 750
EGGSHELL = (240, 234, 214)  # used for the screen's background color
MINIMAX_AI = 2
NON_MINIMAX_AI = 1


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


def evaluate(board, piece):

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

    
def minimax(board, depth, alpha, beta, maximizingPlayer):
    # performs minimax algorithm to find best move
    # code based upon pseudocode found here https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode

    # check for terminal node or depth=0
    if depth == 0:
        return (None, evaluate(board, MINIMAX_AI))
    elif winning_move(board, MINIMAX_AI):
        return (0, math.inf)
    elif winning_move(board, NON_MINIMAX_AI):
        return (0, -math.inf)
    elif len(get_valid_locations(board)) == 0:
        return (0,0)
    

    if maximizingPlayer:
        value = -math.inf
        valid = get_valid_locations(board)
        column = valid[0]
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
        column = valid[0]
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
        return (None, evaluate(board, 2))
    elif winning_move(board, 2):
        return (0, math.inf)
    elif winning_move(board, 1):
        return (0, -math.inf)
    elif len(get_valid_locations(board)) == 0:
        return (0,0)

    if maximizingPlayer:
        value = -math.inf
        valid = get_valid_locations(board)
        column = 0
        for col in valid:
            board_copy = board.copy()
            drop_piece(board_copy, col, 2)
            score = expectimax(board_copy, depth-1, False)[1]
            if score > value:
                value = score
                column = col
        return column, value

    else:
        value = math.inf
        valid = get_valid_locations(board)
        column = 0
        nodes = []
        for col in valid:
            board_copy = board.copy()
            drop_piece(board_copy, col, 1)
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

    b_copy = board.copy()
    drop_piece(b_copy, col, piece)
    return evaluate(b_copy, piece)
    
    opponent = 2
    if piece == 2:
        opponent = 1

    #extra_points = 0
    

    # check whether placing a piece in this position will win the game
    board_copy = board.copy()
    drop_piece(board_copy, col, piece)
    if winning_move(board_copy, piece):
        return math.inf
    else:
        if get_next_open_row(board_copy, col) is not None:
            drop_piece(board_copy, col, opponent)
            if winning_move(board_copy, opponent):
                return -math.inf# dropping this piece will set the opponent up for a win, which we don't want

    # check whether this position will stop the opponent from winning
    board_copy = board.copy()
    drop_piece(board_copy, col, opponent)
    if winning_move(board_copy, opponent):
        return math.inf
    
        
    
    horizontal_score = 0
    vertical_score = 0
    pos_diag_score = 0
    neg_diag_score = 0

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
            horizontal_score+=1
        curr_col+=1

    if col+1 < COLUMN_COUNT and col-1 >= 0:
        if board[row][col+1] == opponent and board[row][col-1] == opponent:
            extra_points+=10 # give extra points for this position because it prevents the opponent from getting 3 in a row horizontally

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
            vertical_score+=1
        curr_row+=1


    # reset these values
    curr_col = col
    curr_row = row

    # now need to determine the upper_row and upper_col values for use in scoring the negatively-sloped diagonals
    done = False
    while not done:
        curr_col+=1
        curr_row+=1
        if curr_col > COLUMN_COUNT-1 or curr_row > ROW_COUNT-1 or curr_col == col+4:
            upper_row = curr_row-1
            upper_col = curr_col-1
            done=True
    
    curr_row = upper_row
    curr_col = upper_col

    # add +1 to pos_diag_score for every positively-sloped 4-in-a-row that can potentially occur from given pos
    # traverse board right->left from upper right diagonal position
    while curr_row >= row and curr_row-3 >= 0 and curr_col >= col and curr_col-3 >= 0:
        if board[curr_row][curr_col] != opponent and board[curr_row-1][curr_col-1] != opponent and board[curr_row-2][curr_col-2] != opponent and board[curr_row-3][curr_col-3] != opponent:
            pos_diag_score+=1
        curr_row-=1
        curr_col-=1


    # reset these values
    curr_col = col
    curr_row = row

    # now we determine the lower_col and upper_row values which are used when scoring the postiively-sloped diagonals
    done = False
    while not done:
        curr_col-=1
        curr_row+=1
        if curr_col < 0 or curr_row > ROW_COUNT-1 or curr_col == col-4:
            lower_col = curr_col+1
            upper_row = curr_row-1
            done=True

    curr_col = lower_col
    curr_row = upper_row # want to start at the highest row and move down, since we are looking for negative diagonals
    
    # add +1 to neg_diag_score for every negatively-sloped 4-in-a-row that can potentially occur from given pos
    # traverse board left->right from upper left position
    while curr_row >= row and curr_row-3 >= 0 and curr_col <= col and curr_col+3 <= COLUMN_COUNT-1:
        #print("[x][y]==[{}][{}]".format(curr_col, curr_row))
        if board[curr_row][curr_col] != opponent and board[curr_row-1][curr_col+1] != opponent and board[curr_row-2][curr_col+2] != opponent and board[curr_row-3][curr_col+3] != opponent:
            neg_diag_score+=1
        curr_row-=1
        curr_col+=1

    return horizontal_score + vertical_score + pos_diag_score + neg_diag_score + extra_points


def PSO(board, piece):
    # based around pseudocode found here https://en.wikipedia.org/wiki/Particle_swarm_optimization
   
    c1 = 2
    c2 = 2
    r1 = np.random.random()
    r2 = np.random.random()
    b_copy = board.copy()
    population_size = 40
    max_generation = 200
    swarm = []

    # initialize particle swarm
    for i in range(population_size):
        p_curr_coord = [random.choice(range(ROW_COUNT)),
                   random.choice(range(COLUMN_COUNT))]
        p_best_coord = [random.choice(range(ROW_COUNT)),
                   random.choice(range(COLUMN_COUNT))]
        p_veloc = [np.random.random(), np.random.random()]

        swarm.append([p_curr_coord, p_best_coord, p_veloc])
    
    gbest = swarm[0][0] # set gbest arbitrarily to the first particle's coordinates


    for i in range(max_generation):
        for j in range(population_size):
            p = swarm[j]

            # adjust the particle's current position using its velocity
            for k in range(2):
                p[2][k] = math.floor(p[2][k] + c1 * r1 * (p[1][k] - p[0][k]) + c2 * r2 * (gbest[k] - p[0][k]))
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
            if fitness(b_copy, p[0], piece) > fitness(b_copy, p[1], piece):
                p[1] = p[0].copy()
                # check whether the particle's current position is the global best for the swarm thus far
                if fitness(b_copy, p[1], piece) > fitness(b_copy, gbest, piece):
                    gbest = p[1].copy()
            swarm[j] = p

    return gbest # return the global best coordinate of the swarm


def draw_piece(screen, row, col, piece):
    if piece == 1:
        color = (255, 0, 0)
    else:
        color = (255, 255, 0)

    x = col * COLUMN_SPACING + LEFT_MARGIN
    y = TOP_MARGIN - row * ROW_SPACING
    pygame.display.update(pygame.draw.circle(screen, color, (x, y), 10, 0))


def draw_board(board, screen):
    for row in range(ROW_COUNT):
        # Loop for each column
        for column in range(COLUMN_COUNT):
            # Calculate our location
            x = column * COLUMN_SPACING + LEFT_MARGIN
            y = TOP_MARGIN - row * ROW_SPACING

            pygame.draw.circle(screen, (255, 255, 255), (x, y), 10, 3)
    pygame.display.update()


def draw_menu(screen):
    options = [Option("Start Game", (400, 350), screen), Option(
        "Quit", (400, 600), screen), Option("<", (200, 475), screen), Option(">", (400, 475), screen)]
    chosen_option = False

    while chosen_option == False:
        # for event in pygame.event.get():
        pygame.event.pump()

        for option in options:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and option.hovered == True:
                    chosen_option = True
                    pygame.quit()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                else:
                    pass

        pygame.display.update()


def display_wins(screen, player_one_wins, player_two_wins, ties, names):
    font = pygame.font.SysFont('Comic Sans MS', 25)
    p1_wins = font.render(
        names[0] + ": "+str(player_one_wins), True, (0, 0, 0))
    screen.blit(p1_wins, (0, 0))

    p2_wins = font.render(
        names[1] + ": "+str(player_two_wins), True, (0, 0, 0))
    screen.blit(p2_wins, (150, 0))

    ties = font.render("Ties: "+str(ties), True, (0, 0, 0))
    screen.blit(ties, (350, 0))


def run_game_with_graphics():
    player1_wins = 0
    player2_wins = 0
    tie_games = 0
    names = ['PSO (red)', 'Minimax()']

    # Open the window and set the background
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    screen.fill(EGGSHELL)
    # draw_menu(screen)

    while player1_wins != 100 or player2_wins != 100:
        board = create_board()
        game_over = False
        turn = random.choice([0, 1])
        turn_num = 0
        screen.fill(EGGSHELL)
        display_wins(screen, player1_wins, player2_wins, tie_games, names)
        draw_board(board, screen)

        while not game_over:
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
                    col = PSO(board, 1)[1]
                    print("PSO chooses column {}".format(col))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, col, 1)
                        draw_piece(screen, row, col, 1)

                        if winning_move(board, 1):
                            print_board(board)
                            print("PSO wins!")
                            player1_wins += 1
                            print("total pso wins: {}".format(player1_wins))
                            game_over = True
                            break

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
                    col = minimax(board, 6, -math.inf, math.inf, True)[0]
                    print("minimax chooses column {}".format(col))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, col, 2)
                        draw_piece(screen, row, col, 2)

                        if winning_move(board, 2):
                            print_board(board)
                            print("minimax wins!")
                            player2_wins += 1
                            print("total minimax wins: {}".format(
                                player2_wins))

                            game_over = True
                            break
            print("-----------")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            time.sleep(.75)
            print_board(board)

            turn = (turn+1) % 2

        screen.fill(EGGSHELL)
        draw_board(board, screen)

    print("minimax wins: {}".format(minimax_wins))
    print("expectimax wins: {}".format(player2_wins))


def run_game_no_graphics():
    player1_wins = 0
    player2_wins = 0
    tie_games = 0
    
    while player1_wins != 100 or player2_wins != 100:
        board = create_board()
        game_over = False
        turn = random.choice([0, 1])
        turn_num = 0

        while not game_over:
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
                    drop_piece(board, col, 1)

                    turn_num += 1
                else:
                    col = PSO(board, 1)[1]
                    print("PSO chooses column {}".format(col))

                    if is_valid_location(board, col):
                        drop_piece(board, col, 1)

                        if winning_move(board, 1):
                            print_board(board)
                            print("PSO wins!")
                            player1_wins += 1
                            print("total pso wins: {}".format(player1_wins))
                            game_over = True
                            break

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
                    col = minimax(board, 6, -math.inf, math.inf, True)[0]
                    print("minimax chooses column {}".format(col))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, col, 2)
                        draw_piece(screen, row, col, 2)

                        if winning_move(board, 2):
                            print_board(board)
                            print("minimax wins!")
                            player2_wins += 1
                            print("total minimax wins: {}".format(
                                player2_wins))

                            game_over = True
                            break
            print("-----------")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            time.sleep(.75)
            print_board(board)

            turn = (turn+1) % 2

        screen.fill(EGGSHELL)
        draw_board(board, screen)

    print("minimax wins: {}".format(minimax_wins))
    print("expectimax wins: {}".format(player2_wins))


if __name__ == '__main__':

    
    run_game_with_graphics()




    