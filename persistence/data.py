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
import hashlib
import json
import os

from typing import Any

from irefuse.irefuse import IRefuse

INDEX = "index"
PLAYERS = "players"
UTF_8 = "utf-8"


def write_object_to_file(filename: str, obj: Any):
    with open(filename, "w") as current:
        json.dump(obj, current)


def write_json_to_file(filename: str, obj: dict):
    with open(filename, "w") as current:
        current.write(obj)


def read_json_from_file(filename: str):
    with open(filename, "r") as game:
        return json.loads(game.readlines()[-1])


def get_player_hash(json_request: dict):
    return hashlib.md5("{}{}".format(json_request["client_ip"],
                                     json_request["client_port"])
                       .encode(UTF_8)).hexdigest()


class GameJournal(object):
    def __init__(self):
        self.game = Game()
        self.players = Players()

    def start(self, json_request: dict) -> None:
        if self.is_started():
            raise AssertionError("only 1 game allowed at a single time")

        self.players.initialize(json_request)
        self.game.initialize(json_request)
        self.__record()
        self.read()

    def read(self) -> None:
        if not self.is_started():
            raise FileNotFoundError("no game started")
        self.game.read()
        self.players.read()

    def get_game_in_progress(self):
        return self.game.get_game()

    def is_started(self) -> bool:
        return self.game.is_started() \
               or self.players.is_active()

    def __record(self) -> None:
        self.players.record()
        self.game.record()

    def add_player_to_game(self, json_request: dict) -> None:
        self.players.add_player(json_request)

    def is_current_player(self, json_request: dict) -> bool:
        return self.players.get_player(self.__get_current_player()) == \
               get_player_hash(json_request)

    def is_player_in_game(self, json_request: dict) -> bool:
        return self.players.in_game(json_request)

    def __get_current_player(self) -> str:
        return str(self.get_game_in_progress()[PLAYERS][INDEX])

    def is_full(self) -> bool:
        return self.players.is_full()


class Game(object):
    CURRENT_GAME_JSON = "current_game.json"

    def __init__(self):
        self.game = None

    def read(self) -> None:
        self.game = read_json_from_file(self.CURRENT_GAME_JSON)

    def is_started(self) -> bool:
        return os.path.exists(self.CURRENT_GAME_JSON)

    def record(self) -> None:
        write_json_to_file(self.CURRENT_GAME_JSON, self.game)

    def initialize(self, json_request: dict) -> None:
        def number_of_players():
            return json_request[PLAYERS]

        game = IRefuse()
        game.setup(number_of_players)
        write_object_to_file(self.CURRENT_GAME_JSON, game.serialize())
        self.read()

    def get_game(self) -> IRefuse:
        return self.game


class Players(object):
    PLAYERS_JSON = "players.json"

    def __init__(self):
        self.players = None

    def initialize(self, json_request: dict) -> dict:
        self.players = {}
        for i in range(json_request[PLAYERS]):
            self.players[i] = None
        self.players[0] = get_player_hash(json_request)
        return self.players

    def add_player(self, json_request: dict) -> None:
        for player in sorted(self.players):
            if self.players[player] is None:
                self.players[player] = get_player_hash(json_request)
                self.record()
                break

    def record(self) -> None:
        write_object_to_file(self.PLAYERS_JSON, self.players)

    def is_full(self) -> bool:
        for i in self.players:
            if self.players[i] is None:
                return False
        return True

    def read(self) -> None:
        self.players = read_json_from_file(self.PLAYERS_JSON)

    def is_active(self) -> bool:
        return os.path.exists(self.PLAYERS_JSON)

    def in_game(self, json_request: dict) -> bool:
        for i in self.players:
            if self.players[i] == get_player_hash(json_request):
                return True
        return False

    def get_player(self, index):
        return self.players[index]
