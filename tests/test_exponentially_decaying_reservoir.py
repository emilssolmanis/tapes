import unittest

import fudge

from tapes.local.reservoir import ExponentiallyDecayingReservoir


class ExponentiallyDecayingReservoirTestCase(unittest.TestCase):
    @fudge.patch('tapes.reservoir.time', 'tapes.reservoir.random')
    def test_update_always_applies_weight_to_values(self, time, random):
        (time
         .expects_call().returns(10)
         .next_call().returns(20)
         .next_call().returns(30)
         .next_call().returns(40)
         .next_call().returns(50)
         .next_call().returns(60)
         .next_call().returns(70))

        (random
         .expects_call().returns(0.1)
         .next_call().returns(0.2)
         .next_call().returns(0.3)
         .next_call().returns(0.4)
         .next_call().returns(0.01)
         .next_call().returns(0.01))

        reservoir = ExponentiallyDecayingReservoir(size=3)

        reservoir.update(1)
        reservoir.update(2)
        reservoir.update(3)
        reservoir.update(4)
        reservoir.update(5)
        reservoir.update(6)

        snapshot = reservoir.get_snapshot()
        assert float(snapshot.get_min()) > 0
        assert float(snapshot.get_max()) > 0
        assert float(snapshot.get_mean()) > 0
        assert float(snapshot.get_sd()) > 0
