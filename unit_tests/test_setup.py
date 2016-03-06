import unittest

import game.player
import game.setup


class TestSetup(unittest.TestCase):
    def setup_cards(self):
        cards_one = game.setup.setup_cards()
        cards_two = game.setup.setup_cards()
        cards_one = set(cards_one)
        sorted_cards_one = sorted(cards_one)
        cards_two = set(cards_two)
        sorted_cards_two = sorted(cards_two)
        self.assertEquals(cards_one, sorted_cards_one)
        self.assertEquals(cards_two, sorted_cards_two)
        self.assertEquals(len(cards_one), 24)
        self.assertEquals(len(cards_two), 24)
        self.assertNotEquals(cards_one, cards_two)
