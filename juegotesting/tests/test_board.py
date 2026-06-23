import pytest
from src.board import Board


class TestBoard:
    def test_board_creation_with_pairs(self):
        board = Board(4, 4)
        assert board.rows == 4
        assert board.cols == 4
        total_cards = board.rows * board.cols
        assert total_cards % 2 == 0
        assert len(board.cards) == total_cards

    def test_board_has_paired_symbols(self):
        board = Board(4, 4)
        symbols = [card.symbol for card in board.cards]
        for symbol in set(symbols):
            assert symbols.count(symbol) == 2

    def test_select_card_returns_card(self):
        board = Board(2, 2)
        card = board.select_card(0, 0)
        assert card is not None
        assert card.id >= 0

    def test_select_card_reveals_it(self):
        board = Board(2, 2)
        card = board.select_card(0, 0)
        assert card.is_revealed is True

    def test_select_out_of_bounds_returns_none(self):
        board = Board(2, 2)
        assert board.select_card(5, 5) is None
        assert board.select_card(-1, 0) is None

    def test_check_match_with_matching_pair(self):
        board = Board(2, 2)
        card1 = board.select_card(0, 0)
        symbol = card1.symbol
        for i, card in enumerate(board.cards):
            if card.symbol == symbol and card.id != card1.id:
                card2 = board.select_card(i // board.cols, i % board.cols)
                break
        assert board.check_match() is True

    def test_check_match_with_non_matching_pair(self):
        board = Board(4, 4)
        card1 = board.select_card(0, 0)
        for card in board.cards:
            if card.symbol != card1.symbol and not card.is_revealed:
                board.select_card(card.position[0], card.position[1])
                break
        assert board.check_match() is False

    def test_is_complete_returns_false_initially(self):
        board = Board(2, 2)
        assert board.is_complete() is False

    def test_is_complete_returns_true_when_all_matched(self):
        board = Board(2, 2)
        for card in board.cards:
            card.match()
        assert board.is_complete() is True

    def test_reset_selection_clears_revealed_unmatched(self):
        board = Board(4, 4)
        card1 = board.select_card(0, 0)
        card2 = board.select_card(0, 1)
        card1.reveal()
        card2.reveal()
        board.revealed_cards = [card1, card2]
        board.reset_selection()
        assert card1.is_revealed is False
        assert card2.is_revealed is False
        assert len(board.revealed_cards) == 0

    def test_auto_match_when_pair_found(self):
        board = Board(2, 2)
        card1 = board.select_card(0, 0)
        for card in board.cards:
            if card.symbol == card1.symbol and card.id != card1.id:
                board.select_card(card.position[0], card.position[1])
                break
        assert board.check_match() is True
        assert card1.is_matched is True

    def test_board_has_correct_number_of_each_symbol(self):
        board = Board(4, 4)
        symbols = [c.symbol for c in board.cards]
        for s in set(symbols):
            assert symbols.count(s) == 2

    def test_symbols_are_geometric_shapes(self):
        board = Board(4, 4)
        allowed = {"circle", "square", "triangle", "diamond", "star", "heart", "pentagon", "hexagon", "cross", "moon", "arrow", "bolt", "ring", "drop", "spade", "club"}
        for card in board.cards:
            assert card.symbol in allowed, f"Symbol '{card.symbol}' not in geometric shapes"
