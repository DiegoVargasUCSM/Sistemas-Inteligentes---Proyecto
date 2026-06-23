class Card:
    def __init__(self, card_id, symbol):
        self.id = card_id
        self.symbol = symbol
        self.is_revealed = False
        self.is_matched = False
        self.position = (0, 0)

    def reveal(self):
        if not self.is_matched and not self.is_revealed:
            self.is_revealed = True

    def hide(self):
        if not self.is_matched:
            self.is_revealed = False

    def match(self):
        self.is_matched = True
        self.is_revealed = True

    def is_match(self, other):
        return self.symbol == other.symbol

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.id == other.id
        return False

    def __repr__(self):
        return self.symbol if self.is_revealed else "?"
