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
import os


def get_current_directory():
    return os.path.dirname(os.path.realpath(__file__))


def get_input(file):
    return "{}/requests/input/{}.json".format(get_current_directory(), file)


def get_output(file):
    return "{}/requests/output/{}.json".format(get_current_directory(), file)


def get_expected(file):
    return "{}/requests/expected/{}.json".format(get_current_directory(), file)


def remove_players_list():
    try:
        os.remove("players.json")
    except FileNotFoundError:
        pass


def remove_current_game():
    try:
        os.remove("current_game.json")
    except FileNotFoundError:
        pass
