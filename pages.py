from ._builtin import Page, WaitPage
from .models import Constants

class Introduction(Page):
    """Description of the game: How to play and returns expected"""

    def is_displayed(self):
        return self.round_number == 1


class Contribute(Page):
    """Player: Choose how much to contribute"""

    form_model = 'player'
    form_fields = ['contribution']

    def vars_for_template(self):
        return dict(show=min(self.round_number, Constants.players_per_group - 1))


class ResultsWaitPage(WaitPage):

    after_all_players_arrive = 'set_payoffs'
    body_text = "Waiting for other participants to choose their allocations."


class Results(Page):
    """Players payoff: How much each has earned"""
    def vars_for_template(self):
        last_round = (self.round_number == Constants.num_rounds + 1)
        player_id = self.player.id_in_group
        cont_hist = []
        for p in self.group.get_players():
            ind_hist = [q.contribution for q in p.in_all_rounds()] + ['' for x in range(15 - self.round_number)]
            cont_hist.append(ind_hist)
        question_marks = ['?' for x in range(self.round_number)] + ['' for x in range(15 - self.round_number)]
        if Constants.treatment:
            if self.round_number < 4:
                for p in self.group.get_players():
                    if (player_id-1) // 2 != (p.id_in_group-1) // 2:
                        cont_hist[(p.id_in_group-1)] = question_marks
            elif self.round_number < 7:
                for p in self.group.get_players():
                    if (player_id-1) // 4 != (p.id_in_group-1) // 4:
                        cont_hist[(p.id_in_group-1)] = question_marks

        table_rows = {0: ['Round Number:','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']}
        counter = 1
        for p in cont_hist:
            if counter == player_id:
                table_rows[counter] = ["<b>Your allocations</b>"] + p
            else:
                table_rows[counter] = ["Player " + str(counter) + "'s allocations"] + p
            counter += 1
        cumulative_payoff = sum([r.payoff for r in self.player.in_all_rounds()])
        avg_payoff = cumulative_payoff / self.round_number
        dollar_payoff = cumulative_payoff // 100
        group11 = [1, 2]
        group12 = [3, 4]
        group13 = [5, 6]
        group14 = [7, 8]
        return dict(t=table_rows, l=last_round, p=avg_payoff, m=dollar_payoff, i=player_id,
                    g11=group11, g12=group12, g13=group13, g14=group14, n=Constants.num_rounds)

page_sequence = [Introduction, Contribute, ResultsWaitPage, Results]