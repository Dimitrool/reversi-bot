import random
import copy

class MyPlayer:
    '''Minimax with depth 4 and cnt+ evaluation'''
    def __init__(self, my_color, opponent_color):
        self.name = 'galkidmi'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.moves = []
        self.depth = 4
        self.pts_board = [[1000, -300, 100,  80,  80, 100,-300, 1000],
                          [-300, -500, -45, -50, -50, -45,-500, -300],
                          [ 100,  -45,   3,   1,   1,   3, -45,  100],
                          [  80,  -50,   1,   5,   5,   1, -50,   80],
                          [  80,  -50,   1,   5,   5,   1, -50,   80],
                          [ 100,  -45,   3,   1,   1,   3, -45,  100],
                          [-300, -500, -45, -50, -50, -45,-500, -300],
                          [1000, -300, 100,  80,  80, 100,-300, 1000]]
    
    def move(self, board):
        return self.minimax(copy.deepcopy(board), self.depth, my_turn = True)

    def minimax(self, board, cur_depth, my_turn):
        if cur_depth == 0:
            return self.count_score(board, self.my_color)
        elif my_turn == True:
            # Tries to maximise 
            best_move = []
            best_score = -10000
            moves = self.find_moves_for_board(board, self.my_color, self.opponent_color)
            if moves == [] and cur_depth != self.depth:
                # We will not have any moves at some depth -> Very good for the opponent
                return -1001 + self.count_score(board, self.my_color)
            elif moves == [] and cur_depth == self.depth:
                # We do not have any possible moves -> None
                return None
            for move in moves:
                board_copy = self.repaint_the_cells(copy.deepcopy(board), move[0], move[1], self.my_color, self.opponent_color)
                score = self.minimax(board_copy, cur_depth - 1, my_turn = False)
                if score >= best_score:
                    best_score = score
                    best_move = move
            if cur_depth == self.depth:
                return best_move
            else:
                return best_score 
        else:
            # Tries to minimise 
            worst_score = 10000
            moves = self.find_moves_for_board(board, self.opponent_color, self.my_color)
            if moves == []:
                # An opponent does not have any moves -> Very good for us
                return 1000 + self.count_score(board, self.my_color)
            for move in moves:
                board_copy = self.repaint_the_cells(copy.deepcopy(board), move[0], move[1], self.opponent_color, self.my_color)
                score = self.minimax(board_copy, cur_depth - 1, my_turn = True)
                worst_score = min(worst_score, score)
            return worst_score
    
    def count_score(self, board, color):
        score = 0
        for y in range(8):
            for x in range(8):
                if board[y][x] == color:
                    score+=1
        return score

    def find_moves_for_board(self, board, p1_color, p2_color):
        # Finds all valid moves that we can make with the current state of the game board
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
        for condition in range(8):
            move_is_valid = 0
            for depth in range(1, 8):
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

    def repaint_the_cells(self, board, y, x, p1_color, p2_color): 
        # Repaints p2_color cells in p1_color after obtaining a cell with coordinates (x, y)
        direction_y = [1, 1, 0, -1, -1, -1,  0,  1] # 1 - lower, -1 - higher
        direction_x = [0, 1, 1,  1,  0, -1, -1, -1] # 1 - right, -1 - left
        for condition in range(8):
            repainting_is_valid = 0
            for depth in range(8):
                new_y = y + depth * direction_y[condition]
                new_x = x + depth * direction_x[condition]
                if (-1 < new_x < 8) and (-1 < new_y < 8):
                    if board[new_y][new_x] == p2_color:
                        # we need to cover at least one opponent's cell to make a move
                        repainting_is_valid = 1 
                    elif board[new_y][new_x] == p1_color and repainting_is_valid == 1:
                        # Go back and repaint all the cells
                        for hight in range(depth - 1, 0, -1):
                            new_y = y + hight * direction_y[condition]
                            new_x = x + hight * direction_x[condition]
                            if board[new_y][new_x] == p2_color:
                                board[new_y][new_x] = p1_color
                        break
                    elif depth == 0:
                        board[new_y][new_x] = p1_color
                    else:
                        # There is no valid move in this direction
                        break
                else:
                    # out of board, change direction
                    break 
        return board



    