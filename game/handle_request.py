import hashlib
import json
import os

from game.irefuse import Game


def handle_request(json_request):
    if json_request["action"] == "START":
        if game_has_been_started():
            return '{ "response": 400, "message": "Game is currently in ' \
                   'progress" }'
        current_game = setup_game(json_request)
        with open("current_game.json", "w") as current:
            current.write(current_game)
        add_player_to_game(json_request)
        return current_game
    elif json_request["action"] == "JOIN":
        if game_has_been_started():
            add_player_to_game(json_request)
            return join_game(json_request)
        else:
            return '{ "response": 400, "message": "No game in progress" }'
    elif json_request["action"] == "STATUS":
        return status(json_request)
    else:
        return '{ "response": 400 }'


def setup_game(json_request):
    def number_of_players():
        return json_request["players"]

    initialize_players(json_request, number_of_players)

    game = Game()
    game.setup(number_of_players)
    return json.dumps(game, default=lambda o: o.__dict__)


def initialize_players(json_request, number_of_players):
    players = {}
    for i in range(number_of_players()):
        players[i] = None
    players[0] = get_player_hash(json_request)
    with open("players.json", "w") as game:
        json.dump(players, game)


def add_player_to_game(json_request):
    with open("players.json") as game:
        players = json.loads(game.readlines()[0])

    for i in range(5):
        if i in players:
            if players[i] is None:
                players[i] = get_player_hash(json_request)


def join_game(json_request):
    try:
        with open("current_game.json", "r") as current_game:
            return current_game.readlines()[-1]
    except FileNotFoundError:
        return '{ "response": 400, "message": "No game in progress" }'


def game_has_been_started():
    return os.path.exists("current_game.json")


def get_game_in_progress():
    with open("current_game.json") as game:
        current_game = json.loads(game.readlines()[-1])
    return current_game


def get_player_hash(json_request):
    return hashlib.md5("{}{}".format(json_request["client_ip"], json_request[
        "client_port"]).encode("utf-8")).hexdigest()


def is_current_player(game, json_request):
    with open("players.json") as current_players:
        players = json.loads(current_players.readlines()[0])

    return players[str(game["players"]["index"])] == get_player_hash(
        json_request)


def has_enough_players(game):
    with open("players.json") as current_players:
        players = json.loads(current_players.readlines()[0])

    for i in range(len(game["players"]["players"])):
        if players[str(i)] is None:
            return False

    return True


def status(json_request):
    if game_has_been_started():
        game = get_game_in_progress()

        if has_enough_players(game):
            if is_current_player(game, json_request):
                return '{ "response": 200, "player_turn": true }'
            else:
                return '{ "response": 200, "player_turn": false }'
        else:
            return '{ "response": 200, "message": "Waiting for players" }'
    return '{ "response": 200, "message": "No game has been started" }'
