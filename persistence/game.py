# json files representing the current game
import hashlib
import json
import os

CURRENT_GAME_JSON = "current_game.json"
PLAYERS_JSON = "players.json"


class Game(object):
    def __init__(self):
        pass

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


def initialize_players(json_request, number_of_players):
    players = {}
    for i in range(number_of_players()):
        players[i] = None

    players[0] = get_player_hash(json_request)

    game = Game()
    game.record_players(players)


def add_player_to_game(json_request):
    game = Game()
    players = game.get_players()

    for player in players:
        if players[player] is None:
            players[player] = get_player_hash(json_request)


def get_player_hash(json_request):
    return hashlib.md5("{}{}".format(json_request["client_ip"], json_request[
        "client_port"]).encode("utf-8")).hexdigest()


def is_current_player(game, json_request):
    current_game = Game()
    players = current_game.get_players()

    return players[get_current_player(game)] == get_player_hash(
        json_request)


def get_current_player(game):
    return str(game["players"]["index"])


def has_enough_players():
    game = Game()
    players = game.get_players()

    for i in players:
        if players[i] is None:
            return False

    return True


def is_player_in_game(json_request):
    game = Game()
    players = game.get_players()

    for i in players:
        if players[i] == get_player_hash(json_request):
            return True
    return False