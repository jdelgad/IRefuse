"""
Module is responsible for handling of game/business logic behind 'I Refuse'

 Author: Jacob Delgado
 Date: Mar 6, 2016
"""
import random
import sys

from irefuse.player import Players


class IRefuse(object):
    """
    The game logic behind 'I Refuse.'
    """
    USER_PASSES = 1
    USER_TAKES_CARD = 2
    MIN_PLAYERS = 3
    MAX_PLAYERS = 5
    NUMBER_OF_ROUNDS = 24
    MIN_CARD = 3
    MAX_CARD = 36

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
        if number_of_people_playing < IRefuse.MIN_PLAYERS or \
                number_of_people_playing > IRefuse.MAX_PLAYERS:
            raise AssertionError("invalid number of players")
        return Players(number_of_people_playing)

    @staticmethod
    def setup_cards():
        """
        :return: A list of randomized 24 cards ranging from 3-35.
        """
        return random.sample(range(IRefuse.MIN_CARD, IRefuse.MAX_CARD),
                             IRefuse.NUMBER_OF_ROUNDS)

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
        for _ in range(max_flips):
            card = self.flip_card()
            tokens = 0
            action = self.prompt_for_action(card, tokens, input_func, player)

            while action == IRefuse.USER_PASSES:
                tokens += 1
                player.passes()
                player = self.players.next_player(player)
                action = self.prompt_for_action(card, tokens, input_func,
                                                player)
            player.take_card(card, tokens)

        return self.determine_winner()

    def prompt_for_action(self, card, tokens, input_func, current_player):
        """
        Prompts the user for action, returns true if the user takes a cards,
        false otherwise.

        :param card: The card currently face up.
        :param tokens: The amount of tokens on the face up card.
        :param input_func: Prompt for user input.
        :param current_player: The player whose action it is.
        :return: True if the user took the card, false if not.
        """
        if not current_player.can_pass():
            return IRefuse.USER_TAKES_CARD

        action = 0
        for player in self.players:
            print(player.stats())
        while not (action == IRefuse.USER_PASSES or
                   action == IRefuse.USER_TAKES_CARD):
            print("\n{} it is your turn".format(current_player))
            print("Available card: {}, Number of tokens: {}"
                  .format(card, tokens))
            print("What action do you wish to perform: ")
            print("{}. Pass".format(IRefuse.USER_PASSES))
            print("{}. Take card".format(IRefuse.USER_TAKES_CARD))
            print("------------")
            sys.stdout.write("Selection: ")
            action = int(input_func())

        return action

    def flip_card(self):
        """
        Flips the top card on the deck

        :return: The newest card to be face up.
        """
        return self.cards.pop()
