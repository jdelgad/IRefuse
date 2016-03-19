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


class GameJournal(object):
    def __init__(self):
        pass

    def initialize(self, json_request):

        players = {}
        for i in range(json_request["players"]):
            players[i] = None

        players[0] = get_player_hash(json_request)
        self.record_players(players)

        def number_of_players():
            return json_request["players"]

        game = IRefuse()
        game.setup(number_of_players)
        self.record_game(self.serialize_game(game))

    def record_game(self, game):
        with open(CURRENT_GAME_JSON, "w") as current:
            current.write(game)

    def record_players(self, players):
        with open(PLAYERS_JSON, "w") as game:
            json.dump(players, game)

    def get_players(self):
        with open(PLAYERS_JSON, "r") as game:
            players = json.loads(game.readlines()[0])
        return players

    def is_started(self):
        return os.path.exists(CURRENT_GAME_JSON) or os.path.exists(PLAYERS_JSON)

    def get_game_in_progress(self):
        with open(CURRENT_GAME_JSON, "r") as game:
            current_game = json.loads(game.readlines()[-1])
        return current_game

    def serialize_game(self, game):
        return json.dumps(game, default=lambda o: o.__dict__)


def add_player_to_game(json_request):
    game = GameJournal()
    players = game.get_players()

    for player in players:
        if players[player] is None:
            players[player] = get_player_hash(json_request)


def get_player_hash(json_request):
    return hashlib.md5("{}{}".format(json_request["client_ip"], json_request[
        "client_port"]).encode("utf-8")).hexdigest()


def is_current_player(game, json_request):
    current_game = GameJournal()
    players = current_game.get_players()

    return players[get_current_player(game)] == get_player_hash(
        json_request)


def get_current_player(game):
    return str(game["players"]["index"])


def has_enough_players():
    game = GameJournal()
    players = game.get_players()

    for i in players:
        if players[i] is None:
            return False

    return True


def is_player_in_game(json_request):
    game = GameJournal()
    players = game.get_players()

    for i in players:
        if players[i] == get_player_hash(json_request):
            return True
    return False
