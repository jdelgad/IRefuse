#!/usr/bin/python -tt
"""
Copyright (c) 2016 Jacob Delgado,
This file is part of I Refuse.

'I Refuse' is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
