"""
Module is responsible for testing of game/business logic behind 'I Refuse.'

 Author: Jacob Delgado
 Date: Mar 6, 2016
"""
import game.irefuse
import game.player
import unittest


class TestIRefuse(unittest.TestCase):
    def test_two_players(self):
        def input_func():
            return 2
        try:
            game.irefuse.Game.setup_players(input_func)
            self.fail("2 players are not allowed")
        except AssertionError:
            pass

    def test_three_players(self):
        def input_func():
            return 3
        try:
            players = game.irefuse.Game.setup_players(input_func)
            self.assertEquals(3, len(players.players))
        except AssertionError:
            self.fail("3 players are allowed")

    def test_five_players(self):
        def input_func():
            return 5
        try:
            players = game.irefuse.Game.setup_players(input_func)
            self.assertEquals(5, len(players.players))
        except AssertionError:
            self.fail("5 players are allowed")

    def test_six_players(self):
        def input_func():
            return 6
        try:
            game.irefuse.Game.setup_players(input_func)
            self.fail("6 players are not allowed")
        except AssertionError:
            pass

    def test_setup_cards(self):
        cards_one = game.irefuse.Game.setup_cards()
        cards_two = game.irefuse.Game.setup_cards()
        cards_one = set(cards_one)
        sorted_cards_one = list(sorted(cards_one))
        cards_two = set(cards_two)
        sorted_cards_two = list(sorted(cards_two))
        self.assertNotEquals(cards_one, sorted_cards_one)
        self.assertNotEquals(cards_two, sorted_cards_two)
        self.assertEquals(len(cards_one), 24)
        self.assertEquals(len(cards_two), 24)
        self.assertNotEquals(cards_one, cards_two)

    def test_prompt_for_action_passes(self):
        inputs = [0, 1]

        def input_func():
            return inputs.pop(0)
        player = game.player.Player()
        self.assertEquals(player.tokens, 11)
        user_took_card = game.irefuse.prompt_for_action(3, 2, input_func, player)
        self.assertFalse(user_took_card)
        self.assertListEqual(inputs, [])
        self.assertEquals(player.tokens, 10)

    def test_prompt_for_action_takes_card(self):
        inputs = [0, 2]

        def input_func():
            return inputs.pop(0)
        player = game.player.Player()
        self.assertEquals(player.tokens, 11)
        user_took_card = game.irefuse.prompt_for_action(3, 2, input_func, player)
        self.assertTrue(user_took_card)
        self.assertListEqual(inputs, [])
        self.assertEquals(player.tokens, 13)

    def test_player_no_action(self):
        def input_func():
            return 0
        player = game.player.Player()
        player.tokens = 0
        self.assertListEqual(player.cards, [])
        self.assertEquals(player.tokens, 0)
        user_took_card = game.irefuse.prompt_for_action(3, 5, input_func, player)
        self.assertTrue(user_took_card)
        self.assertListEqual(player.cards, [3])
        self.assertEquals(player.tokens, 5)

    def test_flip_card(self):
        cards = game.irefuse.Game.setup_cards()
        number_of_cards = len(cards)
        self.assertEquals(24, number_of_cards)
        top_of_deck = cards[23]
        card = game.irefuse.flip_card(cards)
        self.assertEquals(top_of_deck, card)
        self.assertEquals(23, len(cards))

    def test_flip_entire_deck(self):
        cards = game.irefuse.Game.setup_cards()
        self.assertEquals(24, len(cards))
        for i in range(24):
            game.irefuse.flip_card(cards)

    def test_flip_no_more_cards(self):
        cards = game.irefuse.Game.setup_cards()
        self.assertEquals(24, len(cards))
        for i in range(24):
            game.irefuse.flip_card(cards)

        self.assertEquals(0, len(cards))
        try:
            game.irefuse.flip_card(cards)
            self.fail("cannot flip empty card deck")
        except IndexError:
            pass

    def test_play_game(self):
        inputs = [1, 2, 1, 1, 1, 2]

        def input_func():
            return inputs.pop(0)

        def three_players():
            return 3

        game_irefuse = game.irefuse.Game()
        game_irefuse.setup(three_players)
        game_irefuse.cards = [3, 5]

        game_irefuse.players[0].tokens = 2
        self.assertListEqual(game_irefuse.players[0].cards, [])
        game_irefuse.players[1].tokens = 1
        self.assertListEqual(game_irefuse.players[1].cards, [])
        game_irefuse.players[2].tokens = 3
        self.assertListEqual(game_irefuse.players[2].cards, [])

        winner = game_irefuse.play(input_func)
        self.assertEquals(1, len(winner))
        self.assertEquals(winner[0], game_irefuse.players[2])

        self.assertListEqual(game_irefuse.players[0].cards, [])
        self.assertEquals(game_irefuse.players[0].tokens, 0)
        self.assertEquals(game_irefuse.players[0].calculate_points(), 0)

        self.assertListEqual(game_irefuse.players[1].cards, [5, 3])
        self.assertEquals(game_irefuse.players[1].tokens, 4)
        self.assertEquals(game_irefuse.players[1].calculate_points(), 4)

        self.assertListEqual(game_irefuse.players[2].cards, [])
        self.assertEquals(game_irefuse.players[2].tokens, 2)
        self.assertEquals(game_irefuse.players[2].calculate_points(), -2)

    def test_play_game_ends_in_tie(self):
        inputs = [1, 1, 2, 2, 1, 1]

        def input_func():
            return inputs.pop(0)

        def four_players():
            return 4

        game_irefuse = game.irefuse.Game()
        game_irefuse.setup(four_players)
        game_irefuse.cards = [3, 5, 6, 7]

        game_irefuse.players[0].tokens = 1
        game_irefuse.players[0].cards = [14]
        self.assertListEqual(game_irefuse.players[0].cards, [14])
        game_irefuse.players[1].tokens = 1
        game_irefuse.players[1].cards = [30]
        self.assertListEqual(game_irefuse.players[1].cards, [30])
        game_irefuse.players[2].tokens = 0
        game_irefuse.players[2].cards = [24]
        self.assertListEqual(game_irefuse.players[2].cards, [24])
        game_irefuse.players[3].tokens = 2
        game_irefuse.players[3].cards = [16]
        self.assertListEqual(game_irefuse.players[3].cards, [16])

        winner = game_irefuse.play(input_func)
        self.assertEquals(2, len(winner))
        self.assertEquals(winner[0], game_irefuse.players[0])
        self.assertEquals(winner[1], game_irefuse.players[3])

        self.assertListEqual(game_irefuse.players[0].cards, [14, 3])
        self.assertEquals(game_irefuse.players[0].tokens, 2)
        self.assertEquals(game_irefuse.players[0].calculate_points(), 15)

        self.assertListEqual(game_irefuse.players[1].cards, [30])
        self.assertEquals(game_irefuse.players[1].tokens, 0)
        self.assertEquals(game_irefuse.players[1].calculate_points(), 30)

        self.assertListEqual(game_irefuse.players[2].cards, [24, 7, 6, 5])
        self.assertEquals(game_irefuse.players[2].tokens, 1)
        self.assertEquals(game_irefuse.players[2].calculate_points(), 28)

        self.assertListEqual(game_irefuse.players[3].cards, [16])
        self.assertEquals(game_irefuse.players[3].tokens, 1)
        self.assertEquals(game_irefuse.players[3].calculate_points(), 15)

    def test_determine_winner(self):

        def three_players():
            return 3

        game_irefuse = game.irefuse.Game()
        game_irefuse.setup(three_players)

        game_irefuse.players[0].tokens = 2
        game_irefuse.players[0].cards = [3, 5]

        game_irefuse.players[1].tokens = 4
        game_irefuse.players[1].cards = [6, 7]

        game_irefuse.players[2].tokens = 3
        game_irefuse.players[2].cards = []

        winners = game_irefuse.determine_winner()
        self.assertEquals(len(winners), 1)
        self.assertEquals(winners[0], game_irefuse.players[2])
        self.assertEquals(winners[0].calculate_points(), -3)

    def test_determine_winner_tie(self):
        def three_players():
            return 3

        game_irefuse = game.irefuse.Game()
        game_irefuse.setup(three_players)

        game_irefuse.players[0].tokens = 2
        game_irefuse.players[0].cards = [3, 12]

        game_irefuse.players[1].tokens = 2
        game_irefuse.players[1].cards = [5, 14]

        game_irefuse.players[2].tokens = 0
        game_irefuse.players[2].cards = [13]

        expected_winners = [game_irefuse.players[0], game_irefuse.players[2]]
        winners = game_irefuse.determine_winner()
        self.assertEquals(len(winners), 2)
        self.assertListEqual(expected_winners, winners)


if __name__ == '__main__':
    unittest.main()
