import copy

class MyPlayer:
    '''AB pruning. Depth is 4. Moves out of "gold 16". Pre-evaluated table'''
    # "gold 16" - 16 central cells. At the begining it is important to stay inside
    # it, but sometimes (after 8th move) we can get an opportunity to get 
    # a cell, that is closer to wall/corner without any problems for us
    def __init__(self, my_color, opponent_color):
        self.name = 'galkidmi'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.depth = 4 # depth of the recursive AB pruning
        self.cur_move = []
        # A pre-evaluated table. Allows us to stay in the central square 
        # at the begining and helps to choose a good move. (+) good for us, 
        # (-) bad for us.
        self.preev_board = [[1000, -300, 100,  80,  80, 100,-300, 1000],
                            [-300, -500, -45, -50, -50, -45,-500, -300],
                            [ 100,  -45,   3,   1,   1,   3, -45,  100],
                            [  80,  -50,   1,   5,   5,   1, -50,   80],
                            [  80,  -50,   1,   5,   5,   1, -50,   80],
                            [ 100,  -45,   3,   1,   1,   3, -45,  100],
                            [-300, -500, -45, -50, -50, -45,-500, -300],
                            [1000, -300, 100,  80,  80, 100,-300, 1000]]
    
    def move(self, board):
        move = self.minimax(copy.deepcopy(board), self.depth, -10000, 10000, 
                                                                my_turn = True)
        # We've obtained a corner? Then it is safe for us to put our pieces 
        # around it, because an opponent will not be able to flip our cells!
        if move in [[0, 0], [0, 7], [7, 0], [7, 7]]:
            self.change_preev_board(move)
        return move

    def minimax(self, board, cur_depth, alpha, beta, my_turn):
        # Alpha-Beta pruning algorithm, depth is 4
        # alpha - tries to maximise our points
        # beta - tries to minimise our points 
        if cur_depth == 0:
            # Count the difference between the scores and add to this a suitable 
            # number from the preev_board table
            score = self.count_score(board, self.my_color) - \
                                    self.count_score(board, self.opponent_color)
            score += self.preev_board[self.cur_move[0]][self.cur_move[1]]
            return score
        elif my_turn == True:
            return self.maximizer(board, cur_depth, alpha, beta)
        else:
            return self.minimizer(board, cur_depth, alpha, beta)

    def maximizer(self, board, cur_depth, alpha, beta):
         # Tries to maximise my points
        best_move = []
        moves = self.find_moves(board, self.my_color, self.opponent_color)
        if moves == [] and cur_depth != self.depth:
            # We will not have any moves at some depth -> Very good for the opponent
            return -1001 + self.count_score(board, self.my_color)
        elif moves == [] and cur_depth == self.depth:
            # We do not have any possible moves -> None
            return None
        for move in moves:
            # Evaluating all possible moves
            if cur_depth == self.depth:
                # if we've already made more than 8 moves, we'll start to
                # go out of the central square, if position is safe
                self.cur_move = move
                if self.count_score(board, -1) < 50 and self.check_position():
                    if self.is_safe(board) == True:
                        # We will be closer to the walls and corners. It is 
                        # very good for us
                        my_score = self.count_score(board, self.my_color)
                        alpha = my_score - self.preev_board[move[0]][move[1]]
                        best_move = move
                        continue
            board_copy = self.repaint_the_board(copy.deepcopy(board), 
                                            move[0], move[1], my_turn = True)
            # We've repainted the board, now it's time to evaluate the move
            score = self.minimax(board_copy, cur_depth - 1, alpha, beta, 
                                                            my_turn = False)
            if score > alpha:
                alpha = score
                best_move = move
            if beta <= alpha:
                break
        if cur_depth == self.depth:
            return best_move
        else:
            return alpha 

    def minimizer(self, board, cur_depth, alpha, beta):
        # Tries to minimise my score
        moves = self.find_moves(board, self.opponent_color, self.my_color)
        if moves == []:
            # An opponent does not have any moves -> Very good for us
            return 1000 + self.count_score(board, self.my_color)
        for move in moves:
            board_copy = self.repaint_the_board(copy.deepcopy(board), move[0], 
                                                     move[1], my_turn = False)
            score = self.minimax(board_copy, cur_depth - 1, alpha, beta, 
                                                              my_turn = True)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return beta

    def is_safe(self, board):
        # At the beginning a program plays at the central 16 cells, but 
        # sometimes it is better to make a move out of this square.
        # This method defines if it is dangerous for us to make a move 
        # "out of the comfort zone" or not. Dangerous = an opponent can get a 
        # corner or a wall after the move
        direction_y = [1, 1, 0, -1, -1, -1,  0,  1] # 1 - lower, -1 - higher
        direction_x = [0, 1, 1,  1,  0, -1, -1, -1] # 1 - right, -1 - left
        for condition in range(8): # Choose a direction
            is_dangerous = 0
            for depth in range(1, 8): # Follow this direction
                new_y = self.cur_move[0] + depth * direction_y[condition]
                new_x = self.cur_move[1] + depth * direction_x[condition]
                if (-1 < new_x < 8) and (-1 < new_y < 8):
                    if board[new_y][new_x] == self.my_color:
                        # We met our cell -> at this direction we are vulnerable,
                        # our opponent can possibly flip our cells and get a 
                        # wall/corner
                        is_dangerous = 1
                    elif board[new_y][new_x] == -1:
                        # if we make a move, we'll flip some of the opponents cells
                        # if we met an empty cell and before our move in the opposite 
                        # direction there is an opponent's cell, he can flip my
                        # cells and get the wall/corner
                        prev_x = self.cur_move[1] - direction_x[condition]
                        prev_y = self.cur_move[0] - direction_y[condition]
                        if is_dangerous == 1 and board[prev_y][prev_x] == self.opponent_color and \
                        -1 < prev_x < 8 and -1 < prev_y < 8:
                            # direction is dangerous, FALSE
                            return False 
                        else:
                            # This direction is safe, change direction
                            break
                    elif board[new_y][new_x] == self.opponent_color:
                        if is_dangerous == 1:
                            # We met an opponent's cell after ours -> 
                            # direction is dangerous
                            return False 
                        else:
                            # This direction is safe, change direction
                            continue
                else:
                    # out of board, change direction
                    break 
        return True

    def check_position(self):
        # The most dangerous "circle" in the table is second (all the numbers 
        # are negative). Sometimes it is really good for us to make a move in 
        # this area, but it must be 100% safe for us
        # Here we check, if the move is in this "dangerous circle" or not
        if ((self.cur_move[0] == 1 or self.cur_move[0] == 6) and 1 < self.cur_move[1] < 6) or \
           ((self.cur_move[1] == 1 or self.cur_move[1] == 6) and 1 < self.cur_move[0] < 6): 
            return True
        else:
            return False
    
    def count_score(self, board, color):
        # Counts the amount of cells with particular color
        score = 0
        for y in range(8):
            for x in range(8):
                if board[y][x] == color:
                    score += 1
        return score

    def find_moves(self, board, p1_color, p2_color):
        # Finds all valid moves that we can make with the current state of 
        # the game board
        moves = []
        for i in range(8):
            for j in range(8):
                if board[i][j] == p1_color:
                    valid_moves = self.find_moves_for_cell(board, i, j, p2_color)
                    for move in valid_moves:
                        if move not in moves:
                            moves.append(move)
        return moves
    
    def find_moves_for_cell(self, board, y, x, p2_color):
        # Finds all the moves that we can make due to obtaining a specific cell 
        # of the playing board with coordinats (x, y)
        direction_y = [1, 1, 0, -1, -1, -1,  0,  1] # 1 - lower, -1 - higher
        direction_x = [0, 1, 1,  1,  0, -1, -1, -1] # 1 - right, -1 - left
        valid_moves = []
        for condition in range(8): # choose a direction
            move_is_valid = 0
            for depth in range(1, 8): # follow the direction
                new_y = y + depth * direction_y[condition]
                new_x = x + depth * direction_x[condition]
                if (-1 < new_x < 8) and (-1 < new_y < 8):
                    if board[new_y][new_x] == p2_color:
                        # We need to cover at least one opponent's cell to make a move
                        move_is_valid = 1 
                    elif board[new_y][new_x] == -1 and move_is_valid == 1:
                        # Valid move has been found, change direction
                        valid_moves.append([new_y, new_x])
                        break 
                    else:
                        # There is no valid move in this direction
                        break 
                else:
                    # out of board, change direction
                    break 
        return valid_moves

    def repaint_the_board(self, board, y, x, my_turn): 
        # Repaints p2_color cells in p1_color after obtaining a cell with 
        # coordinates (x, y) by p1 player
        if my_turn == True:
            p1_color = self.my_color
            p2_color = self.opponent_color
        else:
            p2_color = self.my_color
            p1_color = self.opponent_color
        direction_y = [1, 1, 0, -1, -1, -1,  0,  1] # 1 - lower, -1 - higher
        direction_x = [0, 1, 1,  1,  0, -1, -1, -1] # 1 - right, -1 - left
        for condition in range(8): 
            repainting_is_valid = 0
            for depth in range(8):
                new_y = y + depth * direction_y[condition]
                new_x = x + depth * direction_x[condition]
                if (-1 < new_x < 8) and (-1 < new_y < 8):
                    if board[new_y][new_x] == p2_color:
                        # We have cells for repainting
                        repainting_is_valid = 1 
                    elif board[new_y][new_x] == p1_color and repainting_is_valid == 1:
                        # Go back until the cell [x, y] and repaint all the cells
                        for height in range(depth - 1, 0, -1):
                            new_y = y + height * direction_y[condition]
                            new_x = x + height * direction_x[condition]
                            if board[new_y][new_x] == p2_color:
                                board[new_y][new_x] = p1_color
                        break
                    elif depth == 0:
                        # The initial [x, y] cell must be repainted too
                        board[new_y][new_x] = p1_color
                    else:
                        # There is no valid repainting in this direction
                        break
                else:
                    # out of board, change direction
                    break 
        return board

    def change_preev_board(self, move):
        # The cells near the corner are not dangerous for us anymore, because 
        # the corner is ours now.
        # Their value = value of cells near the wall
        if move == [0, 0]:
            self.preev_board[1][0] = 80
            self.preev_board[0][1] = 80
            self.preev_board[2][0] = 80
            self.preev_board[0][2] = 80
            self.preev_board[1][1] = 80
        elif move == [0, 7]:
            self.preev_board[1][7] = 80
            self.preev_board[0][6] = 80
            self.preev_board[2][7] = 80
            self.preev_board[0][5] = 80
            self.preev_board[1][6] = 80
        elif move == [7, 0]:
            self.preev_board[6][0] = 80
            self.preev_board[7][1] = 80
            self.preev_board[5][0] = 80
            self.preev_board[7][2] = 80
            self.preev_board[6][1] = 80
        elif move == [7, 7]:
            self.preev_board[6][7] = 80
            self.preev_board[7][6] = 80
            self.preev_board[5][7] = 80
            self.preev_board[7][5] = 80
            self.preev_board[6][6] = 80
