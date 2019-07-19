import unittest
import logging
from ftdi_serial import Serial
from north_utils.test import assert_equal, assert_float_equal
from north_utils.drivers.tecan_cavro import TecanCavro

logging.basicConfig(level=logging.DEBUG)


class TecanCavroTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.serial = Serial(baudrate=38400)
        cls.cavro = TecanCavro(cls.serial, 0)
        cls.cavro.home()

    @classmethod
    def tearDownClass(cls):
        cls.serial.disconnect()

    def test_loop(self):
        self.cavro.loop_start()
        self.cavro.move_absolute_counts(1000)
        self.cavro.move_absolute_counts(0)
        self.cavro.loop_end(2)
        self.cavro.execute()

    def test_dispense(self):
        self.cavro.dispense_ml(0.5, 1, 2, velocity_counts=500)
        self.cavro.dispense_ml(2.5, 1, 2)

    def test_move_velocity(self):
        self.cavro.move_absolute_counts(1400, velocity_counts=500)
        self.cavro.move_absolute_counts(0)