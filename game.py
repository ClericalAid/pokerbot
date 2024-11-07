from pokerkit import Automation, Mode, NoLimitTexasHoldem
import pdb
import typing
from poker import state_vector

big_blind = 100
small_blind = int(big_blind / 2)
min_bet = big_blind
starting_stack = 100 * big_blind
number_of_players = 6
antes = {} # empty should mean no antes

class Game:
    def __init__(self):
        self.state = NoLimitTexasHoldem.create_state(
            (
                Automation.ANTE_POSTING,
                Automation.BET_COLLECTION,
                Automation.BLIND_OR_STRADDLE_POSTING,
                Automation.BOARD_DEALING,
                Automation.CARD_BURNING,
                Automation.CHIPS_PULLING,
                Automation.CHIPS_PUSHING,
                Automation.HAND_KILLING,
                Automation.HOLE_DEALING,
                Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
            ),
            False,  # Uniform antes?
            antes,
            (small_blind, big_blind),  # Blinds, also includes straddles
            min_bet,
            (starting_stack, starting_stack, starting_stack, starting_stack, starting_stack, starting_stack),
            number_of_players,
            mode=Mode.CASH_GAME,
        )

        self.player_state_vectors : typing.Dict[int, state_vector.PlayerStateVector] = dict()
        for i in range(number_of_players):
            self.player_state_vectors[i] = state_vector.PlayerStateVector(i)
            self.player_state_vectors[i].initialize_state_vector(self.state)

        self.common_state_vector = state_vector.CommonStateVector(self.state)

    def fold(self):
        self.state.fold()

    def relative_pot_sized_raise(self, percentage):
        raise_amount = self.calculate_relative_pot_sized_betting(percentage)
        self.raise_bet(raise_amount)

    def raise_bet(self, amount):
        player_seat = self.state.actor_index
        self.state.complete_bet_or_raise_to(amount)
        self.common_state_vector.update_raise(self.state, player_seat, amount)

    def call(self):
        self.state.check_or_call()

    def check(self):
        self.state.check_or_call()

    def calculate_relative_pot_sized_betting(self, percentage):
        calling_amount = 0
        if self.state.checking_or_calling_amount != None:
            calling_amount = self.state.checking_or_calling_amount

        total_pot = sum(list(self.state.pot_amounts)) + sum(self.state.bets) + calling_amount

        return total_pot * percentage + calling_amount

    def get_state(self):
        player_seat = self.state.actor_index
        if player_seat == None:
            print("No player is acting. Why did we ask for state here?")
            return

        player_state = self.player_state_vectors[player_seat]
        player_state.update_vector(self.state)
        self.common_state_vector.update_state(self.state)
        return player_state.state_vector + self.common_state_vector.state_vector

    #def reset(self):

    #def create_state(self):
