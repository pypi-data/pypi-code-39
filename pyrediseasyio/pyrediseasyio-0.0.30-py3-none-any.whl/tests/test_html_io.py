import unittest
from pyrediseasyio.io.io_group import IOGroup
from pyrediseasyio.html.html_io import HTMLIO
from pyrediseasyio import BooleanIO, SingleIO, FloatIO, StringIO
from assertpy import assert_that
from htmldiffer import utils as diff_utils
import json


class TestGroup(IOGroup):
    Bool1 = BooleanIO("Boolean 1", units="On/Off")
    Float1 = FloatIO("Float 1", default=1.23, units="furlongs")


test_group = TestGroup(namespace='Pin1')


def html_equals(actual, expected):
    lines1 = [line.strip() for line in diff_utils.html2list(actual)]
    lines1 = [line for line in lines1 if len(line) > 0]
    lines2 = [line.strip() for line in diff_utils.html2list(expected)]
    lines2 = [line for line in lines2 if len(line) > 0]
    diffs = [(line[0], line[1]) for line in zip(lines1, lines2) if line[0] != line[1]]
    return lines1 == lines2


class TestHTMLIO(unittest.TestCase):

    def test_can_add_set_button_attributes(self):
        attrs = [
            ('data-test', 'Test'),
            ('data-me', 'Me')
        ]
        h = HTMLIO(test_group.Bool1).as_divs(show_set = True, set_button_attributes=attrs)
        print(h)