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

    def setup_cards(self):
        cards_one = main.setup_cards()
        cards_two = main.setup_cards()
        cards_one = set(cards_one)
        sorted_cards_one = sorted(cards_one)
        cards_two = set(cards_two)
        sorted_cards_two = sorted(cards_two)
        self.assertEquals(cards_one, sorted_cards_one)
        self.assertEquals(cards_two, sorted_cards_two)
        self.assertEquals(len(cards_one), 24)
        self.assertEquals(len(cards_two), 24)
        self.assertNotEquals(cards_one, cards_two)

if __name__ == '__main__':
    unittest.main()