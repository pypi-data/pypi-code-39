import unittest
from pyrediseasyio.io.io_group import IOGroup
from pyrediseasyio import BooleanIO, IntIO, FloatIO, StringIO
from assertpy import assert_that

class TestGroup(IOGroup):
    Int1 = IntIO("Some Int")
    Float1 = FloatIO("Some Float")


class TestOperatorOverloads(unittest.TestCase):

    def setUp(self) -> None:
        self.group = TestGroup

    def test_add_sub_mult_div(self):
        group = self.group
        group.Int1 = 100
        group.Float1 = 5
        assert_that(group.Int1 + group.Float1).is_equal_to(105)
        assert_that(group.Int1 - group.Float1).is_equal_to(95)
        assert_that(group.Int1 * group.Float1).is_equal_to(500)
        assert_that(group.Int1 / group.Float1).is_equal_to(20)

    def test_plus_equals(self):
        group = self.group
        group.Int1 += 5
        assert_that(group.Int1).is_equal_to(5)