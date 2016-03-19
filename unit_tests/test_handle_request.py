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
import json
import os
import shutil
import unittest

from restful.handle_request import JoinRequestHandler, \
    StatusRequestHandler, StartRequestHandler


def get_input(file):
    return "requests/input/{}.json".format(file)


def get_output(file):
    return "requests/output/{}.json".format(file)


def get_expected(file):
    return "requests/expected/{}.json".format(file)


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


class TestStartRequestHandler(unittest.TestCase):
    def setUp(self):
        remove_current_game()
        remove_players_list()
        self.request_handler = StartRequestHandler()

    def test_handle_start_game(self):
        with open(get_input("start_game")) as data_file:
            data = json.load(data_file)
            game = self.request_handler.handle(data)

            # cards must be zeroed out since they are randomized
            output_json = json.loads(game)
            output_json["cards"] = []

            with open(get_expected("start_game")) as expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)

    def test_handle_start_game_but_game_in_progress(self):
        shutil.copy(get_expected("start_game"), "current_game.json")
        with open(get_input("start_game")) as data_file:
            data = json.load(data_file)
            game = self.request_handler.handle(data)

            output_json = json.loads(game)

            with open(get_expected("start_game_but_game_in_progress")) as \
                    expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)


class TestJoinRequestHandler(unittest.TestCase):
    def setUp(self):
        remove_current_game()
        remove_players_list()
        self.request_handler = JoinRequestHandler()

    def test_handle_join_game_allowed(self):
        shutil.copy(get_expected("players"), "players.json")
        shutil.copy(get_expected("start_game"), "current_game.json")
        with open(get_input("join_game")) as data_file:
            data = json.load(data_file)
            game = self.request_handler.handle(data)

            # cards must be zeroed out since they are randomized
            game["cards"] = []

            with open(get_expected("join_game")) as expected:
                expected_json = json.load(expected)
            self.assertEquals(game, expected_json)

    def test_handle_join_game_with_none_in_progress(self):
        with open(get_input("join_game")) as data_file:
            data = json.load(data_file)
            game = self.request_handler.handle(data)
            output_json = json.loads(game)

            with open(get_expected("join_game_no_game_in_progress")) as \
                    expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)

    def test_handle_join_but_game_is_full(self):
        shutil.copy(get_expected("all_players_in_game"), "players.json")
        shutil.copy(get_expected("start_game"), "current_game.json")
        with open(get_input("join_game")) as data_file:
            data = json.load(data_file)
            game = self.request_handler.handle(data)
            output_json = json.loads(game)

            with open(get_expected("join_game_but_game_is_full")) as \
                    expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)

    def test_handle_join_but_player_already_in_full_game(self):
        shutil.copy(get_expected("all_players_in_game_join"),
                    "players.json")
        shutil.copy(get_expected("start_game"), "current_game.json")
        with open(get_input("join_game")) as data_file:
            data = json.load(data_file)
            game = self.request_handler.handle(data)
            output_json = json.loads(game)

            with open(get_expected("join_player_already_in_full_game")) as \
                    expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)

    def test_handle_join_but_player_already_in_game_waiting(self):
        shutil.copy(get_expected("all_players_in_game_waiting"),
                    "players.json")
        shutil.copy(get_expected("start_game"), "current_game.json")
        with open(get_input("join_game")) as data_file:
            data = json.load(data_file)
            game = self.request_handler.handle(data)
            output_json = json.loads(game)

            with open(get_expected("join_player_already_in_game_waiting")) as \
                    expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)


class TestStatusRequestHandler(unittest.TestCase):
    def setUp(self):
        remove_current_game()
        remove_players_list()
        self.request_handler = StatusRequestHandler()

    def test_handle_status_waiting_for_players(self):
        shutil.copy(get_expected("players"), "players.json")
        shutil.copy(get_expected("start_game"), "current_game.json")
        with open(get_input("status")) as data_file:
            data = json.load(data_file)
            game = self.request_handler.handle(data)
            output_json = json.loads(game)

            with open(get_expected("status_waiting_to_start")) as expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)

    def test_handle_status_no_game_in_progress(self):
        with open(get_input("status")) as data_file:
            data = json.load(data_file)
            game = self.request_handler.handle(data)
            output_json = json.loads(game)

            with open(get_expected("status_no_game_started")) as expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)

    def test_handle_status_players_turn(self):
        shutil.copy(get_expected("all_players_turn"), "players.json")
        shutil.copy(get_expected("start_game"), "current_game.json")
        with open(get_input("status")) as data_file:
            data = json.load(data_file)
            game = self.request_handler.handle(data)
            output_json = json.loads(game)

            with open(get_expected("status_players_turn")) as expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)

    def test_handle_status_not_players_turn(self):
        shutil.copy(get_expected("all_players_no_turn"), "players.json")
        shutil.copy(get_expected("start_game"), "current_game.json")
        with open(get_input("status")) as data_file:
            data = json.load(data_file)
            game = self.request_handler.handle(data)
            output_json = json.loads(game)

            with open(get_expected("status_players_no_turn")) as expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)
