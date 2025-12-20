import random

def get_filtered_moves(board, proximity=2):

    n = board.n
    stones = []

    for r in range(n):
        for c in range(n):
            if board.board[r][c] != 0:
                stones.append((r, c))

    if not stones:
        mid = n // 2
        return [(mid, mid)]

    candidates = set()

    for (sr, sc) in stones:
        for dr in range(-proximity, proximity + 1):
            for dc in range(-proximity, proximity + 1):
                r = sr + dr
                c = sc + dc
                if 0 <= r < n and 0 <= c < n and board.board[r][c] == 0:
                    candidates.add((r, c))

    moves = list(candidates)
    random.shuffle(moves)
    return moves