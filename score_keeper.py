class ScoreKeeper:
    def __init__(self):
        self._score = 0.0
        self._score_scale = 1.0

    def break_brick(self) -> None:
        self._score += 100.0
        self._score_scale += 0.3

    def get_score(self) -> float:
        return self._score

    def hit_puddle(self) -> None:
        self._score += 10.0
        self._score_scale = 1.0
