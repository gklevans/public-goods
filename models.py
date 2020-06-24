from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


class Constants(BaseConstants):
    name_in_url = 'public_goods_klevans'
    players_per_group = 3
    num_rounds = 5

    endowment = players_per_group
    multiplier = 1
    inputs = [[x+1,'Contribute ' + str(x+1) + ' unit(s) at a total cost of $' + str((x+1)**2 / 2) +
               '. Increasing your contribution to ' + str(x+2) + ' units would cost an additional $' + str(1.5 + x)]
              for x in range(endowment)]
    inputs[-1][1] = ('Contribute ' + str(endowment) + ' unit(s) at a total cost of $' + str((endowment**2/2)) +
                     '.  This is the maximum contribution.')


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def set_payoffs(self):
        players = self.get_players()
        contributions = [p.contribution for p in players]
        self.total_contribution = sum(contributions)
        self.individual_share = (
            self.total_contribution * Constants.multiplier / Constants.players_per_group
        )
        for p in players:
            p.payoff = Constants.endowment - p.contribution**2/2 + self.total_contribution
            p.stop = p.round_number + int(p.id_in_group <= p.round_number)


class Player(BasePlayer):

    contribution = models.CurrencyField(min=0, max=Constants.endowment, widget=widgets.RadioSelect,
                                        choices=Constants.inputs)
    stop = models.IntegerField()