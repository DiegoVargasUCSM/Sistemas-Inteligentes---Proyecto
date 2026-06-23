import pytest
from src.card import Card


class TestCard:
    def test_card_creation(self):
        card = Card(1, "A")
        assert card.id == 1
        assert card.symbol == "A"
        assert card.is_revealed is False
        assert card.is_matched is False

    def test_card_reveal(self):
        card = Card(1, "A")
        card.reveal()
        assert card.is_revealed is True

    def test_card_hide(self):
        card = Card(1, "A")
        card.reveal()
        card.hide()
        assert card.is_revealed is False

    def test_card_match(self):
        card = Card(1, "A")
        card.match()
        assert card.is_matched is True

    def test_is_match_returns_true_for_same_symbol(self):
        card1 = Card(1, "A")
        card2 = Card(2, "A")
        assert card1.is_match(card2) is True

    def test_is_match_returns_false_for_different_symbols(self):
        card1 = Card(1, "A")
        card2 = Card(2, "B")
        assert card1.is_match(card2) is False

    def test_matched_card_is_revealed(self):
        card = Card(1, "A")
        card.match()
        assert card.is_revealed is True

    def test_cannot_reveal_already_revealed_card(self):
        card = Card(1, "A")
        card.reveal()
        card.reveal()
        assert card.is_revealed is True

    def test_equality_based_on_id(self):
        card1 = Card(1, "A")
        card2 = Card(1, "B")
        assert card1 == card2

    def test_str_representation(self):
        card = Card(1, "A")
        assert str(card) == "?"
        card.reveal()
        assert str(card) == "A"
