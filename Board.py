class Board:

    def __init__(self, n=None):
        self.n = n
        if n is None:
            self.n = 15
        elif n < 5:
            raise ValueError("Board size n must be at least 5")
        self.moves_made = 0
        self.board = [[0] * self.n for _ in range(self.n)]

    def __str__(self):
        rows = []
        for r in self.board:
            row = ""
            for cell in r:
                if cell == 1:
                    row += "X "
                elif cell == -1:
                    row += "O "
                else:
                    row += ". "
            rows.append(row)
        return "\n".join(rows)

    def get_board(self):
        return self.board

    def is_valid(self, row, column):
        if not (0 <= row < self.n and 0 <= column < self.n):
            raise IndexError("Move is outside the board boundaries.")
        if self.board[row][column] != 0:
            raise ValueError("Tile is already occupied.")
        return True

    def move(self, row, column, player):
        self.is_valid(row, column)
        self.board[row][column] = player
        self.moves_made += 1

    def undo_move(self, row, column):
        self.board[row][column] = 0
        self.moves_made -= 1

    def get_legal_moves(self):
        return [(r, c) for r in range(self.n)
                for c in range(self.n)
                if self.board[r][c] == 0]

    @staticmethod
    def line_to_string(line):
        s = ""
        for cell in line:
            if cell == 1:
                s += 'X'
            elif cell == -1:
                s += 'O'
            else:
                s += '_'
        return s

    def get_all_lines(self):
        lines = []

        for r in range(self.n):
            lines.append(self.board[r])

        for c in range(self.n):
            col = [self.board[r][c] for r in range(self.n)]
            lines.append(col)

        for d in range(-(self.n - 1), self.n):
            diag = [self.board[r][r - d] for r in range(self.n)
                    if 0 <= r - d < self.n]
            if len(diag) >= 5:
                lines.append(diag)

        for d in range(0, 2 * self.n - 1):
            anti = [self.board[r][d - r] for r in range(self.n)
                    if 0 <= d - r < self.n]
            if len(anti) >= 5:
                lines.append(anti)

        return lines

    def count_closed_fours(self, player):
        symbol = 'X' if player == 1 else 'O'
        empty = '_'
        block = 'O' if player == 1 else 'X'

        patterns = [
            block + symbol * 4 + empty,
            empty + symbol * 4 + block,
        ]

        count = 0
        for line in self.get_all_lines():
            s = self.line_to_string(line)
            for pat in patterns:
                count += s.count(pat)
        return count

    def count_closed_threes(self, player):
        symbol = 'X' if player == 1 else 'O'
        empty = '_'
        block = 'O' if player == 1 else 'X'

        patterns = [
            block + symbol * 3 + empty,
            empty + symbol * 3 + block,
        ]

        count = 0
        for line in self.get_all_lines():
            s = self.line_to_string(line)
            for pat in patterns:
                count += s.count(pat)
        return count

    def count_open_threes(self, player):
        symbol = 'X' if player == 1 else 'O'
        empty = '_'

        pattern = empty + symbol * 3 + empty

        count = 0
        for line in self.get_all_lines():
            s = self.line_to_string(line)
            count += s.count(pattern)
        return count

    def count_broken_threes(self, player):
        symbol = 'X' if player == 1 else 'O'
        empty = '_'

        patterns = [
            empty + symbol * 2 + empty + symbol + empty,
            empty + symbol + empty + symbol * 2 + empty,
        ]

        count = 0
        for line in self.get_all_lines():
            s = self.line_to_string(line)
            for pat in patterns:
                count += s.count(pat)
        return count

    def count_open_fours(self, player):
        symbol = 'X' if player == 1 else 'O'
        empty = '_'

        pattern = empty + symbol * 4 + empty

        count = 0
        for line in self.get_all_lines():
            s = self.line_to_string(line)
            count += s.count(pattern)
        return count

    def count_broken_fours(self, player):
        symbol = 'X' if player == 1 else 'O'
        empty = '_'

        patterns = [
            symbol + empty + symbol * 3,
            symbol * 3 + empty + symbol,
        ]

        count = 0
        for line in self.get_all_lines():
            s = self.line_to_string(line)
            for pat in patterns:
                count += s.count(pat)
        return count

    def check_win(self, row, col, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for dr, dc in directions:
            count = 1
            r, c = row + dr, col + dc
            while 0 <= r < self.n and 0 <= c < self.n and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc

            r, c = row - dr, col - dc
            while 0 <= r < self.n and 0 <= c < self.n and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc

            if count >= 5:
                return True

        return False

    def is_terminal_state(self, last_move=None, player=None):

        if last_move is not None and player is not None:
            r, c = last_move
            if self.check_win(r, c, player):
                return True, player

        for r in range(self.n):
            for c in range(self.n):
                p = self.board[r][c]
                if p != 0 and self.check_win(r, c, p):
                    return True, p

        if self.moves_made == self.n * self.n:
            return True, 0

        return False, None