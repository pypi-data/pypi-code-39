import unittest
from X4_parser import *
from TSW_IWR import *
from X4_threshold import *


class TestParser(unittest.TestCase):

    def test_iq(self):
        """
        Method to test if .dat binary file was converted successfully to .csv file with in-phase and quadrature
        components together.
        """
        file_iq = iq_data('X4data.dat', 'X4iq')
        self.assertEqual(file_iq, 'converted')

    def test_raw(self):
        """
        Method to test if .dat binary file was converted successfully to .csv file with in-phase and quadrature
        component separated.
        """
        file_raw = raw_data('X4data.dat', 'X4raw')
        self.assertEqual(file_raw, 'converted')

    def test_TSW(self):
        """
        Method to test if .bin binary file was converted successfully to .csv file with iq data put together.
        """

        file_TI = readTSWdata('TIdata.bin', 'TIdata')
        self.assertEqual(file_TI, 'converted')

    def X4_Threshold_range_finder(self):
        """
        Method to test if correct range bin was gotten from running function on csv file.
        """

        range_bin = range_finder("Heli150040.csv",0.02)
        self.assertEqual(range_bin, [9])

    def X4_Threshold_bin_to_distance(self):
        """
        Method to test if range bin to distance converted correctly
        """

        bin_to_distance = distance_finder("Heli150040.csv", 0.02)
        self.assertEqual(bin_to_distance, [29.25])

    def X4_Threshold_noise_estimate(self):
        """
        Method to test if noise estimate was calculated properly
        """

        noise_estimate = noise_power_estimate("Heli150040.csv", 0.02)
        self.assertEqual(noise_estimate, 0.00045988029076158947)


if __name__ == '__main__':
    unittest.main()
