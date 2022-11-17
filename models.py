from otree.api import models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, currency_range
import numpy as np

class Constants(BaseConstants):
    name_in_url = 'public_goods_klevans'
    players_per_group = 8
    endowment = 5 * (players_per_group - 1) * players_per_group #set to ensure no bankruptcy
    num_rounds = min(15, np.random.geometric(p=0.1))
    multiplier = 1
    instructions_template = 'klevans_public_goods/instructions.html'
    treatment = True

    def payoff_x(y):
        return Constants.endowment - 5 * (y ** 2 - y)


class Subsession(BaseSubsession):
    pass


class Label():
    max_contribution = Constants.players_per_group


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def set_payoffs(self):
        players = self.get_players()
        contributions = [p.contribution for p in players]
        self.total_contribution = sum(contributions)
        self.individual_share = self.total_contribution * Constants.multiplier / Constants.players_per_group
        for p in players:
            p.payoff = Constants.endowment - 10 * (p.contribution**2 - p.contribution)/2 + 10 * self.total_contribution


class Player(BasePlayer):
    contribution = models.IntegerField(min=0, max=Constants.players_per_group,
                                       label="How much do you want to contribute?")

    def contribution_error_message(player, value):
        if value == 0:
            return 'Must contribute at least 1 unit'