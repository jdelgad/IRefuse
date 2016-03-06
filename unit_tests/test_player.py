import game.player
import unittest


class TestPlayers(unittest.TestCase):
    def test_two_players(self):
        def input_func():
            return 2
        try:
            game.player.setup_players(input_func)
            self.fail("2 players are not allowed")
        except AssertionError:
            pass

    def test_three_players(self):
        def input_func():
            return 3
        try:
            players = game.player.setup_players(input_func)
            self.assertEquals(3, len(players.players))
        except AssertionError:
            self.fail("3 players are allowed")

    def test_five_players(self):
        def input_func():
            return 5
        try:
            players = game.player.setup_players(input_func)
            self.assertEquals(5, len(players.players))
        except AssertionError:
            self.fail("5 players are allowed")

    def test_six_players(self):
        def input_func():
            return 6
        try:
            game.player.setup_players(input_func)
            self.fail("6 players are not allowed")
        except AssertionError:
            pass

    def test_get_next_player(self):
        players = game.player.Players(3)
        player = players.next()
        self.assertEquals(players.players[0], player)

        player = players.next(player)
        self.assertEquals(players.players[1], player)

        player = players.next(player)
        self.assertEquals(players.players[2], player)

        player = players.next(player)
        self.assertEquals(players.players[0], player)

    def test_determine_winner(self):
        players = game.player.Players(3)
        players.players[0].tokens = 2
        players.players[0].cards = [3, 5]

        players.players[1].tokens = 4
        players.players[1].cards = [6, 7]

        players.players[2].tokens = 3
        players.players[2].cards = []

        winners = players.determine_winner()
        self.assertEquals(len(winners), 1)
        self.assertEquals(winners[0], players.players[2])
        self.assertEquals(winners[0].calculate_points(), -3)

    def test_determine_winner_tie(self):
        players = game.player.Players(3)
        players.players[0].tokens = 2
        players.players[0].cards = [3, 12]

        players.players[1].tokens = 2
        players.players[1].cards = [5, 14]

        players.players[2].tokens = 0
        players.players[2].cards = [13]

        expected_winners = [players.players[0], players.players[2]]
        winners = players.determine_winner()
        self.assertEquals(len(winners), 2)
        self.assertListEqual(expected_winners, winners)


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
