"""
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
import unittest

from persistence.data import GameJournal
from unit_tests.utfiles import remove_current_game, remove_players_list


class TestGameJournal(unittest.TestCase):
    def setUp(self):
        remove_current_game()
        remove_players_list()

    def test_initialize_record(self):
        game = GameJournal()
        game.initialize(3)


