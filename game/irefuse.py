"""
Module is responsible for handling of game/business logic behind 'I Refuse'

 Author: Jacob Delgado
 Date: Mar 6, 2016
"""
import random
import sys

from game.player import Players


class Game(object):
    """
    The game logic behind 'I Refuse.'
    """

    def __init__(self):
        self.cards = []
        self.players = None

    def setup(self, input_func):
        """
        Sets up the card game.

        :param input_func: The function to use to prompt the user with.
        :return: None
        """
        self.cards = self.setup_cards()
        self.players = self.setup_players(input_func)

    @staticmethod
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

    @staticmethod
    def setup_cards():
        """
        :return: A list of randomized 24 cards ranging from 3-35.
        """
        return random.sample(range(3, 36), 24)

    def determine_winner(self):
        """
        Calculate who won. Ties can occur.

        :return: The list of winners.
        """
        player_totals = {}
        for player in self.players:
            if player.calculate_points() in player_totals:
                player_totals[player.calculate_points()].append(player)
            else:
                player_totals[player.calculate_points()] = [player]

        sorted_totals = sorted(player_totals.keys())
        return player_totals[sorted_totals[0]]

    def play(self, input_func):
        """
        Business logic for I Refuse. Coordinates how the game is played.

        :param input_func: Input function to prompt the user.
        :return: The list of winners after a game has been completed.
        """
        max_flips = len(self.cards)
        player = self.players.next_player()
        for i in range(max_flips):
            card = self.flip_card()
            tokens = 0
            while not self.prompt_for_action(card, tokens, input_func, player):
                tokens += 1
                player = self.players.next_player(player)

        return self.determine_winner()

    @staticmethod
    def prompt_for_action(card, tokens, input_func, player):
        """
        Prompts the user for action, returns true if the user takes a cards, false otherwise.

        :param card: The card currently face up.
        :param tokens: The amount of tokens on the face up card.
        :param input_func: Prompt for user input.
        :param player: The player whose action it is.
        :return: True if the user took the card, false if not.
        """
        if not player.can_pass():
            player.take_card(card, tokens)
            return True

        action = 0
        while not (action == 1 or action == 2):
            print("\nAvailable card: {}, Number of tokens: {}".format(card, tokens))
            print("What action do you wish to perform: ")
            print("1. Pass")
            print("2. Take card")
            print("------------")
            sys.stdout.write("Selection: ")
            action = int(input_func())

        if action == 1:
            player.passes()
            return False
        elif action == 2:
            player.take_card(card, tokens)
            return True

    def flip_card(self):
        """
        Flips the top card on the deck

        :return: The newest card to be face up.
        """
        return self.cards.pop()
