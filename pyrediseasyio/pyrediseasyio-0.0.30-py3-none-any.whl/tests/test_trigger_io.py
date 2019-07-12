import unittest
from pyrediseasyio.io.io_group import IOGroup
from pyrediseasyio import BooleanIO, IntIO, FloatIO, StringIO, TriggerIO
from assertpy import assert_that
from htmldiffer import utils as diff_utils
import json


class TestGroup(IOGroup):
    Bool1 = BooleanIO("Boolean 1", "Bool1", False)
    Bool2 = BooleanIO("Boolean 2", "Bool2", True)
    Int1 = IntIO("Integer 1", "Int1")
    Int2 = IntIO("Integer 2", "Int2", default=34)
    Float1 = FloatIO("Float 1", "Float1", default=1.2)

    def __init__(self):
        super().__init__(channel="TestChannel")

    @staticmethod
    def on_reset_write(value):
        pass

    @staticmethod
    def on_reset_read():
        pass


class TestGroup2(IOGroup):
    Bool1 = BooleanIO("Boolean 1", "Bool1", False)
    Bool2 = BooleanIO("Boolean 2", "Bool2", True)
    Int1 = IntIO("Integer 1", "Int1")
    Int2 = IntIO("Integer 2", "Int2", default=34)
    Float1 = FloatIO("Float 1", "Float1", default=1.2)
    Message1 = StringIO("String 1", "String1")
    ApplyMany = TriggerIO("Apply to Many")


class TestTriggerIO(unittest.TestCase):

    def on_write_reset(self, value):
        tf, i, f = value
        self.testgroup1.Bool1 = tf
        self.testgroup2.Bool1 = tf
        self.testgroup1.Int1 = i
        self.testgroup2.Int1 = i
        self.testgroup1.Float1 = f
        self.testgroup2.Float1 = f

    def on_read_reset(self):
        tg1, tg2 = self.testgroup1, self.testgroup2
        return tg1.Int1, tg2.Float1

    def setUp(self) -> None:
        self.testgroup1 = TestGroup()
        self.testgroup2 = TestGroup2()
        self.testgroup2.ApplyMany.write_callback = self.on_write_reset
        self.testgroup2.ApplyMany.read_callback = self.on_read_reset

    def test_trigger_write(self):
        tg1, tg2 = self.testgroup1, self.testgroup2
        tg2.ApplyMany = (True, 100, 120.5)
        assert_that(tg1.Bool1).is_true()
        assert_that(tg2.Bool1).is_true()
        assert_that(tg1.Int1).is_equal_to(100)
        assert_that(tg2.Int1).is_equal_to(100)
        assert_that(tg1.Float1).is_equal_to(120.5)
        assert_that(tg2.Float1).is_equal_to(120.5)

    def test_trigger_read(self):
        tg1, tg2 = self.testgroup1, self.testgroup2
        tg1.Int1 = 333
        tg2.Float1 = 444.4
        a, b = tg2.ApplyMany
        assert_that(a).is_equal_to(333)
        assert_that(b).is_equal_to(444.4)