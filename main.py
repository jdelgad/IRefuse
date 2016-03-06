#!/usr/bin/env python -tt

import random

def setup_players(input_func):
    print("Number of players: ")
    num = input_func()
    if num < 3 or num > 5:
        raise AssertionError("invalid number of players")
    return num


def setup_cards():
    return random.sample(range(3, 36), 24)


def main():
    players = setup_players(input)
    cards = setup_cards()

if __name__ == "__main__":
    main()