import random
import sys

import game.player


def setup_players(input_func):
    """
    Sets up the number of players. Must be between 3-5.

    :param input_func: Used for mocking input()
    :return: A list of game.player.Player objects
    """
    sys.stdout.write("Enter the number of players [3-5]: ")
    num = int(input_func())
    if num < 3 or num > 5:
        raise AssertionError("invalid number of players")
    players = []
    for i in range(num):
        players.append(game.player.Player())
    return players


def setup_cards():
    """
    :return: A list of randomized 24 cards ranging from 3-35.
    """
    return random.sample(range(3, 36), 24)