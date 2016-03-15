from abc import ABCMeta, abstractmethod

from irefuse.irefuse import IRefuse
from persistence.game import Game, initialize_players, add_player_to_game, \
    is_current_player, has_enough_players, is_player_in_game

GAME_HAS_NOT_BEEN_STARTED = '{ "response": 200, "message": "No game has been started" }'

WAITING_FOR_PLAYERS = '{ "response": 200, "message": "Waiting for players" }'

NOT_PLAYERS_TURN = '{ "response": 200, "player_turn": false }'

PLAYERS_TURN = '{ "response": 200, "player_turn": true }'

GAME_IS_CURRENTLY_IN_PROGRESS = '{ "response": 400, "message": "Game is currently in progress" }'
GAME_IS_ALREADY_FULL_ = '{ "response": 400, "message": "Game is already full" }'
PLAYER_IS_ALREADY_IN_GAME = '{ "response": 200, "message": "You are already in game" }'
NO_GAME_IN_PROGRESS = '{ "response": 400, "message": "No game in progress" }'


def get_request_handler(json_request):
    if json_request["action"] == "START":
        return StartRequestHandler()
    elif json_request["action"] == "JOIN":
        return JoinRequestHandler()
    elif json_request["action"] == "STATUS":
        return StatusRequestHandler()


class RequestHandler(metaclass=ABCMeta):
    def __init__(self):
        self.game = Game()

    @abstractmethod
    def handle(self, json_request):
        pass


class StartRequestHandler(RequestHandler):
    def handle(self, json_request):
        if self.game.is_started():
            return GAME_IS_CURRENTLY_IN_PROGRESS

        return self.start_game(json_request)

    def start_game(self, json_request):
        current_game = self.setup_game(json_request)
        self.game.record_game(current_game)

        add_player_to_game(json_request)

        return current_game

    def setup_game(self, json_request):
        def number_of_players():
            return json_request["players"]

        initialize_players(json_request, number_of_players)

        irefuse = IRefuse()
        irefuse.setup(number_of_players)
        game = Game()
        return game.serialize_game(irefuse)


class JoinRequestHandler(RequestHandler):
    def handle(self, json_request):
        if self.game.is_started():
            return self.handle_join_after_start(json_request)
        else:
            return NO_GAME_IN_PROGRESS

    def handle_join_after_start(self, json_request):
        if is_player_in_game(json_request):
            return PLAYER_IS_ALREADY_IN_GAME
        elif has_enough_players():
            return GAME_IS_ALREADY_FULL_
        else:
            add_player_to_game(json_request)
            return self.game.get_game_in_progress()


class StatusRequestHandler(RequestHandler):
    def handle(self, json_request):
        if self.game.is_started():
            game = self.game.get_game_in_progress()

            if has_enough_players():
                if is_current_player(game, json_request):
                    return PLAYERS_TURN
                else:
                    return NOT_PLAYERS_TURN
            else:
                return WAITING_FOR_PLAYERS
        return GAME_HAS_NOT_BEEN_STARTED
