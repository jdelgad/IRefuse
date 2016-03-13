import filecmp
import unittest
import json

from game.handle_request import handle_request


class TestHandleRequest(unittest.TestCase):
    def test_handle_start_game(self):
        with open("start_game.json") as data_file:
            data = json.load(data_file)
            game = handle_request(data)

            with open("start_game.json.output", "w") as output_file:
                output_file.write(game)
        self.assertTrue(filecmp.cmp("start_game.json.expected",
                                    "start_game.json.output"))

    def test_handle_start_game_fails(self):
        with open("start_game_invalid_players.json") as data_file:
            data = json.load(data_file)
            game = handle_request(data)
            self.assertEquals('{ "response": 400 }', game)
