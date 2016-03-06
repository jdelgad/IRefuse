import main
import game.player
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
            players = main.setup_players(input_func)
            self.assertEquals(3, len(players))
        except AssertionError:
            self.fail("3 players are allowed")

    def test_five_players(self):
        def input_func():
            return 5
        try:
            players = main.setup_players(input_func)
            self.assertEquals(5, len(players))
        except AssertionError:
            self.fail("5 players are allowed")

    def test_six_players(self):
        def input_func():
            return 6
        try:
            main.setup_players(input_func)
            self.fail("6 players are not allowed")
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

    def test_prompt_for_action_passes(self):
        inputs = [0, 1]

        def input_func():
            return inputs.pop(0)
        player = game.player.Player()
        self.assertEquals(player.tokens, 11)
        main.prompt_for_action(3, 2, input_func, player)
        self.assertListEqual(inputs, [])
        self.assertEquals(player.tokens, 10)

    def test_prompt_for_action_takes_card(self):
        inputs = [0, 2]

        def input_func():
            return inputs.pop(0)
        player = game.player.Player()
        self.assertEquals(player.tokens, 11)
        main.prompt_for_action(3, 2, input_func, player)
        self.assertListEqual(inputs, [])
        self.assertEquals(player.tokens, 13)

    def test_player_no_action(self):
        def input_func():
            return 1
        player = game.player.Player()
        player.tokens = 0
        self.assertListEqual(player.cards, [])
        self.assertEquals(player.tokens, 0)
        main.prompt_for_action(3, 5, input_func, player)
        self.assertListEqual(player.cards, [3])
        self.assertEquals(player.tokens, 5)

    def test_flip_card(self):
        cards = main.setup_cards()
        number_of_cards = len(cards)
        self.assertEquals(24, number_of_cards)
        top_of_deck = cards[23]
        card = main.flip_card(cards)
        self.assertEquals(top_of_deck, card)
        self.assertEquals(23, len(cards))

    def test_flip_entire_deck(self):
        cards = main.setup_cards()
        self.assertEquals(24, len(cards))
        for i in range(24):
            main.flip_card(cards)

    def test_flip_no_more_cards(self):
        cards = main.setup_cards()
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

    # def test_play_game(self):
    #     inputs = [1, 2, 1, 1]
    #
    #     def input_func():
    #         return inputs.pop(0)
    #
    #     cards = [3, 5]
    #     players = [game.player.Player(), game.player.Player()]
    #     players[0].tokens = 2
    #     self.assertListEqual(players[0].cards, [])
    #     players[1].tokens = 1
    #     self.assertListEqual(players[0].cards, [])
    #
    #     main.play_game(players, input_func)


if __name__ == '__main__':
    unittest.main()
