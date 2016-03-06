class Player(object):
    def __init__(self):
        self.tokens = 11

    def passes(self):
        if self.__can_pass():
            self.tokens -= 1
            return True
        else:
            return False

    def __can_pass(self):
        return self.tokens != 0
