import hashlib
import json
import os

from game.irefuse import Game

# json responses
GAME_IS_CURRENTLY_IN_PROGRESS = '{ "response": 400, "message": "Game is currently in progress" }'
GAME_IS_ALREADY_FULL_ = '{ "response": 400, "message": "Game is already full" }'
PLAYER_IS_ALREADY_IN_GAME = '{ "response": 200, "message": "You are already in game" }'
NO_GAME_IN_PROGRESS_ = '{ "response": 400, "message": "No game in progress" }'

# json files representing the current game
CURRENT_GAME_JSON = "current_game.json"
PLAYERS_JSON = "players.json"


def handle_request(json_request):
    if json_request["action"] == "START":
        return handle_start_request(json_request)
    elif json_request["action"] == "JOIN":
        return handle_join_request(json_request)
    elif json_request["action"] == "STATUS":
        return handle_status_request(json_request)


def handle_join_request(json_request):
    if game_has_been_started():
        return handle_join_after_start(json_request)
    else:
        return NO_GAME_IN_PROGRESS_


def handle_join_after_start(json_request):
    if is_player_in_game(json_request):
        return PLAYER_IS_ALREADY_IN_GAME
    elif has_enough_players():
        return GAME_IS_ALREADY_FULL_
    else:
        add_player_to_game(json_request)
        return get_game_in_progress()


def handle_start_request(json_request):
    if game_has_been_started():
        return GAME_IS_CURRENTLY_IN_PROGRESS

    return start_game(json_request)


def start_game(json_request):
    current_game = setup_game(json_request)
    create_game_record(current_game)

    add_player_to_game(json_request)

    return current_game


def create_game_record(current_game):
    with open(CURRENT_GAME_JSON, "w") as current:
        current.write(current_game)


def setup_game(json_request):
    def number_of_players():
        return json_request["players"]

    initialize_players(json_request, number_of_players)

    game = Game()
    game.setup(number_of_players)
    return serialize_game(game)


def serialize_game(game):
    return json.dumps(game, default=lambda o: o.__dict__)


def initialize_players(json_request, number_of_players):
    players = {}
    for i in range(number_of_players()):
        players[i] = None

    players[0] = get_player_hash(json_request)

    serialize_players(players)


def serialize_players(players):
    with open(PLAYERS_JSON, "w") as game:
        json.dump(players, game)


def add_player_to_game(json_request):
    players = deserialize_players()

    for player in players:
        if players[player] is None:
            players[player] = get_player_hash(json_request)


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


def get_player_hash(json_request):
    return hashlib.md5("{}{}".format(json_request["client_ip"], json_request[
        "client_port"]).encode("utf-8")).hexdigest()


def is_current_player(game, json_request):
    with open(PLAYERS_JSON) as current_players:
        players = json.loads(current_players.readlines()[0])

    return players[get_current_player(game)] == get_player_hash(
        json_request)


def get_current_player(game):
    return str(game["players"]["index"])


def has_enough_players():
    with open(PLAYERS_JSON) as current_players:
        players = json.loads(current_players.readlines()[0])

    for i in players:
        if players[i] is None:
            return False

    return True


def handle_status_request(json_request):
    if game_has_been_started():
        game = get_game_in_progress()

        if has_enough_players():
            if is_current_player(game, json_request):
                return '{ "response": 200, "player_turn": true }'
            else:
                return '{ "response": 200, "player_turn": false }'
        else:
            return '{ "response": 200, "message": "Waiting for players" }'
    return '{ "response": 200, "message": "No game has been started" }'


def is_player_in_game(json_request):
    with open(PLAYERS_JSON) as game:
        players = json.loads(game.readlines()[0])

    for i in players:
        if players[i] == get_player_hash(json_request):
            return True
    return False
