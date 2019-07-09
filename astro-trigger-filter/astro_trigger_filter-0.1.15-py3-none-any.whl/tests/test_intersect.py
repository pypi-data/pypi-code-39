import unittest
import random
from astrotc.radio_pulse import RadioPulseIntersectionGen, test_radio_pulse_intersection, dm_one_delay


class TestIntersect(unittest.TestCase):

    def setUp(self):
        self.freq_lo_mhz = 1249.8
        self.freq_hi_mhz = 1549.8
        self.sample_rate = 8.192e-05
        self.tol = 0.0001

    def make_test_case(self, r, N, dm1):
        # Set the seed so that we can reproduce the random numbers
        random.seed(r)

        # Create a list of random triggers
        triggers = [
            (
                random.uniform(0, 0.1),
                random.uniform(0, 0.01),
                random.uniform(0, 100),
                i
            )
            for i in range (N)
        ]

        # Sort triggers on time
        triggers.sort(key=lambda tup: tup[0])

        # use a brute force reference method to create a list of all intersections
        pairs_true = []
        dm1 = dm_one_delay(self.freq_lo_mhz, self.freq_hi_mhz)

        for i in range(N):
            for k in range(i+1,N):
                if test_radio_pulse_intersection(
                    *triggers[i][:3],
                    *triggers[k][:3],
                    dm1,
                    self.tol
                ):
                    e = (triggers[i][3],triggers[k][3])
                    pairs_true.append("{}-{}".format(min(e), max(e)))
        pairs_true.sort()

        return triggers, pairs_true

    def test_intersect(self):

        R = 100
        N = 20
        debug =  False

        # repeat the test R times
        for r in range(R):

            gen = RadioPulseIntersectionGen(self.freq_lo_mhz, self.freq_hi_mhz, self.tol)

            triggers, pairs_true = self.make_test_case(r, N, gen.dm1 )

            # test the generator to create a list of all intersections
            pairs = ["{}-{}".format(min(e), max(e)) for e in gen(triggers)]
            pairs.sort()

            if debug:
                # Print some debug info
                print("\nRANDOM TEST nr", r)
                for t in triggers:
                    print(t)
                print("generator", pairs)
                print("actual", pairs_true)

            with self.subTest(msg="sub test r={}, N={}".format(r, N)):
                self.assertEqual(pairs, pairs_true)


if __name__ == '__main__':
    unittest.main()
