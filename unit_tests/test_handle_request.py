import os
import unittest
import json

import shutil

from game.handle_request import handle_request


def get_input(file):
    return "requests/input/{}.json".format(file)


def get_output(file):
    return "requests/output/{}.json".format(file)


def get_expected(file):
    return "requests/expected/{}.json".format(file)


class TestHandleRequest(unittest.TestCase):
    def test_handle_start_game(self):
        try:
            os.remove("current_game.json")
        except FileNotFoundError:
            pass

        with open(get_input("start_game")) as data_file:
            data = json.load(data_file)
            game = handle_request(data)

            # cards must be zeroed out since they are randomized
            output_json = json.loads(game)
            output_json["cards"] = []

            with open(get_expected("start_game")) as expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)

    def test_handle_join_game_passes(self):
        try:
            os.remove("current_game.json")
        except FileNotFoundError:
            pass
        shutil.copy(get_expected("start_game"), "current_game.json")
        with open(get_input("join_game")) as data_file:
            data = json.load(data_file)
            game = handle_request(data)

            # cards must be zeroed out since they are randomized
            output_json = json.loads(game)
            output_json["cards"] = []

            with open(get_expected("join_game")) as expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)

    def test_handle_join_game_with_none_in_progress(self):
        try:
            os.remove("current_game.json")
        except FileNotFoundError:
            pass

        with open(get_input("join_game_no_game_in_progress")) as data_file:
            data = json.load(data_file)
            game = handle_request(data)
            output_json = json.loads(game)

            with open(get_expected("join_game_no_game_in_progress")) as expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)
