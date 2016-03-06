class Players(object):
    def __init__(self, number):
        self.players = []
        self.index = 0
        for i in range(number):
            self.players.append(Player())

    def next_player(self, player=None):
        """
        Gets the next player in the players list.

        :param player: Player who just took a turn.
        :return: The next player who will take a turn.
        """
        if not player:
            return self.players[0]

        index = self.players.index(player)
        index = (index + 1) % len(self.players)
        return self.players[index]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index == len(self.players):
            raise StopIteration
        self.index += 1
        return self.players[self.index-1]

    def __getitem__(self, index):
        return self.players[index]


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
