# -*- encoding: UTF-8 -*-
"""
'I Refuse' web application
Copyright (C) 2017  Jacob Delgado

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import json
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


def get_json(filename):
    with open(filename) as current:
        game_json = json.load(current)
    return game_json


def get_expected_json(filename):
    with open(get_expected(filename)) as expected:
        expected_json = json.load(expected)
    return expected_json
