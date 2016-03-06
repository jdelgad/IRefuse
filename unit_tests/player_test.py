import game.player
import unittest


class TestPlayer(unittest.TestCase):
    def test_default_player(self):
        player = game.player.Player()
        self.assertEquals(player.tokens, 11)

    def test_passes(self):
        player = game.player.Player()
        self.assertTrue(player.passes())
        self.assertEquals(player.tokens, 10)

    def player_cannot_pass(self):
        player = game.player.Player()
        player.tokens = 0
        self.assertFalse(player.passes())

    def test_calculate_points_no_sequence(self):
        player = game.player.Player()
        player.tokens = 2
        player.cards = [5, 7, 9]
        points = player.calculate_points()
        self.assertEquals(points, 19)

    def test_calculate_points_with_sequence(self):
        player = game.player.Player()
        player.tokens = 4
        player.cards = [5, 6, 8, 9]
        points = player.calculate_points()
        self.assertEquals(points, 9)
