RANK_MAP = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
SUIT_MAP = {'d': 1, 'c': 2, 'h': 3, 's': 4}

def card_to_vector(card):
    rank = card.rank.value
    suit = card.suit.value
    
    rank_vector = RANK_MAP[rank]
    suit_vector = SUIT_MAP[suit]
    
    return [rank_vector, suit_vector]

class PlayerStateVector:
    def __init__(self, player_seat):
        self.state_vector = [
            [], # hole_cards [[rank, suit],[rank, suit]]
            0, # position 0 = SB, 1 = BB, ...
            0, # current stack
        ]
        self.player_seat = player_seat # SB should be 0

    def initialize_state_vector(self, state):
        hole_cards = state.hole_cards[self.player_seat]
        hole_cards_vector = []
        for card in hole_cards:
            hole_cards_vector.append(card_to_vector(card))
        self.state_vector[0] = hole_cards_vector
        self.state_vector[1] = self.player_seat
        self.state_vector[2] = state.stacks[self.player_seat]
        self.player_seat = self.player_seat

    def update_vector(self, state):
        self.state_vector[2] = state.stacks[self.player_seat]


class CommonStateVector:
    INDEX_COMMUNITY_CARDS = 0
    INDEX_CURRENT_POT = 1
    INDEX_STARTING_STACKS = 2
    INDEX_CURRENT_STACKS = 3
    INDEX_PLAYER_STATUS = 4
    INDEX_INITIAL_BETS = 5
    INDEX_ALL_RAISES = 6

    def __init__(self, state):
        self.state_vector = [
            [[0,0]] * 5, # community cards [[rank, suit], [rank, suit], ...]
            0, # current pot total
            [], # starting stacks
            [], # current stacks
            [], # current players who are in the hand 0 = folded, 1 = active
            [], # initial bets
            [[-1, -1, -1]] * 30, # all raises, [[bet_amount, player_position, community_card_count] , ...], the community_card_count represents the phase of the game.
        ]

        self.max_player_count = 6
        self.raise_count = 0
        self.player_count = state.player_count
        # self.player_fill = self.max_player_count - self.player_count

        self.state_vector[self.INDEX_PLAYER_STATUS] = list(map(int, state.statuses)) # + [0] * self.player_fill
        self.state_vector[self.INDEX_INITIAL_BETS] = state.bets[:] # + [0] * self.player_fill
        self.state_vector[self.INDEX_STARTING_STACKS] = state.stacks[:]

    def update_raise(self, state, player_seat, raise_amount):
        board_card_count = len(state.board_cards)
        self.state_vector[self.INDEX_ALL_RAISES][self.raise_count] = [raise_amount, player_seat, board_card_count]
        self.raise_count += 1

    def update_call(self, state, player_seat, call_amount):
        print("blah")

    def update_state(self, state):
        board_cards_as_vector = []
        for card in state.board_cards:
            board_cards_as_vector.append(card_to_vector(card))

        for index, card in enumerate(board_cards_as_vector):
            self.state_vector[self.INDEX_COMMUNITY_CARDS][index] = card

        self.state_vector[self.INDEX_CURRENT_POT] = sum(list(state.pot_amounts)) + sum(state.bets)
        self.state_vector[self.INDEX_CURRENT_STACKS] = state.stacks
        self.state_vector[self.INDEX_PLAYER_STATUS] = list(map(int, state.statuses)) # + [0] * self.player_fill
