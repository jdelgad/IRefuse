#!/usr/bin/python -tt
"""
 Author: Jacob Delgado
 Date: Mar 6, 2016
"""
import game.irefuse


def main():
    """
    Main function

    :return: None
    """
    game_play = game.irefuse.Game()
    game_play.setup(input)
    winners = game_play.play(input)

    print("\n------------")
    print("The winners are:")
    for winner in winners:
        print(winner)


if __name__ == "__main__":
    main()
