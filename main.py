#!/usr/bin/env python -tt

import random
import game.player


def setup_players(input_func):
    print("Number of players: ")
    num = input_func()
    if num < 3 or num > 5:
        raise AssertionError("invalid number of players")
    players = []
    for i in range(num):
        players.append(game.player.Player())
    return players


def setup_cards():
    return random.sample(range(3, 36), 24)


def flip_card(cards):
    return cards.pop()


def prompt_for_action(card, tokens, input_func, player):
    if not player.can_pass():
        player.take_card(card, tokens)
        return

    action = 0
    while not (action == 1 or action == 2):
        print("\nAvailable card: {}".format(card))
        print("What action do you wish to perform: ")
        print("1. Pass")
        print("2. Accept card")
        action = input_func()

    if action == 1:
        player.passes()
    elif action == 2:
        player.take_card(card, tokens)


def determine_winner(players):
    player_totals = {}
    for player in players:
        if player.calculate_points() in player_totals:
            player_totals[player.calculate_points()].append(player)
        else:
            player_totals[player.calculate_points()] = [player]

    sorted_totals = sorted(player_totals.keys())
    print(player_totals)
    return player_totals[sorted_totals[0]]


def main():
    players = setup_players(input)
    cards = setup_cards()

if __name__ == "__main__":
    main()


