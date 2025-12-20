class Evaluation:
    SCORE_WIN = 1000000
    SCORE_OPEN_FOUR = 50000
    SCORE_BROKEN_FOUR = 10000
    SCORE_CLOSED_FOUR = 3000
    SCORE_BROKEN_THREE = 2000
    SCORE_OPEN_THREE = 800
    SCORE_CLOSED_THREE = 200

    def evaluate(self, board, player):
        opponent = -player

        term, winner = board.is_terminal_state()
        if term:
            if winner == player:
                return self.SCORE_WIN
            elif winner == opponent:
                return -self.SCORE_WIN
            else:
                return 0

        my_score = self.score_player(board, player)
        opp_score = self.score_player(board, opponent)

        return my_score - opp_score

    def score_player(self, board, player):
        score = 0

        if board.count_open_fours(player) > 0 and board.count_open_threes(player) > 0:
            score += self.SCORE_WIN // 2

        score += board.count_open_fours(player) * self.SCORE_OPEN_FOUR

        score += board.count_broken_fours(player) * self.SCORE_BROKEN_FOUR

        score += board.count_closed_fours(player) * self.SCORE_CLOSED_FOUR

        score += board.count_open_threes(player) * self.SCORE_OPEN_THREE

        score += board.count_broken_threes(player) * self.SCORE_BROKEN_THREE

        score += board.count_closed_threes(player) * self.SCORE_CLOSED_THREE

        return score
