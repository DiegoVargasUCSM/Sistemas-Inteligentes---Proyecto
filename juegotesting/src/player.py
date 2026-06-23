class Player:
    def __init__(self, total_pairs=8, time_limit=100):
        self.total_pairs = total_pairs
        self.time_limit = time_limit
        self.attempts = 0
        self.pairs_found = 0
        self.is_winner = False

    def increment_attempts(self):
        self.attempts += 1

    def add_pair(self):
        self.pairs_found += 1
        if self.pairs_found >= self.total_pairs:
            self.is_winner = True

    @property
    def is_loser(self):
        return not self.is_winner and self.pairs_found < self.total_pairs

    def reset(self):
        self.attempts = 0
        self.pairs_found = 0
        self.is_winner = False

    @property
    def score(self):
        return f"Pares: {self.pairs_found}/{self.total_pairs} - Intentos: {self.attempts}"
