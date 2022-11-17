from . import pages
from ._builtin import Bot
import random


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield pages.Introduction
        if self.round_number == 2:
            rand_c = random.randint(1,8)
            yield pages.Contribute, dict(contribution=rand_c)
            yield pages.Results