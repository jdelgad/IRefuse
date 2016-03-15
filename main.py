#!/usr/bin/python -tt
"""
 Author: Jacob Delgado
 Date: Mar 6, 2016
"""
import irefuse.irefuse


def main():
    """
    Main function

    :return: None
    """
    game_play = irefuse.irefuse.IRefuse()
    game_play.setup(input)
    winners = game_play.play(input)

    print("\n------------")
    print("The winners are:")
    for winner in winners:
        print(winner)


if __name__ == "__main__":
    main()
