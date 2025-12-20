import time
from Evaluation import Evaluation
from MoveFilter import get_filtered_moves


class AlphaBetaAgent:
    def __init__(self, depth=2, proximity=2):
        self.max_depth = depth
        self.proximity = proximity
        self.evaluator = Evaluation()
        self.player = None

        self.nodes_expanded = 0
        self.max_depth_reached = 0
        self.last_move_time = 0.0
        self.cutoffs = 0

    def reset_stats(self):
        self.nodes_expanded = 0
        self.max_depth_reached = 0
        self.last_move_time = 0.0
        self.cutoffs = 0


    def choose_move(self, board, player):
        self.player = player
        self.reset_stats()

        start_time = time.perf_counter()

        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        moves = get_filtered_moves(board, self.proximity)

        moves.sort(key=lambda mv: self.center_distance(board, mv))

        for (r, c) in moves:
            board.move(r, c, player)
            score = self.min_value(board, depth=1, alpha=alpha, beta=beta)
            board.undo_move(r, c)

            if score > best_score:
                best_score = score
                best_move = (r, c)

            if best_score > alpha:
                alpha = best_score

        self.last_move_time = time.perf_counter() - start_time
        return best_move


    def min_value(self, board, depth, alpha, beta):
        self.nodes_expanded += 1
        if depth > self.max_depth_reached:
            self.max_depth_reached = depth

        term, winner = board.is_terminal_state()
        if term or depth == self.max_depth:
            return self.evaluator.evaluate(board, self.player)

        opponent = -self.player
        value = float('inf')

        moves = get_filtered_moves(board, self.proximity)
        moves.sort(key=lambda mv: self.center_distance(board, mv))

        for (r, c) in moves:
            board.move(r, c, opponent)
            score = self.max_value(board, depth + 1, alpha, beta)
            board.undo_move(r, c)

            if score < value:
                value = score

            if value <= alpha:
                self.cutoffs += 1
                return value

            if value < beta:
                beta = value

        return value


    def max_value(self, board, depth, alpha, beta):
        self.nodes_expanded += 1
        if depth > self.max_depth_reached:
            self.max_depth_reached = depth

        term, winner = board.is_terminal_state()
        if term or depth == self.max_depth:
            return self.evaluator.evaluate(board, self.player)

        value = float('-inf')

        moves = get_filtered_moves(board, self.proximity)
        moves.sort(key=lambda mv: self.center_distance(board, mv))

        for (r, c) in moves:
            board.move(r, c, self.player)
            score = self.min_value(board, depth + 1, alpha, beta)
            board.undo_move(r, c)

            if score > value:
                value = score

            if value >= beta:
                self.cutoffs += 1
                return value

            if value > alpha:
                alpha = value

        return value


    def center_distance(self, board, move):
        r, c = move
        mid = board.n // 2
        return abs(r - mid) + abs(c - mid)
