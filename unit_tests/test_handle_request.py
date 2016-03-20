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
import shutil
import unittest

from restful.handle_request import JoinRequestHandler, \
    StatusRequestHandler, StartRequestHandler
from unit_tests.utfiles import get_input, get_expected, remove_players_list, \
    remove_current_game, get_expected_json

CURRENT_GAME_JSON = "current_game.json"
PLAYERS_JSON = "players.json"

START_GAME = "start_game"
JOIN_GAME = "join_game"
PLAYERS = "players"
STATUS = "status"


def get_game(request_handler, filename):
    with open(get_input(filename)) as data_file:
        data = json.load(data_file)
        game = request_handler.handle(data)
        # cards must be zeroed out since they are randomized
        game["cards"] = []
    return game


def get_output_json(request_handler, filename):
    with open(get_input(filename)) as data_file:
        data = json.load(data_file)
        game = request_handler.handle(data)
        output_json = json.loads(game)
    return output_json


class TestStartRequestHandler(unittest.TestCase):

    def setUp(self):
        remove_current_game()
        remove_players_list()
        self.request_handler = StartRequestHandler()

    def test_handle_start_game(self):
        game = get_game(self.request_handler, START_GAME)

        expected_json = get_expected_json(START_GAME)
        self.assertEquals(game, expected_json)

    def test_handle_start_game_but_game_in_progress(self):
        shutil.copy(get_expected(START_GAME), CURRENT_GAME_JSON)
        output_json = get_output_json(self.request_handler, START_GAME)
        expected_json = get_expected_json("start_game_but_game_in_progress")
        self.assertEquals(output_json, expected_json)


class TestJoinRequestHandler(unittest.TestCase):
    def setUp(self):
        remove_current_game()
        remove_players_list()
        self.request_handler = JoinRequestHandler()

    def test_handle_join_game_allowed(self):
        shutil.copy(get_expected(PLAYERS), PLAYERS_JSON)
        shutil.copy(get_expected(START_GAME), CURRENT_GAME_JSON)
        game = get_game(self.request_handler, JOIN_GAME)

        expected_json = get_expected_json(JOIN_GAME)
        self.assertEquals(game, expected_json)

        expected_json = get_expected_json("join_players")
        with open(PLAYERS_JSON) as expected:
            players = json.load(expected)
        self.assertEquals(players, expected_json)

    def test_handle_join_game_with_none_in_progress(self):
        output_json = get_output_json(self.request_handler, JOIN_GAME)
        expected_json = get_expected_json("join_game_no_game_in_progress")
        self.assertEquals(output_json, expected_json)

    def test_handle_join_but_game_is_full(self):
        shutil.copy(get_expected("all_players_in_game"), PLAYERS_JSON)
        shutil.copy(get_expected(START_GAME), CURRENT_GAME_JSON)
        output_json = get_output_json(self.request_handler, JOIN_GAME)
        expected_json = get_expected_json("join_game_but_game_is_full")
        self.assertEquals(output_json, expected_json)

    def test_handle_join_but_player_already_in_full_game(self):
        shutil.copy(get_expected("all_players_in_game_join"),
                    PLAYERS_JSON)
        shutil.copy(get_expected(START_GAME), CURRENT_GAME_JSON)
        output_json = get_output_json(self.request_handler, JOIN_GAME)
        expected_json = get_expected_json("join_player_already_in_full_game")
        self.assertEquals(output_json, expected_json)

    def test_handle_join_but_player_already_in_game_waiting(self):
        shutil.copy(get_expected("all_players_in_game_waiting"),
                    PLAYERS_JSON)
        shutil.copy(get_expected(START_GAME), CURRENT_GAME_JSON)
        output_json = get_output_json(self.request_handler, JOIN_GAME)
        expected_json = get_expected_json("join_player_already_in_game_waiting")
        self.assertEquals(output_json, expected_json)


class TestStatusRequestHandler(unittest.TestCase):
    def setUp(self):
        remove_current_game()
        remove_players_list()
        self.request_handler = StatusRequestHandler()

    def test_handle_status_waiting_for_players(self):
        shutil.copy(get_expected(PLAYERS), PLAYERS_JSON)
        shutil.copy(get_expected(START_GAME), CURRENT_GAME_JSON)
        output_json = get_output_json(self.request_handler, STATUS)
        expected_json = get_expected_json("status_waiting_to_start")
        self.assertEquals(output_json, expected_json)

    def test_handle_status_no_game_in_progress(self):
        output_json = get_output_json(self.request_handler, STATUS)
        expected_json = get_expected_json("status_no_game_started")
        self.assertEquals(output_json, expected_json)

    def test_handle_status_players_turn(self):
        shutil.copy(get_expected("all_players_turn"), PLAYERS_JSON)
        shutil.copy(get_expected(START_GAME), CURRENT_GAME_JSON)
        output_json = get_output_json(self.request_handler, STATUS)
        expected_json = get_expected_json("status_players_turn")
        self.assertEquals(output_json, expected_json)

    def test_handle_status_not_players_turn(self):
        shutil.copy(get_expected("all_players_no_turn"), PLAYERS_JSON)
        shutil.copy(get_expected(START_GAME), CURRENT_GAME_JSON)
        output_json = get_output_json(self.request_handler, STATUS)
        expected_json = get_expected_json("status_players_no_turn")
        self.assertEquals(output_json, expected_json)
