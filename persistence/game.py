# json files representing the current game
import json
import os

CURRENT_GAME_JSON = "current_game.json"
PLAYERS_JSON = "players.json"


def create_game_record(current_game):
    with open(CURRENT_GAME_JSON, "w") as current:
        current.write(current_game)


def serialize_players(players):
    with open(PLAYERS_JSON, "w") as game:
        json.dump(players, game)


def deserialize_players():
    with open(PLAYERS_JSON, "r") as game:
        players = json.loads(game.readlines()[0])
    return players


def game_has_been_started():
    return os.path.exists(CURRENT_GAME_JSON) or os.path.exists(PLAYERS_JSON)


def get_game_in_progress():
    with open(CURRENT_GAME_JSON, "r") as game:
        current_game = json.loads(game.readlines()[-1])
    return current_game


def get_current_players():
    with open(PLAYERS_JSON) as current_players:
        players = json.loads(current_players.readlines()[0])
    return players
