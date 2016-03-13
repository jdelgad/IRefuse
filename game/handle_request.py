import json

from game.irefuse import Game


def handle_request(json_request):
    if json_request["action"] == "START":
        current_game = setup_game(json_request)
        with open("current_game.json", "w") as current:
            current.write(current_game)
        return current_game
    elif json_request["action"] == "JOIN":
        return join_game(json_request)
    else:
        return '{ "response": 400 }'


def setup_game(json_request):
    def number_of_players():
        return json_request["players"]

    game = Game()
    game.setup(number_of_players)
    return json.dumps(game, default=lambda o: o.__dict__)


def join_game(json_request):
    try:
        with open("current_game.json", "r") as current_game:
            return current_game.readlines()[-1]
    except FileNotFoundError:
        return '{ "response": 400, "message": "No game in progress" }'
