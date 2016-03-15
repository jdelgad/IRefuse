import json
import os
import shutil
import unittest

from restful.handle_request import handle_request


def get_input(file):
    return "requests/input/{}.json".format(file)


def get_output(file):
    return "requests/output/{}.json".format(file)


def get_expected(file):
    return "requests/expected/{}.json".format(file)


def remove_players_list():
    try:
        os.remove("players.json")
    except FileNotFoundError:
        pass


def remove_current_game():
    try:
        os.remove("current_game.json")
    except FileNotFoundError:
        pass


class TestHandleRequest(unittest.TestCase):
    def setUp(self):
        remove_current_game()
        remove_players_list()

    def test_handle_start_game(self):
        with open(get_input("start_game")) as data_file:
            data = json.load(data_file)
            game = handle_request(data)

            # cards must be zeroed out since they are randomized
            output_json = json.loads(game)
            output_json["cards"] = []

            with open(get_expected("start_game")) as expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)

    def test_handle_start_game_but_game_in_progress(self):
        shutil.copy(get_expected("start_game"), "current_game.json")
        with open(get_input("start_game")) as data_file:
            data = json.load(data_file)
            game = handle_request(data)

            output_json = json.loads(game)

            with open(get_expected("start_game_but_game_in_progress")) as \
                    expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)

    def test_handle_join_game_passes(self):
        shutil.copy(get_expected("players"), "players.json")
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
        with open(get_input("join_game_no_game_in_progress")) as data_file:
            data = json.load(data_file)
            game = handle_request(data)
            output_json = json.loads(game)

            with open(get_expected("join_game_no_game_in_progress")) as \
                    expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)

    def test_handle_status_waiting_for_players(self):
        shutil.copy(get_expected("players"), "players.json")
        shutil.copy(get_expected("start_game"), "current_game.json")
        with open(get_input("status")) as data_file:
            data = json.load(data_file)
            game = handle_request(data)
            output_json = json.loads(game)

            with open(get_expected("status_waiting_to_start")) as expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)

    def test_handle_status_no_game_in_progress(self):
        with open(get_input("status")) as data_file:
            data = json.load(data_file)
            game = handle_request(data)
            output_json = json.loads(game)

            with open(get_expected("status_no_game_started")) as expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)

    def test_handle_status_players_turn(self):
        shutil.copy(get_expected("all_players_turn"), "players.json")
        shutil.copy(get_expected("start_game"), "current_game.json")
        with open(get_input("status")) as data_file:
            data = json.load(data_file)
            game = handle_request(data)
            output_json = json.loads(game)

            with open(get_expected("status_players_turn")) as expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)

    def test_handle_status_not_players_turn(self):
        shutil.copy(get_expected("all_players_no_turn"), "players.json")
        shutil.copy(get_expected("start_game"), "current_game.json")
        with open(get_input("status")) as data_file:
            data = json.load(data_file)
            game = handle_request(data)
            output_json = json.loads(game)

            with open(get_expected("status_players_no_turn")) as expected:
                expected_json = json.load(expected)
            self.assertEquals(output_json, expected_json)
