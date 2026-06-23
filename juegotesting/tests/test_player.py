import pytest
from src.player import Player


class TestPlayer:
    def test_player_initialization(self):
        p = Player()
        assert p.attempts == 0
        assert p.pairs_found == 0
        assert p.is_winner is False

    def test_increment_attempts(self):
        p = Player()
        p.increment_attempts()
        assert p.attempts == 1
        p.increment_attempts()
        assert p.attempts == 2

    def test_add_pair(self):
        p = Player()
        p.add_pair()
        assert p.pairs_found == 1
        p.add_pair()
        assert p.pairs_found == 2

    def test_is_winner_with_no_pairs(self):
        p = Player()
        assert p.is_winner is False

    def test_is_winner_after_adding_all_pairs(self):
        p = Player(total_pairs=1)
        p.add_pair()
        assert p.is_winner is True

    def test_reset(self):
        p = Player()
        p.increment_attempts()
        p.add_pair()
        p.reset()
        assert p.attempts == 0
        assert p.pairs_found == 0
        assert p.is_winner is False

    def test_total_cards_affects_win_condition(self):
        p = Player(total_pairs=4)
        for _ in range(3):
            p.add_pair()
        assert p.is_winner is False
        p.add_pair()
        assert p.is_winner is True

    def test_score_property(self):
        p = Player(total_pairs=4)
        p.increment_attempts()
        p.increment_attempts()
        p.add_pair()
        assert p.score == "Pares: 1/4 - Intentos: 2"

    def test_time_limit_default(self):
        p = Player()
        assert p.time_limit == 100

    def test_time_limit_custom(self):
        p = Player(total_pairs=4, time_limit=30)
        assert p.time_limit == 30

    def test_is_loser_when_not_complete(self):
        p = Player(total_pairs=4)
        assert p.is_loser is True

    def test_is_loser_when_complete(self):
        p = Player(total_pairs=1)
        p.add_pair()
        assert p.is_loser is False
        assert p.is_winner is True
