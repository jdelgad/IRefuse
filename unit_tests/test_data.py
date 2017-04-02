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
import unittest
import shutil

from persistence.data import GameJournal
from unit_tests.utfiles import remove_current_game, remove_players_list, \
    get_expected, get_input, get_expected_json, get_json

CURRENT_GAME_JSON = "current_game.json"
PLAYERS_JSON = "players.json"
START_GAME = "start_game"
PLAYERS = "players"


class TestGameJournal(unittest.TestCase):
    def setUp(self):
        remove_current_game()
        remove_players_list()

    def test_initialization_success(self):
        with open(get_input(START_GAME)) as data_file:
            data = json.load(data_file)
        game = GameJournal()
        game.start(data)

        expected_json = get_expected_json(START_GAME)
        game_json = get_json(CURRENT_GAME_JSON)
        game_json["cards"] = []
        self.assertEquals(game_json, expected_json)

    def test_initialization_fails(self):
        shutil.copy(get_expected(START_GAME), CURRENT_GAME_JSON)
        shutil.copy(get_expected(PLAYERS), PLAYERS_JSON)

        with open(get_input(START_GAME)) as data_file:
            data = json.load(data_file)
        game = GameJournal()
        try:
            game.start(data)
            self.fail("expected failure - only 1 game is allowed currently")
        except BaseException:
            pass

    def test_read_success(self):
        shutil.copy(get_expected(START_GAME), CURRENT_GAME_JSON)
        shutil.copy(get_expected(PLAYERS), PLAYERS_JSON)
        game = GameJournal()
        game.read()

        expected_json = get_expected_json(START_GAME)
        game_json = get_json(CURRENT_GAME_JSON)
        self.assertEquals(expected_json, game_json)

        expected_json = get_expected_json(PLAYERS)
        players_json = get_json(PLAYERS_JSON)
        self.assertEquals(expected_json, players_json)

    def test_read_fails(self):
        game = GameJournal()
        try:
            game.read()
            self.fail("no game should have started")
        except FileNotFoundError:
            pass
