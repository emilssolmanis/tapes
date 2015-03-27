import unittest

import fudge

from tapes.reservoir import ExponentiallyDecayingReservoir


class ExponentiallyDecayingReservoirTestCase(unittest.TestCase):
    @fudge.patch('tapes.reservoir.time', 'tapes.reservoir.random')
    def test_update_always_applies_weight_to_values(self, time, random):
        (time
         .expects_call().returns(1.0)
         .next_call().returns(10).next_call().returns(10)
         .next_call().returns(20).next_call().returns(20)
         .next_call().returns(30).next_call().returns(30)
         .next_call().returns(40).next_call().returns(40)
         .next_call().returns(50).next_call().returns(50)
         .next_call().returns(60).next_call().returns(60))

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

    @fudge.patch('tapes.reservoir.time')
    def test_reservoir_gets_rescaled(self, time):
        (time.expects_call().returns(1.0)
         .next_call().returns(2.0)
         .next_call().returns(2.0)
         .next_call().returns(24 * 60 * 60.0)
         .next_call().returns(24 * 60 * 60.0))

        r = ExponentiallyDecayingReservoir()
        r.update(0.4)
        # This happens 24h after start. If the reservoir isn't rescaled, this raises an overflow error
        # because of exp(1000-ish)
        r.update(0.6)

        s = r.get_snapshot()
        assert s.get_max() == 0.6
        assert s.get_min() == 0.4
        assert s.get_mean() == 0.6
