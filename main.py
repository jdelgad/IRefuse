#!/usr/bin/env python -tt

import random
import game.player
import sys


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


def flip_card(cards):
    """
    Flips the top card on the deck

    :param cards:
    :return:
    """
    return cards.pop()


def prompt_for_action(card, tokens, input_func, player):
    """
    Prompts the user for action, returns true if the user takes a cards, false otherwise.

    :param card:
    :param tokens:
    :param input_func:
    :param player:
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
        action = int(input_func())

    if action == 1:
        player.passes()
        return False
    elif action == 2:
        player.take_card(card, tokens)
        return True


def determine_winner(players):
    """
    Given the list of all players, calculate who won. Ties can occur.

    :param players:
    :return:
    """
    player_totals = {}
    for player in players:
        if player.calculate_points() in player_totals:
            player_totals[player.calculate_points()].append(player)
        else:
            player_totals[player.calculate_points()] = [player]

    sorted_totals = sorted(player_totals.keys())
    return player_totals[sorted_totals[0]]


def get_next_player(player, players):
    """
    Gets the next player in the players list.

    :param player: Player who just took a turn.
    :param players: Players currently playing.
    :return: The next player who will take a turn.
    """
    index = players.index(player)
    index = (index + 1) % len(players)
    return players[index]


def play_game(players, cards, input_func):
    """
    Rules logic for I Refuse

    :param players:
    :param cards:
    :param input_func:
    :return:
    """
    max_flips = len(cards)
    player = players[0]
    for i in range(max_flips):
        card = flip_card(cards)
        tokens = 0
        while not prompt_for_action(card, tokens, input_func, player):
            tokens += 1
            player = get_next_player(player, players)
        player = get_next_player(player, players)

    return determine_winner(players)


def main():
    """
    Main function

    :return: None
    """
    players = setup_players(input)
    cards = setup_cards()
    play_game(players, cards, input)

if __name__ == "__main__":
    main()
