import unittest
from pyrediseasyio.io.io_group import IOGroup
from pyrediseasyio import BooleanIO, IntIO, FloatIO, StringIO
from assertpy import assert_that


class TestGroup(IOGroup):
    Bool1 = BooleanIO("Boolean 1", "Bool1", False)
    Bool2 = BooleanIO("Boolean 2", "Bool2", True)
    Int1 = IntIO("Integer 1", "Int1")
    Int2 = IntIO("Integer 2", "Int2", default=34)
    Float1 = FloatIO("Float 1", "Float1", default=1.2)
    MinMaxInt = IntIO("Int with min/max", min=-10, max=220)
    MinMaxFloat = FloatIO("Float with min/max", min=-30.2, max=9999.9)

    def __init__(self):
        super().__init__(channel="TestChannel")


class TestGroup2(IOGroup):
    Bool1 = BooleanIO("Boolean 1", "Bool1", False)
    Bool2 = BooleanIO("Boolean 2", "Bool2", True)
    Int1 = IntIO("Integer 1", "Int1")
    Int2 = IntIO("Integer 2", "Int2", default=34)
    Float1 = FloatIO("Float 1", "Float1", default=1.2)
    Message1 = StringIO("String 1", "String1")

    def __init__(self):
        super().__init__(channel="TestChannel")


class TestGroup3(IOGroup):
    def __init__(self, db=2):
        self.Bool1 = BooleanIO("Boolean 1", default=False)
        self.Bool2 = BooleanIO("Boolean 2", "Bool2", True)
        self.Int1 = IntIO("Integer 1", "Int1")
        self.Int2 = IntIO("Integer 2", "Int2", default=34)
        self.Float1 = FloatIO("Float 1", "Float1", default=1.2)
        super().__init__(db=db)


class TestReadWrite(unittest.TestCase):

    def setUp(self):
        self.group = TestGroup()
        self.group2 = TestGroup2()
        self.group3 = TestGroup3()
        self.group.flush_db()
        self.group2.flush_db()
        self.group3.flush_db()

    def test_that_defaults_are_applied(self):
        group = self.group
        group3 = self.group3

        assert_that(group.Bool1).is_false()
        assert_that(group.Bool2).is_true()
        assert_that(group.Int1).is_equal_to(0)
        assert_that(group.Int2).is_equal_to(34)
        assert_that(group.Float1).is_equal_to(1.2)

        assert_that(group3.Bool1).is_false()
        assert_that(group3.Bool2).is_true()
        assert_that(group3.Int1).is_equal_to(0)
        assert_that(group3.Int2).is_equal_to(34)
        assert_that(group3.Float1).is_equal_to(1.2)

    def test_basic_read_write(self):
        group1 = self.group
        group2 = self.group2

        group4 = TestGroup3(db=2)
        group5 = TestGroup3(db=2)

        group1.Bool1 = True
        assert_that(group2.Bool1).is_true()
        group1.Bool1 = False
        assert_that(group2.Bool1).is_false()

        group1.Int1 = 100
        assert_that(group2.Int1).is_equal_to(100)
        group1.Int1 = -100
        assert_that(group2.Int1).is_equal_to(-100)

        group4.Float1 = 123.4
        assert_that(group5.Float1).is_equal_to(123.4)

        group4.Bool1 = True
        assert_that(group5.Bool1).is_true()
        group4.Bool1 = False
        assert_that(group5.Bool1).is_false()

        group4.Int1 = 100
        assert_that(group5.Int1).is_equal_to(100)
        group4.Int1 = -100
        assert_that(group5.Int1).is_equal_to(-100)

        group4.Float1 = 123.4
        assert_that(group5.Float1).is_equal_to(123.4)

    def test_same_name_different_database(self):
        group1 = self.group
        group2 = self.group2
        group3 = self.group3
        group4 = TestGroup3(db=5)

        group1.Int1 = 234
        assert_that(group2.Int1).is_equal_to(234)
        assert_that(group3.Int1).is_not_equal_to(234)

        group4.Float1 = 555
        assert_that(group4.Float1).is_equal_to(555)
        assert_that(group3.Float1).is_not_equal_to(555)

    def test_that_group_can_be_saved_to_memory(self):
        group = self.group
        group2 = self.group2
        j = group.dump("SomeKey")
        assert_that(j).is_not_none()
        assert_that(len(j)).is_greater_than(10)

        r = group2.read("SomeKey")
        assert_that(r).is_equal_to(j)

    def test_arithmatic_operations(self):
        group1 = self.group
        group3 = self.group3

        group1.Float1 = 10.0
        group3.Float1 = 20.0

        assert_that(group1.Float1 + group3.Float1).is_equal_to(30)
        assert_that(group1.Float1 * group3.Float1).is_equal_to(200)
        assert_that(group3.Float1 / group1.Float1).is_equal_to(2)
        assert_that(group3.Float1 - group1.Float1).is_equal_to(10)

    def test_that_pubsub_possible_on_io_group(self):
        group = self.group
        group2 = self.group2

        group2.Message1.publish("This is a test")

        msg = None
        for m in group.listen():
            msg = m
            break

        assert_that("This is a test" in msg[1]).is_true()


    def test_values_can_be_set_to_default(self):
        group1 = self.group
        group1.Bool1 = True
        group1.Float1 = 99

        assert_that(group1.Bool1).is_true()
        assert_that(group1.Float1).is_equal_to(99)

        group1.set_all_to_defaults()
        assert_that(group1.Bool1).is_false()
        assert_that(group1.Float1).is_equal_to(1.2)


    def test_that_values_are_min_max_limited(self):
        group = self.group
        group.MinMaxInt = 20
        group.MinMaxFloat = 30.0
        assert_that(group.MinMaxInt).is_equal_to(20)
        assert_that(group.MinMaxFloat).is_equal_to(30.0)

        group.MinMaxInt = 250
        assert_that(group.MinMaxInt).is_equal_to(220)
        group.MinMaxInt = -60
        assert_that(group.MinMaxInt).is_equal_to(-10)

        group.MinMaxFloat = 20000
        assert_that(group.MinMaxFloat).is_equal_to(9999.9)
