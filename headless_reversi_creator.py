from game_board import GameBoard
import time, getopt, sys
import random_player
import player


class HeadlessReversiCreator(object):
    '''
    Creator of the Reversi game without the GUI.
    '''

    def __init__(self, player1, player1_color, player2, player2_color, board_size=8):
        '''
        :param player1: Instance of first player
        :param player1_color: color of player1
        :param player2: Instance of second player
        :param player1_color: color of player2
        :param boardSize: Board will have size [boardSize x boardSize]
        '''
        self.board = GameBoard(board_size, player1_color, player2_color)
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.current_player_color = player1_color
        self.player1_color = player1_color
        self.player2_color = player2_color

    def play_game(self):
        '''
        This function contains game loop that plays the game.
        '''
        correct_finish = True
        while self.board.can_play(self.current_player_color):
            startTime = time.time()
            move = self.current_player.move(self.board.get_board_copy())
            endTime = time.time()
            moveTime = (endTime - startTime) * 1000
            if move is None:
                print('Player %d returns None instead of a valid move. Move takes %.3f ms.' % (self.current_player_color, moveTime))
                correct_finish = False
                break
            else:
                print('Player %d wants move [%d,%d]. Move takes %.3f ms.' % (self.current_player_color, move[0], move[1], moveTime))
                if moveTime >= 1000:
                    print("TIME LIMIT EXCEEDED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    return 100
            
            move = (int(move[0]),int(move[1]))
            if self.board.is_correct_move(move, self.current_player_color):
                print('Move is correct')
                self.board.play_move(move, self.current_player_color)

            else:
                print('Player %d made the wrong move [%d,%d]' % (self.current_player_color, move[0], move[1]))
                correct_finish = False
                break

            self.change_player()
            if not self.board.can_play(self.current_player_color):
                print('No possible move for Player %d' % (self.current_player_color))
                self.change_player()
                if self.board.can_play(self.current_player_color):
                    print('Player %d plays again ' % (self.current_player_color))
                else:
                    print('Game over')
            self.board.print_board()
        if correct_finish:
            return self.printFinalScore()
        else:
            print('Game over.')
            if self.current_player_color == self.player1_color:
                print('Winner is player %d.' % (self.player2_color))
            else:
                print('Winner is player %d.' % (self.player1_color))

    def count_score(self, board, color):
        # Counts the amount of cells with particular color
        score = 0
        for y in range(8):
            for x in range(8):
                if board[y][x] == color:
                    score += 1
        return score

    def change_player(self):
        '''
        Change the current_player
        '''
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.current_player_color = self.player2_color
        else:
            self.current_player = self.player1
            self.current_player_color = self.player1_color

    def printFinalScore(self):
        ret = 0
        p1Stones = 0
        p2Stones = 0
        for x in range(self.board.board_size):
            for y in range(self.board.board_size):
                if self.board.board[x][y] == 0:
                    p1Stones += 1
                if self.board.board[x][y] == 1:
                    p2Stones += 1
        if p1Stones > p2Stones:
            ret = 0
        elif p1Stones < p2Stones:
            ret = 1
        else:
            ret = -1
        print('\n\n-----------------------------\n')
        print('Final score:\n\nPlayer%d:Player%d\n\t[%d:%d]\n' % (self.player1_color, self.player2_color, p1Stones, p2Stones))
        if p1Stones > p2Stones:
            print('Player %d wins!' % self.player1_color)
        elif p2Stones > p1Stones:
            print('Player %d wins!' % self.player2_color)
        else:
            print('Draw')
        print('\n-----------------------------\n\n')
        return ret


if __name__ == "__main__":
    (choices, args) = getopt.getopt(sys.argv[1:], "")
    p1_color = 0
    p2_color = 1

    if len(args) == 0:
        print('No arguments given.\nRunning game with two random players.')

        win0 = 0
        win1 = 0
        idx = 1
        # choose players
        for idx in range(65):
            # p1 = AB4TCB_diff.MyPlayer(p1_color, p2_color)
            # p1 = AB4TC_diff.MyPlayer(p1_color, p2_color)
            # p1 = AB4T_diff.MyPlayer(p1_color, p2_color)
            # p1 = AB4T_cntp.MyPlayer(p1_color, p2_color)
            # p1 = AB4_cntp.MyPlayer(p1_color, p2_color)
            # p1 = player.MyPlayer(p1_color, p2_color)
            # p1 = dev_player.MyPlayer(p1_color, p2_color)
            p1 = random_player.MyPlayer(p1_color, p2_color)

            # p2 = AB4TCB_diff.MyPlayer(p2_color, p1_color)
            # p2 = AB4TC_diff.MyPlayer(p2_color, p1_color)
            # p2 = AB4T_diff.MyPlayer(p2_color, p1_color)
            # p2 = AB4T_cntp.MyPlayer(p2_color, p1_color)
            # p2 = AB4_cntp.MyPlayer(p2_color, p1_color)
            p2 = player.MyPlayer(p2_color, p1_color)
            # p2 = dev_player.MyPlayer(p2_color, p1_color)
            # p2 = random_player.MyPlayer(p2_color, p1_color)

            game = HeadlessReversiCreator(p1, p1_color, p2, p2_color, 8)
            result = game.play_game()
            if result == 100:
                print("Time error occured at the %d game!" % idx)
                break
            elif result == 0:
                win0 += 1
            elif result == 1:
                win1 += 1
        print("Games played:", idx)
        print("I won", win1, "games")
        print("I lost", win0, "games")
        print("Draws:", idx - win1 - win0, "games")

    elif len(args) == 1:
        print('One player given in argument.\nRunning game with given player against the random player.')
        p1 = random_player.MyPlayer(p1_color, p2_color)
        try:
            to_import = args[0]
            if ".py" in args[0]:
                to_import = args[0].replace(".py","")
            player_module = __import__(to_import)
            p2 = player_module.MyPlayer(p2_color, p1_color)

            game = HeadlessReversiCreator(p1, p1_color, p2, p2_color, 8)
            game.play_game()

        except ImportError:
            print('Error: Cannot import given player: %s.' %(args[0]))

    else:
        if len(args) > 2:
            print('More than two arguments given. Ignoring other arguments and using only the first and the second as players.')

        importsCorrect = True
        try:
            to_import = args[0]
            if ".py" in args[0]:
                to_import = args[0].replace(".py","")
            player_module = __import__(to_import)
            p1 = player_module.MyPlayer(p1_color, p2_color)
        except ImportError:
            importsCorrect = False
            print('Error: Cannot import given player: %s.' %(args[0]))

        try:
            to_import2 = args[1]
            if ".py" in args[1]:
                to_import2 = args[1].replace(".py","")
            player_module = __import__(to_import2)
            p2 = player_module.MyPlayer(p2_color, p1_color)
        except ImportError:
            importsCorrect = False
            print('Error: Cannot import given player: %s.' %(args[1]))

        if importsCorrect:
            game = HeadlessReversiCreator(p1, p1_color, p2, p2_color, 8)
            game.play_game()

