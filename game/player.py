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
