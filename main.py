#!/usr/bin/python -tt
from game.engine import play_game
from game.setup import setup_players, setup_cards


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
