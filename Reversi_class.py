BLACK = 1
WHITE = -1
VALID_MOVE = 2
REVERSI_CHOICE = 3
DIRECTION = [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, -1), (-1, 1)]
SIZE = 8


class Othello:
    def __init__(self, black_ai, white_ai):
        self.board = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        self.board[3][3], self.board[4][4] = BLACK, BLACK
        self.board[3][4], self.board[4][3] = WHITE, WHITE
        self.black_count = 2
        self.white_count = 2
        self.black_ai = black_ai
        self.white_ai = white_ai
        self.winner = None
        self.current_turn = BLACK
        self.black_set = {(3, 3), (4, 4)}
        self.white_set = {(3, 4), (4, 3)}
        self.valid_move = set()
        self.reversi_choice = dict()
        self.stalemate = 0

    def get_valid_moves_backtrack(self, row, col, direction, visited, flag):
        """
        Called in get_valid_moves. For each owned pieces on the board, use backtrack to find the valid place.
        """
        if not 0 <= row < SIZE or not 0 <= col < SIZE:
            return False
        if visited[row][col]:
            return False
        if self.board[row][col] == 0 and flag:
            self.valid_move.add((row, col))
            self.board[row][col] = VALID_MOVE
            return True
        if self.board[row][col] not in [BLACK, WHITE]:
            return False
        elif self.board[row][col] == -self.current_turn:
            flag = True
        elif self.board[row][col] == self.current_turn and flag:
            return False
        elif self.board[row][col] == self.current_turn:
            visited[row][col] = True
        if self.get_valid_moves_backtrack(row + direction[0], col + direction[1], direction, visited, flag):
            return True

        return False

    def get_valid_moves(self)->bool:
        """
        For the current player, try to find the valid places to drop the piece. if there is at least one valid place,
        return true, otherwise, false.
        :return: boolean
        """
        ans = False
        for d in DIRECTION:
            visited = [[False for _ in range(SIZE)] for _ in range(SIZE)]
            for i in range(SIZE):
                for j in range(SIZE):
                    if self.board[i][j] == self.current_turn:
                        if self.get_valid_moves_backtrack(i, j, d, visited, False):
                            ans = True
        if not ans:
            self.stalemate += 1
            self.current_turn = -self.current_turn

        return ans

    def is_valid(self, grid, color):
        """
        Check if the place user clicked is valid: when in the wait_move function, call is_valid to check if the place
        color is grey, and when in the wait_reversi function, call is_valid to check if the direction is a valid choice
        to reversi. if is valid, return true otherwise false
        :param grid:the grid user chose
        :param color: the color of the grid(the piece type of the grid)
        :return: boolean
        """
        (row, col) = grid
        if self.board[row][col] == color:
            return True
        else:
            return False

    def move(self, grid):
        """
        Drop the piece,update the board information and call the get_reversi_choice to create the valid reversi_choice.
        :param grid: the grid user chose
        :return:
        """
        while self.valid_move:
            (r, c) = self.valid_move.pop()
            self.board[r][c] = 0

        (row, col) = grid
        self.board[row][col] = self.current_turn

        if self.current_turn == BLACK:
            self.black_set.add((row, col))
            self.black_count += 1
        else:
            self.white_set.add((row, col))
            self.white_count += 1

        self.get_reversi_choice(grid)
        return

    def get_reversi_choice(self, grid):
        """
        create the valid reversi_choice.
        :param grid: the grid user chose
        :return:
        """
        # see how many reversi choice are there, and the player could only flip over in one direction
        (row, col) = grid
        for (x, y) in DIRECTION:
            r, c = row + x, col + y
            record = set()
            reward_flag=False
            reward= set()
            while 0 <= r < SIZE and 0 <= c < SIZE:
                if self.board[r][c] == -self.current_turn and not reward_flag:
                    record.add((r, c))
                    r += x
                    c += y
                elif self.board[r][c] == self.current_turn and not reward_flag:
                    if len(record) > 0:
                        reward_flag=True
                        self.reversi_choice[(x, y)] = record
                        for (i, j) in record:
                            self.board[i][j] = REVERSI_CHOICE
                        r += x
                        c += y
                    else:
                        break
                elif self.board[r][c] == -self.current_turn and reward_flag:
                    reward.add((r, c))
                    r += x
                    c += y

                elif self.board[r][c] == self.current_turn and reward_flag:
                    self.reversi_choice[(x, y)] |= reward
                    for (i, j) in reward:
                        self.board[i][j] = REVERSI_CHOICE
                    break
                else:
                    break
        return

    def reversi(self, grid):
        """
        flip over the opponent's pieces.
        :param grid: the grid user chose
        :return:
        """
        choice = None
        for key, values in self.reversi_choice.items():
            if grid in values:
                choice = key

        if self.current_turn == BLACK:
            self.black_count += len(self.reversi_choice[choice])
            self.white_count -= len(self.reversi_choice[choice])
        else:
            self.white_count += len(self.reversi_choice[choice])
            self.black_count -= len(self.reversi_choice[choice])

        # flip over
        while len(self.reversi_choice[choice]) > 0:
            g = self.reversi_choice[choice].pop()
            self.board[g[0]][g[1]] = self.current_turn
            if self.current_turn == BLACK:
                self.black_set.add((g[0], g[1]))
                self.white_set.remove((g[0], g[1]))
            else:
                self.white_set.add((g[0], g[1]))
                self.black_set.remove((g[0], g[1]))
        self.board = [[j if j != REVERSI_CHOICE else -self.current_turn for j in i] for i in self.board]
        self.reversi_choice.clear()
        self.current_turn = -self.current_turn
        return

    def unmake_reversi(self, choice):
        """
        A helper for minimax to undo something.
        :param choice:
        :return:
        """
        if self.current_turn == BLACK:
            self.black_count -= len(self.reversi_choice[choice])
            self.white_count += len(self.reversi_choice[choice])
        else:
            self.white_count -= len(self.reversi_choice[choice])
            self.black_count += len(self.reversi_choice[choice])

        # flip over
        while len(self.reversi_choice[choice]) > 0:
            g = self.reversi_choice[choice].pop()
            self.board[g[0]][g[1]] = -self.current_turn
            if self.current_turn == BLACK:
                self.white_set.add((g[0], g[1]))
                self.black_set.remove((g[0], g[1]))
            else:
                self.black_set.add((g[0], g[1]))
                self.white_set.remove((g[0], g[1]))
        return

    def is_end(self)->bool:
        """
        Check if the game ends, board is full or no move for the last two turns.
        :return: if game ends, call the win_loss to annouce the winner, and return True, otherwise False
        """
        # there are two situations could end the game, if so, call the win_loss to give the winner.
        if self.black_count + self.white_count == SIZE *SIZE or self.stalemate == 2:
            self.win_loss()
            return True
        else:
            return False

    def win_loss(self):
        """
        Return the player who has more pieces on the board. If same, return 0 represent a TIE
        """
        if self.black_count > self.white_count:
            self.winner = BLACK
        elif self.black_count < self.white_count:
            self.winner = WHITE
        else:
            self.winner = 0
