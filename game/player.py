"""
Module is responsible for handling the players playing 'I Refuse'.

 Author: Jacob Delgado
 Date: Mar 6, 2016
"""


class Players(object):
    """
    Represents the list of all players in the game.

    Interface is similar to an array of players objects.
    """

    def __init__(self, number):
        self.players = []
        self.index = 0
        for i in range(number):
            self.players.append(Player(i))

    def next_player(self, player=None):
        """
        Gets the next player in the players list by turn order. This will
        repeat in a cycle.

        :param player: Player who just took a turn.
        :return: The next player who will take a turn.
        """
        if not player:
            return self.players[0]

        index = self.players.index(player)
        index = (index + 1) % len(self.players)
        return self.players[index]

    def __len__(self):
        return len(self.players)

    def __iter__(self):
        """
        Allows the Players object to be used as an iterable object.

        :return: A reference to the iter.
        """
        self.index = 0
        return self

    def __next__(self):
        """
        Python 3 construct to get the next element in the players list.

        :return: The next player in the list. Will throw StopIteration when
        the list has been exhausted.
        """
        if self.index == len(self.players):
            raise StopIteration

        current_index = self.index
        self.index += 1
        return self.players[current_index]

    def __getitem__(self, index):
        """
        Allow a players object to access elements similar to an array.

        :param index: The index to a player playing the game.
        :return: A player object referenced by index.
        """
        return self.players[index]


class Player(object):
    """
    A player in the game. Every player starts with an empty hand and with 11
    tokens.
    """
    STARTING_TOKENS = 11

    def __init__(self, number):
        self.cards = []
        self.tokens = Player.STARTING_TOKENS
        self.number = number

    def __str__(self):
        return "Player {}".format(self.number)

    def passes(self):
        """
        The player wishes to pass. If the player can pass (has a token),
        then they are allowed and a token is subtracted from their hand. No
        state is changed if they cannot pass.

        :return: A boolean indicating whether the player was able to pass.
        """
        if not self.can_pass():
            raise AssertionError("Player cannot pass without any tokens")
        self.tokens -= 1

    def can_pass(self):
        """
        The user is only allowed to pass if they have one or more tokens.

        :return: Boolean if they have >= 1 token.
        """
        return self.tokens != 0

    def take_card(self, card, tokens):
        """


        :param card:
        :param tokens:
        :return:
        """
        self.cards.append(card)
        self.tokens += tokens

    def calculate_points(self):
        """
        Calculate the number of points the user has given their cards and
        tokens.

        :return: The number of points the user currently has.
        """
        points = 0
        card_in_sequence = 0
        cards = sorted(self.cards)
        for card in cards:
            if not self.__next_card_in_sequence(card, card_in_sequence):
                points += card
            card_in_sequence = card
        return points - self.tokens

    def stats(self):
        """
        Stats for the given player

        :return: A string of the players given hand and number of current
        points.
        """
        cards = sorted(self.cards)
        return "{}: cards = {}; tokens = {}; points = {}"\
            .format(self.__str__(),
                    cards,
                    self.tokens,
                    self.calculate_points())

    @staticmethod
    def __next_card_in_sequence(card, card_in_sequence):
        """

        :param card: Current card in player's hands.
        :param card_in_sequence: Previous card in player's hand.
        :return: True/False if the current card follows the previous card.
        """
        return card == card_in_sequence + 1
