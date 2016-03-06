import main
import unittest


class TestIRefuse(unittest.TestCase):
    def test_two_players(self):
        def input_func():
            return 2
        try:
            main.setup_players(input_func)
            self.fail("2 players are not allowed")
        except AssertionError:
            pass

    def test_three_players(self):
        def input_func():
            return 3
        try:
            num = main.setup_players(input_func)
            self.assertEquals(3, num)
        except AssertionError:
            self.fail("3 players are allowed")

    def test_five_players(self):
        def input_func():
            return 5
        try:
            num = main.setup_players(input_func)
            self.assertEquals(5, num)
        except AssertionError:
            self.fail("5 players are allowed")

    def test_six_players(self):
        def input_func():
            return 6
        try:
            main.setup_players(input_func)
            self.fail("2 players are not allowed")
        except AssertionError:
            pass


if __name__ == '__main__':
    unittest.main()