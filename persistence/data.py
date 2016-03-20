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
    CURRENT_GAME_JSON = "current_game.json"
    PLAYERS_JSON = "players.json"

    def __init__(self):
        self.game = None
        self.players = None

    def start(self, json_request):
        if self.is_started():
            raise AssertionError("only 1 game allowed at a single time")

        self.__initialize_players(json_request)
        self.__initialize_game(json_request)
        self.__record()
        self.read()

    def read(self):
        if not self.is_started():
            raise FileNotFoundError("no game started")
        self.game = read_json_from_file(self.CURRENT_GAME_JSON)
        self.players = read_json_from_file(self.PLAYERS_JSON)

    def get_game_in_progress(self):
        return self.game

    def get_players(self):
        return self.players

    def is_started(self):
        return os.path.exists(self.CURRENT_GAME_JSON) \
               or os.path.exists(self.PLAYERS_JSON)

    def __initialize_game(self, json_request):
        def number_of_players():
            return json_request["players"]

        game = IRefuse()
        game.setup(number_of_players)
        self.game = game.serialize()

    def __initialize_players(self, json_request):
        self.players = {}
        for i in range(json_request["players"]):
            self.players[i] = None
        self.players[0] = self.__get_player_hash(json_request)
        return self.players

    def __record(self):
        self.__record_players()
        self.__record_game()

    def __record_game(self):
        write_json_to_file(self.CURRENT_GAME_JSON, self.game)

    def __record_players(self):
        write_object_to_file(self.PLAYERS_JSON, self.players)

    def add_player_to_game(self, json_request):
        for player in sorted(self.players):
            if self.players[player] is None:
                self.players[player] = self.__get_player_hash(json_request)
                self.__record_players()
                break

    @staticmethod
    def __get_player_hash(json_request):
        return hashlib.md5("{}{}".format(json_request["client_ip"],
                                         json_request["client_port"])
                           .encode("utf-8")).hexdigest()

    def is_current_player(self, json_request):
        players = self.get_players()

        return players[self.__get_current_player()] == self.__get_player_hash(
            json_request)

    def is_player_in_game(self, json_request):
        players = self.get_players()

        for i in self.players:
            if players[i] == self.__get_player_hash(json_request):
                return True
        return False

    def __get_current_player(self):
        return str(self.get_game_in_progress()["players"]["index"])

    def has_enough_players(self):
        for i in self.players:
            if self.players[i] is None:
                return False
        return True
