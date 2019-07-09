import unittest
from pyrediseasyio.io.io_group import IOGroup
from pyrediseasyio.html.html_io_group import HMTLIOGroup
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


class TestHTML(unittest.TestCase):

    def test_boolean_div_conversion(self):
        h = HMTLIOGroup(test_group).html(show_units=True).render()
        expected = '''
        <div class="easyio_container" id="Pin1Bool1_io_container">
          <div class="easyio_io" data-type="BooleanIO" id="Pin1Bool1_io">
            <div class="easyio_name">Boolean 1</div>
            <div class="easyio_value" data-addr="Bool1" data-namespace="Pin1" data-units="On/Off" id="Pin1Bool1" onchange="OnEasyIOValueChange(event)">False</div>
            <div class="easyio_units">On/Off</div>
          </div>
          <div class="easyio_io" data-type="FloatIO" id="Pin1Float1_io">
            <div class="easyio_name">Float 1</div>
            <div class="easyio_value" data-addr="Float1" data-namespace="Pin1" data-units="furlongs" id="Pin1Float1" onchange="OnEasyIOValueChange(event)">1.23</div>
            <div class="easyio_units">furlongs</div>
          </div>
        </div>
        '''
        assert_that(html_equals(h, expected)).is_true()

    def test_boolean_table_conversion(self):
        h = HMTLIOGroup(test_group).html_table(show_units=True).render()
        expected = '''
        <table class="easyio_container" id="Bool1_io_container">
          <tr class="easyio_io" data-type="BooleanIO" id="Pin1Bool1_io">
            <td class="easyio_name">Boolean 1</td>
            <td class="easyio_value" data-addr="Bool1" data-namespace="Pin1" data-units="On/Off" id="Pin1Bool1" onchange="OnEasyIOValueChange(event)">False</td>
            <td class="easyio_units">On/Off</td>
          </tr>
          <tr class="easyio_io" data-type="FloatIO" id="Pin1Float1_io">
            <td class="easyio_name">Float 1</td>
            <td class="easyio_value" data-addr="Float1" data-namespace="Pin1" data-units="furlongs" id="Pin1Float1" onchange="OnEasyIOValueChange(event)">1.23</td>
            <td class="easyio_units">furlongs</td>
          </tr>
        </table>
        '''
        assert_that(html_equals(h, expected)).is_true()


    def test_different_id(self):
        h = HMTLIOGroup(test_group).html_table(html_id="NewID", show_units=True).render()
        expected = '''
        <table class="easyio_container" id="NewID">
          <tr class="easyio_io" data-type="BooleanIO" id="Pin1Bool1_io">
            <td class="easyio_name">Boolean 1</td>
            <td class="easyio_value" data-addr="Bool1" data-namespace="Pin1" data-units="On/Off" id="Pin1Bool1" onchange="OnEasyIOValueChange(event)">False</td>
            <td class="easyio_units">On/Off</td>
          </tr>
          <tr class="easyio_io" data-type="FloatIO" id="Pin1Float1_io">
            <td class="easyio_name">Float 1</td>
            <td class="easyio_value" data-addr="Float1" data-namespace="Pin1" data-units="furlongs" id="Pin1Float1" onchange="OnEasyIOValueChange(event)">1.23</td>
            <td class="easyio_units">furlongs</td>
          </tr>
        </table>
        '''
        assert_that(html_equals(h, expected)).is_true()


    def test_set_reset_true(self):
        h = HMTLIOGroup(test_group).html_table(
            html_id="NewID", show_units=False, show_set=True, show_reset=True, set_text="SetMe").render()
        expected = '''
        <table class="easyio_container" id="NewID">
          <tr class="easyio_io" data-type="BooleanIO" id="Pin1Bool1_io">
            <td class="easyio_name">Boolean 1</td>
            <td class="easyio_value" data-addr="Bool1" data-namespace="Pin1" data-units="On/Off" id="Pin1Bool1" onchange="OnEasyIOValueChange(event)">False</td>
            <td class="easyio_btn_cell easyio_set_btn_cell">
              <button class="easyio_set" onclick="EasyIOSet('Pin1','Bool1','Pin1Bool1','True')">SetMe</button>
            </td>
            <td class="easyio_btn_cell easyio_rst_btn_cell">
              <button class="easyio_reset" onclick="EasyIOSet('Pin1','Bool1','Pin1Bool1','False')">Reset</button>
            </td>
          </tr>
          <tr class="easyio_io" data-type="FloatIO" id="Pin1Float1_io">
            <td class="easyio_name">Float 1</td>
            <td class="easyio_value" data-addr="Float1" data-namespace="Pin1" data-units="furlongs" id="Pin1Float1" onchange="OnEasyIOValueChange(event)">1.23</td>
            <td class="easyio_btn_cell easyio_set_btn_cell">
              <button class="easyio_set" onclick="EasyIOSet('Pin1','Float1','Pin1Float1','1.23')">SetMe</button>
            </td>
            <td class="easyio_btn_cell easyio_rst_btn_cell">
              <button class="easyio_reset" onclick="EasyIOSet('Pin1','Float1','Pin1Float1','0')">Reset</button>
            </td>
          </tr>
        </table>
        '''
        assert_that(html_equals(h, expected)).is_true()



    def test_json_dumps_basic(self):
        h = HMTLIOGroup(test_group)
        d = h.dumps()
        as_list = json.loads(d)
        first = as_list[0]
        assert_that(len(as_list)).is_equal_to(len(test_group))
        assert_that(first['name']).is_equal_to('Boolean 1')
        assert_that(first['display_value']).is_equal_to("Off")


    def test_json_dumps_by_name(self):
        h = HMTLIOGroup(test_group)
        d = h.dumps(by_names=['Bool1'])
        as_list = json.loads(d)
        assert_that(len(as_list)).is_equal_to(1)
