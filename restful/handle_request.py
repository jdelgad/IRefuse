"""
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
from abc import ABCMeta, abstractmethod

from persistence.data import GameJournal

GAME_HAS_NOT_BEEN_STARTED = '{ "response": 200, ' \
                            '"message": "No game has been started" }'
WAITING_FOR_PLAYERS = '{ "response": 200, "message": "Waiting for players" }'
NOT_PLAYERS_TURN = '{ "response": 200, "player_turn": false }'
PLAYERS_TURN = '{ "response": 200, "player_turn": true }'
GAME_IS_CURRENTLY_IN_PROGRESS = '{ "response": 400, ' \
                                '"message": "Game is currently in progress" }'
GAME_IS_ALREADY_FULL_ = '{ "response": 400, ' \
                        '"message": "Game is already full" }'
PLAYER_IS_ALREADY_IN_GAME = '{ "response": 200, ' \
                            '"message": "You are already in game" }'
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
        self.game = GameJournal()

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
        self.game.add_player_to_game(json_request)
        return current_game

    def setup_game(self, json_request):
        self.game.start(json_request)
        return self.game.get_game_in_progress()


class JoinRequestHandler(RequestHandler):
    def handle(self, json_request):
        if self.game.is_started():
            self.game.read()
            return self.handle_join_after_start(json_request)
        else:
            return NO_GAME_IN_PROGRESS

    def handle_join_after_start(self, json_request):
        if self.game.is_player_in_game(json_request):
            return PLAYER_IS_ALREADY_IN_GAME
        elif self.game.has_enough_players():
            return GAME_IS_ALREADY_FULL_
        else:
            self.game.add_player_to_game(json_request)
            return self.game.get_game_in_progress()


class StatusRequestHandler(RequestHandler):
    def handle(self, json_request):
        if self.game.is_started():
            self.game.read()
            if self.game.has_enough_players():
                if self.game.is_current_player(json_request):
                    return PLAYERS_TURN
                else:
                    return NOT_PLAYERS_TURN
            else:
                return WAITING_FOR_PLAYERS
        return GAME_HAS_NOT_BEEN_STARTED
