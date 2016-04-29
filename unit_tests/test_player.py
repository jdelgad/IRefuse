"""
Module is responsible for testing of players module in 'I Refuse.'
Copyright (c) 2016 Jacob Delgado,
This file is part of I Refuse.

'I Refuse' is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import irefuse.irefuse
import irefuse.player
import unittest


class TestPlayers(unittest.TestCase):
    def test_get_next_player(self):
        players = irefuse.player.Players(3)
        player = players.next_player()
        self.assertEquals(players.players[0], player)

        player = players.next_player(player)
        self.assertEquals(players.players[1], player)

        player = players.next_player(player)
        self.assertEquals(players.players[2], player)

        player = players.next_player(player)
        self.assertEquals(players.players[0], player)

    def test_get_index(self):
        players = irefuse.player.Players(2)
        players.players[0].tokens = 3
        players.players[0].cards = [1]
        self.assertEquals(players[0].tokens, 3)
        self.assertListEqual(players[0].cards, [1])

        players.players[1].tokens = 5
        players.players[1].cards = [3, 9]
        self.assertEquals(players[1].tokens, 5)
        self.assertListEqual(players[1].cards, [3, 9])

    def test_iterator(self):
        players = irefuse.player.Players(3)
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
        player = irefuse.player.Player(1)
        self.assertEquals(player.tokens, 11)

    def test_passes(self):
        player = irefuse.player.Player(2)
        player.passes()
        self.assertEquals(player.tokens, 10)

    def test_player_cannot_pass(self):
        player = irefuse.player.Player(3)
        player.tokens = 0
        try:
            player.passes()
            self.fail()
        except AssertionError:
            pass

    def test_calculate_points_no_sequence(self):
        player = irefuse.player.Player(4)
        player.tokens = 2
        player.cards = [5, 7, 9]
        points = player.calculate_points()
        self.assertEquals(points, 19)

    def test_calculate_points_with_sequence(self):
        player = irefuse.player.Player(5)
        player.tokens = 1
        player.cards = [24, 7, 6, 5]
        points = player.calculate_points()
        self.assertEquals(points, 28)

    def test_print_string(self):
        player = irefuse.player.Player(5)
        player_str = player.__str__()
        self.assertEquals("Player 5", player_str)
