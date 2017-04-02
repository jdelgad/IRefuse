# -*- encoding: UTF-8 -*-
"""
'I Refuse' web application
Copyright (C) 2017  Jacob Delgado

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import json
import logging
import random

from irefuse.player import Players

logger = logging.getLogger()


class IRefuse(object):
    """The game logic behind I Refuse."""

    USER_PASSES = 1
    USER_TAKES_CARD = 2
    MIN_PLAYERS = 3
    MAX_PLAYERS = 5
    NUMBER_OF_ROUNDS = 24
    MIN_CARD = 3
    MAX_CARD = 36

    def __init__(self):
        """Constructor for 'I Refuse' game object."""
        self.cards = []
        self.players = None

    def setup(self, input_func):
        """
        Set up the card game.

        :param input_func: The function to use to prompt the user with.
        :return: None
        """
        logger.debug("Setting up I Refuse")
        self.cards = self.setup_cards()
        self.players = self.setup_players(input_func)
        logger.info("Game created with {} players".format(len(self.players)))
        logger.debug("Cards to be used in game: {}".format(self.cards))

    @staticmethod
    def setup_players(input_func):
        """
        Set up the number of players. Must be between 3-5.

        :param input_func: Used for mocking input()
        :return: A list of game.player.Player objects
        """
        print("Enter the number of players [3-5]: ")
        number_of_people_playing = int(input_func())
        if number_of_people_playing < IRefuse.MIN_PLAYERS or \
                number_of_people_playing > IRefuse.MAX_PLAYERS:
            logger.error("Invalid number of players specified: {}"
                         .format(number_of_people_playing))
            raise AssertionError("invalid number of players")
        return Players(number_of_people_playing)

    @staticmethod
    def setup_cards():
        """:return: A list of randomized 24 cards ranging from 3-35."""
        return random.sample(range(IRefuse.MIN_CARD, IRefuse.MAX_CARD),
                             IRefuse.NUMBER_OF_ROUNDS)

    def determine_winner(self):
        """
        Calculate who won. Ties can occur.

        Creates a dictionary of point values to list of players with that
        value. Returns the players with the lowest point value.

        :return: The list of winners.
        """
        player_totals = {}
        for player in self.players:
            if player.calculate_points() in player_totals:
                player_totals[player.calculate_points()].append(player)
            else:
                player_totals[player.calculate_points()] = [player]

        logger.info("Final results: {}".format(self.players))
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

            logger.debug("Available card: {}".format(card))
            while action == IRefuse.USER_PASSES:
                logger.debug("{} passed on {} with {} tokens remaining"
                             .format(player, card, player.tokens))
                tokens += 1
                player.passes()
                player = self.players.next_player(player)
                action = self.prompt_for_action(card, tokens, input_func,
                                                player)
            player.take_card(card, tokens)
            logger.debug("{} took {} and now has {} tokens".format(player, card,
                         player.tokens))

        logger.debug("No more actions")
        # TODO: command or query, but not both
        return self.determine_winner()

    def prompt_for_action(self, card, tokens, input_func, current_player):
        """
        Prompt the user for action. Return enum for user selection.

        :param card: The card currently face up.
        :param tokens: The amount of tokens on the face up card.
        :param input_func: Prompt for user input.
        :param current_player: The player whose action it is.
        :return: The user selection (enum integer).
        """
        # TODO: command or query, but not both
        if not current_player.can_pass():
            return IRefuse.USER_TAKES_CARD

        action = 0
        while not (action == IRefuse.USER_PASSES or
                   action == IRefuse.USER_TAKES_CARD):
            print("\n{} it is your turn".format(current_player))
            print("Available card: {}, Number of tokens: {}"
                  .format(card, tokens))
            print("What action do you wish to perform: ")
            print("{}. Pass".format(IRefuse.USER_PASSES))
            print("{}. Take card".format(IRefuse.USER_TAKES_CARD))
            print("------------")
            print("Selection: ")
            action = int(input_func())

        return action

    def flip_card(self):
        """
        Flip the top card on the deck.

        :return: The newest card to be face up.
        """
        return self.cards.pop()

    def serialize(self):
        """Serialize class to json string."""
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
