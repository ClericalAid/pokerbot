import pytest

from poker.game import Game

import pdb

@pytest.fixture
def game():
    return Game()

class TestGame:
    """
    """
    def test_something(self, game):
        actor_index = game.state.actor_index
        raise_amount = 200
        game.raise_bet(raise_amount)
        state = game.get_state()
        # pdb.set_trace()
        index_offset = 3
        assert state[1] == 3
        assert state[2] == 10000
        assert state[index_offset + 0] == [[0,0], [0,0], [0,0], [0,0], [0,0]]
        assert state[index_offset + 1] == 350
        assert state[index_offset + 2] == [9950, 9900, 10000, 10000, 10000, 10000]
        assert state[index_offset + 3] == [9950, 9900, 9800, 10000, 10000, 10000]
        assert state[index_offset + 4] == [1, 1, 1, 1, 1, 1]
        assert state[index_offset + 5] == [50, 100, 0, 0, 0, 0]
        assert state[index_offset + 6][0] == [200, 2, 0]
