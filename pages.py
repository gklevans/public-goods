from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants

import random

class Introduction(Page):
    """Description of the game: How to play and returns expected"""

    pass


class Contribute(Page):
    """Player: Choose how much to contribute"""

    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'

    body_text = "Waiting for other participants to contribute."


class Results(Page):
    """Players payoff: How much each has earned"""




page_sequence = [Contribute, ResultsWaitPage, Results]
