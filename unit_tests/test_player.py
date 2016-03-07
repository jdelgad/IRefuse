"""
Module is responsible for testing of players module in 'I Refuse.'

 Author: Jacob Delgado
 Date: Mar 6, 2016
"""
import game.irefuse
import game.player
import unittest


class TestPlayers(unittest.TestCase):
    def test_get_next_player(self):
        players = game.player.Players(3)
        player = players.next_player()
        self.assertEquals(players.players[0], player)

        player = players.next_player(player)
        self.assertEquals(players.players[1], player)

        player = players.next_player(player)
        self.assertEquals(players.players[2], player)

        player = players.next_player(player)
        self.assertEquals(players.players[0], player)

    def test_get_index(self):
        players = game.player.Players(2)
        players.players[0].tokens = 3
        players.players[0].cards = [1]
        self.assertEquals(players[0].tokens, 3)
        self.assertListEqual(players[0].cards, [1])

        players.players[1].tokens = 5
        players.players[1].cards = [3, 9]
        self.assertEquals(players[1].tokens, 5)
        self.assertListEqual(players[1].cards, [3, 9])

    def test_iterator(self):
        players = game.player.Players(3)
        count = 0
        for _ in players:
            count += 1
        self.assertEquals(3, count)

        count = 0
        for _ in players:
            count += 1
        self.assertEquals(3, count)


class TestPlayer(unittest.TestCase):
    def test_default_player(self):
        player = game.player.Player(1)
        self.assertEquals(player.tokens, 11)

    def test_passes(self):
        player = game.player.Player(2)
        self.assertTrue(player.passes())
        self.assertEquals(player.tokens, 10)

    def player_cannot_pass(self):
        player = game.player.Player(3)
        player.tokens = 0
        self.assertFalse(player.passes())

    def test_calculate_points_no_sequence(self):
        player = game.player.Player(4)
        player.tokens = 2
        player.cards = [5, 7, 9]
        points = player.calculate_points()
        self.assertEquals(points, 19)

    def test_calculate_points_with_sequence(self):
        player = game.player.Player(5)
        player.tokens = 1
        player.cards = [24, 7, 6, 5]
        points = player.calculate_points()
        self.assertEquals(points, 28)

    def test_print_string(self):
        player = game.player.Player(5)
        player_str = player.__str__()
        self.assertEquals("Player 5", player_str)

    def test_print_stats(self):
        player = game.player.Player(5)
        player.tokens = 1
        player.cards = [24, 7, 6, 5]
        stats = player.stats()
        self.assertEquals("Player 5: cards = [5, 6, 7, 24]; tokens = 1; "
                          "points = 28", stats)
