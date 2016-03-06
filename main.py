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


def can_pass(player):
    return player.tokens == 0


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

def main():
    players = setup_players(input)
    cards = setup_cards()

if __name__ == "__main__":
    main()
