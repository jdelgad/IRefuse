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


def main():
    players = setup_players(input)
    cards = setup_cards()

if __name__ == "__main__":
    main()
