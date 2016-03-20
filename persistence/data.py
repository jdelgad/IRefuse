"""
Module is responsible for handling the persistence layer between web service
and backend.
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
import hashlib
import json
import os

from irefuse.irefuse import IRefuse

CURRENT_GAME_JSON = "current_game.json"
PLAYERS_JSON = "players.json"


def write_object_to_file(filename, obj):
    with open(filename, "w") as current:
        json.dump(obj, current)


def write_json_to_file(filename, obj):
    with open(filename, "w") as current:
        current.write(obj)


def read_json_from_file(filename):
    with open(filename, "r") as game:
        return json.loads(game.readlines()[-1])


class GameJournal(object):
    def __init__(self):
        self.game = None
        self.players = None

    def start(self, json_request):
        if self.is_started():
            raise AssertionError("only 1 game allowed at a single time")

        players = self.__initialize_players(json_request)
        game = self.__initialize_game(json_request)
        self.__record(players, game)

    def read(self):
        if not self.is_started():
            raise FileNotFoundError("no game started")
        self.game = read_json_from_file(CURRENT_GAME_JSON)
        self.players = self.get_players()

    def get_game_in_progress(self):
        return read_json_from_file(CURRENT_GAME_JSON)

    def get_players(self):
        return read_json_from_file(PLAYERS_JSON)

    def is_started(self):
        return os.path.exists(CURRENT_GAME_JSON) or os.path.exists(PLAYERS_JSON)

    def __initialize_game(self, json_request):
        def number_of_players():
            return json_request["players"]

        game = IRefuse()
        game.setup(number_of_players)
        return game

    def __initialize_players(self, json_request):
        players = {}
        for i in range(json_request["players"]):
            players[i] = None
        players[0] = self.__get_player_hash(json_request)
        return players

    def __record(self, players, game):
        self.__record_players(players)
        self.record_game(game)

    def record_game(self, game):
        write_json_to_file(CURRENT_GAME_JSON, game.serialize())

    def __record_players(self, players):
        write_object_to_file(PLAYERS_JSON, players)

    def add_player_to_game(self, json_request):
        players = self.get_players()

        for player in players:
            if players[player] is None:
                players[player] = self.__get_player_hash(json_request)

    def __get_player_hash(self, json_request):
        return hashlib.md5("{}{}".format(json_request["client_ip"], json_request[
            "client_port"]).encode("utf-8")).hexdigest()

    def is_current_player(self, json_request):
        players = self.get_players()

        return players[self.get_current_player()] == self.__get_player_hash(
            json_request)

    def is_player_in_game(self, json_request):
        players = self.get_players()

        for i in self.players:
            if players[i] == self.__get_player_hash(json_request):
                return True
        return False

    def get_current_player(self):
        return str(self.get_game_in_progress()["players"]["index"])

    def has_enough_players(self):
        players = self.get_players()

        for i in players:
            if players[i] is None:
                return False

        return True
