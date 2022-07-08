from ai.derivable_state import DerivableState


class EvaluableState(DerivableState):
    """
    EvaluableState provide a score to evaluate the situation
    used as heuristic function in heuristic search
    """

    SCORE_TABLE = {
        'p': 2,
        'a': 3,
        'm': 3,
        'c': 5,
        'k': 5,
        'r': 10,
        'g': 1  # use a small value to ensure that the total result is positive
    }  # 62 in total

    def __init__(self, board, next_side):
        super().__init__(board, next_side)
        self._score = None

    @property
    def score(self):
        if self._score is None:
            self_power = sum(self.SCORE_TABLE[p.lower()] for p in self._get_pieces(self.next_side).values())
            oppo_power = sum(self.SCORE_TABLE[p.lower()] for p in self._get_pieces(self.next_side.opponent).values())
            alive_score = 1 if self._get_general_position(self.next_side) else 0
            self._score = alive_score * self_power / oppo_power
        return self._score