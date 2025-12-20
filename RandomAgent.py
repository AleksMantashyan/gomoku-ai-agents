import random
import time
from MoveFilter import get_filtered_moves

class RandomAgent:
    def __init__(self, proximity=2):
        self.proximity = proximity

        self.nodes_expanded = 0
        self.max_depth_reached = 0
        self.last_move_time = 0.0

    def choose_move(self, board, player):
        start = time.perf_counter()

        moves = get_filtered_moves(board, self.proximity)
        if not moves:
            return None

        move = random.choice(moves)

        self.nodes_expanded = 1
        self.max_depth_reached = 0
        self.last_move_time = time.perf_counter() - start

        return move
