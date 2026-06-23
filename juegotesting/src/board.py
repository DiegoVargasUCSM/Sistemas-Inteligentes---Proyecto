import random
from src.card import Card


class Board:
    def __init__(self, rows=4, cols=4):
        self.rows = rows
        self.cols = cols
        self.revealed_cards = []
        self.cards = []
        self._create_cards()

    def _create_cards(self):
        total = self.rows * self.cols
        num_pairs = total // 2
        shapes = ["circle", "square", "triangle", "diamond", "star", "heart", "pentagon", "hexagon", "cross", "moon", "arrow", "bolt", "ring", "drop", "spade", "club"]
        symbols = [shapes[i] for i in range(num_pairs)]
        symbols = symbols * 2
        random.shuffle(symbols)
        self.cards = []
        for i, symbol in enumerate(symbols):
            card = Card(i, symbol)
            card.position = (i // self.cols, i % self.cols)
            self.cards.append(card)

    def select_card(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return None
        index = row * self.cols + col
        card = self.cards[index]
        if not card.is_matched and not card.is_revealed:
            card.reveal()
            if card not in self.revealed_cards:
                self.revealed_cards.append(card)
        return card

    def check_match(self):
        if len(self.revealed_cards) < 2:
            return False
        card1, card2 = self.revealed_cards[-2], self.revealed_cards[-1]
        if card1.is_match(card2):
            card1.match()
            card2.match()
            return True
        return False

    def reset_selection(self):
        for card in self.revealed_cards:
            card.hide()
        self.revealed_cards = []

    def is_complete(self):
        return all(card.is_matched for card in self.cards)
