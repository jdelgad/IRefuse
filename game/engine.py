def play_game(players, cards, input_func):
    """
    Rules logic for I Refuse

    :param players:
    :param cards:
    :param input_func:
    :return:
    """
    max_flips = len(cards)
    player = players.next()
    for i in range(max_flips):
        card = flip_card(cards)
        tokens = 0
        while not prompt_for_action(card, tokens, input_func, player):
            tokens += 1
            player = players.next(player)
        player = players.next(player)

    return players.determine_winner()


def flip_card(cards):
    """
    Flips the top card on the deck

    :param cards:
    :return:
    """
    return cards.pop()


def prompt_for_action(card, tokens, input_func, player):
    """
    Prompts the user for action, returns true if the user takes a cards, false otherwise.

    :param card:
    :param tokens:
    :param input_func:
    :param player:
    :return: True if the user took the card, false if not.
    """
    if not player.can_pass():
        player.take_card(card, tokens)
        return True

    action = 0
    while not (action == 1 or action == 2):
        print("\nAvailable card: {}, Number of tokens: {}".format(card, tokens))
        print("What action do you wish to perform: ")
        print("1. Pass")
        print("2. Take card")
        action = int(input_func())

    if action == 1:
        player.passes()
        return False
    elif action == 2:
        player.take_card(card, tokens)
        return True




