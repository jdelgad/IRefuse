#!/usr/bin/python -tt
from game.irefuse import play_game, setup_players
from game.setup import setup_cards
from game.player import setup_players


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
