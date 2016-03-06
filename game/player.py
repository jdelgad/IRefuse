import sys


class Players(object):
    def __init__(self, number):
        self.players = []
        for i in range(number):
            self.players.append(Player())

    def next(self, player=None):
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

    def determine_winner(self):
        """
        Calculate who won. Ties can occur.

        :return:
        """
        player_totals = {}
        for player in self.players:
            if player.calculate_points() in player_totals:
                player_totals[player.calculate_points()].append(player)
            else:
                player_totals[player.calculate_points()] = [player]

        sorted_totals = sorted(player_totals.keys())
        return player_totals[sorted_totals[0]]


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


def setup_players(input_func):
    """
    Sets up the number of players. Must be between 3-5.

    :param input_func: Used for mocking input()
    :return: A list of game.player.Player objects
    """
    sys.stdout.write("Enter the number of players [3-5]: ")
    number_of_people_playing = int(input_func())
    if number_of_people_playing < 3 or number_of_people_playing > 5:
        raise AssertionError("invalid number of players")
    return Players(number_of_people_playing)
