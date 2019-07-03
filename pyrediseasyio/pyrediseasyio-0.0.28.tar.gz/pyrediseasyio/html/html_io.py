import dominate
import gettext
from dominate.util import raw

from pyrediseasyio.io.trigger_io import TriggerIO
from pyrediseasyio.io.single_io import SingleIO
from pyrediseasyio.io.boolean_io import BooleanIO
from dominate.tags import div, tr, td, button

_ = gettext.gettext


class HTMLIO:

    def __init__(self, io: SingleIO):
        key = io.key
        self.io = io
        self.container_id = f'{key}_io'
        self.value_id = f'{key}'
        self.name = io.name
        self.value = io.value
        self.units = io.units
        self.namespace = io.namespace
        self.default_set_value = True if isinstance(io, BooleanIO) or isinstance(io, TriggerIO) else io.default
        self.default_reset_value = False if isinstance(io, BooleanIO) or isinstance(io, TriggerIO) else 0

    def build(self, row_tag: dominate.tags, cell_tag: dominate.tags, **kwargs):
        """
        Creates html containing relevant parts of the IO
        :param row_tag: The html tag to use for rows
        :param cell_tag: The html tage to use for cells
        :param kwargs:
            show_name:  bool: optional value, set to false to hide name column.
            show_value: bool: optional, set to false to hide the value column.
            show_set:   bool: optional, set to True to show the 'set' button column.
            show_reset: bool: optional, set to False to show the 'reset' button column.
            show_units: bool: optional, set to true so thow the units column.
            set_text:   str:  The text to place on the 'set' button
            reset_text: str:  The text to place on the 'reset' button)
        :return: dominate tag object that can be rendered to html.
        """
        show_name = bool(kwargs.get('show_name', True))
        show_value = bool(kwargs.get('show_value', True))
        show_set = bool(kwargs.get('show_set', False))
        show_reset = bool(kwargs.get('show_reset', False))
        show_units = bool(kwargs.get('show_units', False))
        set_text = str(kwargs.get('set_text', _("Set")))
        reset_text = str(kwargs.get('reset_text', _("Reset")))

        io = self.io
        name, addr, val, units, ns = io.name, io.addr, io.value, io.units, self.namespace

        with row_tag(cls=f'easyio_io', id=self.container_id, data_type=type(io).__name__) as container:

            if show_name:
                self.html_name_cell(cell_tag)

            if show_value:
                self.html_value_cell(cell_tag)

            if show_units:
                units = '' if units is None else units
                cell_tag(units, cls=f'easyio_units')

            if show_set:
                with cell_tag(cls='easyio_btn_cell easyio_set_btn_cell'):
                    self.set_button(button, set_text)

            if show_reset:
                with cell_tag(cls='easyio_btn_cell easyio_rst_btn_cell'):
                    self.reset_button(button, reset_text)


        return container


    def set_button(self, tag: dominate.tags = button, txt: str = "On"):
        io = self.io
        name, addr, val, units, ns = io.name, io.addr, io.value, io.units, self.namespace
        ns = "na" if not ns else ns
        value = self.default_set_value
        value = str(value).lower()
        return tag(txt, cls='easyio_set', onclick=f"EasyIOSet('{ns}','{addr}','{self.value_id}',{value})")


    def reset_button(self, tag: dominate.tags = button, txt: str = "Off") -> dominate.tags:
        io = self.io
        name, addr, val, units, ns = io.name, io.addr, io.value, io.units, self.namespace
        ns = "na" if not ns else ns
        value = self.default_reset_value
        value = str(value).lower()
        return tag(txt, cls='easyio_reset', onclick=f"EasyIOSet('{ns}','{addr}','{self.value_id}',{value})")


    def html(self, **kwargs) -> dominate.tags:
        """
        Creates html containing relevant parts of the IO using div elements
        :param kwargs:
            show_name:  bool: optional value, set to false to hide name column.
            show_value: bool: optional, set to false to hide the value column.
            show_set:   bool: optional, set to True to show the 'set' button column.
            show_reset: bool: optional, set to False to show the 'reset' button column.
            show_units: bool: optional, set to true so thow the units column.
            set_text:   str:  The text to place on the 'set' button
            reset_text: str:  The text to place on the 'reset' button)
        :return: dominate tag object that can be rendered to html.
        """
        return self.build(div, div, **kwargs)


    def html_row(self, **kwargs) -> dominate.tags:
        """
        Creates html containing relevant parts of the IO using table elements
        :param kwargs:
            show_name:  bool: optional value, set to false to hide name column.
            show_value: bool: optional, set to false to hide the value column.
            show_set:   bool: optional, set to True to show the 'set' button column.
            show_reset: bool: optional, set to False to show the 'reset' button column.
            show_units: bool: optional, set to true so thow the units column.
            set_text:   str:  The text to place on the 'set' button
            reset_text: str:  The text to place on the 'reset' button)
        :return: dominate tag object that can be rendered to html.
        """
        return self.build(tr, td, **kwargs)


    def html_name_cell(self, tag: dominate.tags = div) -> dominate.tags:
        return tag(self.io.name, cls=f'easyio_name')


    def html_value_cell(self, tag: dominate.tags = div) -> dominate.tags:
        """Generate the html for generating the cell that contains the object value."""
        io = self.io
        name, addr, val, units, ns = io.name, io.addr, io.value, io.units, self.namespace
        val = False if val is None else val
        return tag(val, cls=f'easyio_value', id=self.value_id, onchange='OnEasyIOValueChange(event)',
                 data_namespace=ns, data_addr=addr)

    def html_value_svg_circle(self, x: int, y: int, r: int):
        return raw(f'<circle cls=easyio_value" id="{self.value_id}" cx="{x}" cy="{y}" r="{r}"></circle>')









