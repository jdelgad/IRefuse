import random


def setup_cards():
    """
    :return: A list of randomized 24 cards ranging from 3-35.
    """
    return random.sample(range(3, 36), 24)