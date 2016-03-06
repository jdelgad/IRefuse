class Player(object):
    def __init__(self):
        self.cards = []
        self.tokens = 11

    def passes(self):
        if self.can_pass():
            self.tokens -= 1
            return True
        else:
            return False

    def can_pass(self):
        return self.tokens != 0

    def take_card(self, card, tokens):
        self.cards.append(card)
        self.tokens += tokens

    def calculate_points(self):
        points = 0
        card_in_sequence = 0
        for card in self.cards:
            if card != card_in_sequence + 1:
                points += card
            card_in_sequence = card
        return points - self.tokens
