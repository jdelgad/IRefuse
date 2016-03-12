from game.irefuse import Game


def handle_request(json_request):
    if json_request["action"] == "START":
        def number_of_players():
            return json_request["players"]

        game = Game()
        try:
            game.setup(number_of_players)
        except AssertionError:
            return '{ "response": 400 }'
        return game
    else:
        return '{ "response": 400 }'
