import unittest
import json

from game.handle_request import handle_request


class TestHandleRequest(unittest.TestCase):
    def test_handle_start_game(self):
        with open("start_game.json") as data_file:
            data = json.load(data_file)
            print(data)
            game = handle_request(data)
            self.assertEquals(len(game.players), 4)

    def test_handle_start_game_fails(self):
        with open("start_game_invalid_players.json") as data_file:
            data = json.load(data_file)
            game = handle_request(data)
            self.assertEquals('{ "response": 400 }', game)
