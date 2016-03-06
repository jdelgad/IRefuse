import game.setup
import main
import game.player
import unittest


class TestIRefuse(unittest.TestCase):

    def test_prompt_for_action_passes(self):
        inputs = [0, 1]

        def input_func():
            return inputs.pop(0)
        player = game.player.Player()
        self.assertEquals(player.tokens, 11)
        user_took_card = main.prompt_for_action(3, 2, input_func, player)
        self.assertFalse(user_took_card)
        self.assertListEqual(inputs, [])
        self.assertEquals(player.tokens, 10)

    def test_prompt_for_action_takes_card(self):
        inputs = [0, 2]

        def input_func():
            return inputs.pop(0)
        player = game.player.Player()
        self.assertEquals(player.tokens, 11)
        user_took_card = main.prompt_for_action(3, 2, input_func, player)
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
        user_took_card = main.prompt_for_action(3, 5, input_func, player)
        self.assertTrue(user_took_card)
        self.assertListEqual(player.cards, [3])
        self.assertEquals(player.tokens, 5)

    def test_flip_card(self):
        cards = game.setup.setup_cards()
        number_of_cards = len(cards)
        self.assertEquals(24, number_of_cards)
        top_of_deck = cards[23]
        card = main.flip_card(cards)
        self.assertEquals(top_of_deck, card)
        self.assertEquals(23, len(cards))

    def test_flip_entire_deck(self):
        cards = game.setup.setup_cards()
        self.assertEquals(24, len(cards))
        for i in range(24):
            main.flip_card(cards)

    def test_flip_no_more_cards(self):
        cards = game.setup.setup_cards()
        self.assertEquals(24, len(cards))
        for i in range(24):
            main.flip_card(cards)

        self.assertEquals(0, len(cards))
        try:
            main.flip_card(cards)
            self.fail("cannot flip empty card deck")
        except IndexError:
            pass

    def test_determine_winner(self):
        players = [game.player.Player(), game.player.Player(), game.player.Player()]
        players[0].tokens = 2
        players[0].cards = [3, 5]

        players[1].tokens = 4
        players[1].cards = [6, 7]

        players[2].tokens = 3
        players[2].cards = []

        winners = main.determine_winner(players)
        self.assertEquals(len(winners), 1)
        self.assertEquals(winners[0], players[2])
        self.assertEquals(winners[0].calculate_points(), -3)

    def test_determine_winner_tie(self):
        players = [game.player.Player(), game.player.Player(), game.player.Player()]
        players[0].tokens = 2
        players[0].cards = [3, 12]

        players[1].tokens = 2
        players[1].cards = [5, 14]

        players[2].tokens = 0
        players[2].cards = [13]

        expected_winners = [players[0], players[2]]
        winners = main.determine_winner(players)
        self.assertEquals(len(winners), 2)
        self.assertListEqual(expected_winners, winners)

    def test_get_next_player(self):
        players = [game.player.Player(), game.player.Player(), game.player.Player()]
        player = players[0]
        player = main.get_next_player(player, players)
        self.assertEquals(players[1], player)

        player = main.get_next_player(player, players)
        self.assertEquals(players[2], player)

        player = main.get_next_player(player, players)
        self.assertEquals(players[0], player)

    def test_play_game(self):
        inputs = [1, 2, 1, 1]

        def input_func():
            return inputs.pop(0)

        cards = [3, 5]
        players = [game.player.Player(), game.player.Player()]
        players[0].tokens = 2
        self.assertListEqual(players[0].cards, [])
        players[1].tokens = 1
        self.assertListEqual(players[0].cards, [])

        winner = main.play_game(players, cards, input_func)
        self.assertEquals(1, len(winner))
        self.assertEquals(players[0].calculate_points(), 1)
        self.assertEquals(players[1].calculate_points(), 4)


if __name__ == '__main__':
    unittest.main()
