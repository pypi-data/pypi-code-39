import dominate
import gettext
from dominate.util import raw

from pyrediseasyio.io.trigger_io import TriggerIO
from pyrediseasyio.io.single_io import SingleIO
from pyrediseasyio.io.boolean_io import BooleanIO
from pyrediseasyio.io.float_io import FloatIO
from dominate.tags import div, tr, td, button
from typing import List, Tuple

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


    def _build(self, row_tag: dominate.tags, cell_tag: dominate.tags, **kwargs):
        show_name = bool(kwargs.get('show_name', True))
        show_value = bool(kwargs.get('show_value', True))
        show_set = bool(kwargs.get('show_set', False))
        show_reset = bool(kwargs.get('show_reset', False))
        show_change = bool(kwargs.get('show_change', False))
        show_units = bool(kwargs.get('show_units', False))
        set_text = str(kwargs.get('set_text', _("Set")))
        reset_text = str(kwargs.get('reset_text', _("Reset")))
        change_text = str(kwargs.get('change_text', _("Change")))

        io = self.io
        name, addr, val, units, ns = io.name, io.addr, io.value, io.units, self.namespace

        with row_tag(cls=f'easyio_io', id=self.container_id, data_type=type(io).__name__) as container:

            if show_name:
                self.name_cell(cell_tag)

            if show_value:
                self.value_cell(cell_tag)

            if show_units:
                units = '' if units is None else units
                cell_tag(units, cls=f'easyio_units')

            if show_set:
                with cell_tag(cls='easyio_btn_cell easyio_set_btn_cell'):
                    self.set_button(button, set_text, **kwargs)

            if show_reset:
                with cell_tag(cls='easyio_btn_cell easyio_rst_btn_cell'):
                    self.reset_button(button, reset_text, **kwargs)

            if show_change:
                with cell_tag(cls='easyio_btn_cell easyio_change_btn_cell'):
                    self.change_button(button, change_text, **kwargs)



        return container


    def as_divs(self, **kwargs) -> dominate.tags:
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
            set_button_attributes: List[Tuple]: Allows additional attributes to be give to the set button
            reset_button_attributes: List[Tuple]: Allows additional attributes to be give to the reset button
            change_button_attributes: List[Tuple]: Allows additional attributes to be give to the change button
        :return: dominate tag object that can be rendered to html.
        """
        return self._build(div, div, **kwargs)


    def as_table_row(self, **kwargs) -> dominate.tags:
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
            set_button_attributes: List[Tuple]: Allows additional attributes to be give to the set button
            reset_button_attributes: List[Tuple]: Allows additional attributes to be give to the reset button
            change_button_attributes: List[Tuple]: Allows additional attributes to be give to the change button
        :return: dominate tag object that can be rendered to html.
        """
        return self._build(tr, td, **kwargs)


    def change_button(self, tag: dominate.tags = button, txt: str = _("Change"),
                      change_button_attributes: List[Tuple] = None, **kwargs) -> dominate.tags:
        io = self.io
        change_button_attributes = [] if change_button_attributes is None else change_button_attributes
        name, addr, val, units, ns = io.name, io.addr, io.value, io.units, self.namespace
        ns = "na" if not ns else ns
        _max = io.max if hasattr(io, "max") else None
        _min = io.min if hasattr(io, "min") else None
        allow_decimal = isinstance(io, FloatIO)
        allow_negative = _min is None or _min < 0

        change_button_attributes.append(('data-allow-negative', str(allow_negative).lower()))
        change_button_attributes.append(('data-allow-decimal', str(allow_decimal).lower()))
        change_button_attributes.append(('data-units', str(io.units)))
        change_button_attributes.append(('data-max', _max))
        change_button_attributes.append(('data-min', _min))
        change_button_attributes.append(('data-value-id', io.key))
        change_button_attributes.append(('data-name', name))

        t = tag(txt, cls='easyio_change', onclick="EasyIOChange(event)")

        for a in change_button_attributes:
            t.attributes[a[0]] = a[1]
        return t


    def set_button(self, tag: dominate.tags = button, txt: str = "On", set_button_attributes: List[Tuple] = None,
                   **kwargs) -> dominate.tags:
        io = self.io
        name, addr, val, units, ns = io.name, io.addr, io.value, io.units, self.namespace
        set_button_attributes = [] if set_button_attributes is None else set_button_attributes
        value = self.default_set_value
        ns = "na" if not ns else ns

        set_button_attributes.append(('data-value-id', self.value_id))
        set_button_attributes.append(('data-value', str(value)))
        set_button_attributes.append(('data-namespace', ns))

        t = tag(txt, cls='easyio_set', onclick=f"EasyIOSet(event)")
        for a in set_button_attributes:
            t.attributes[a[0]] = a[1]
        return t


    def reset_button(self, tag: dominate.tags = button, txt: str = "Off", reset_button_attributes: List[Tuple] = None,
                     **kwargs)-> dominate.tags:
        io = self.io
        name, addr, val, units, ns = io.name, io.addr, io.value, io.units, self.namespace
        ns = "na" if not ns else ns
        value = self.default_reset_value
        reset_button_attributes = [] if reset_button_attributes is None else reset_button_attributes

        reset_button_attributes.append(('data-value-id', self.value_id))
        reset_button_attributes.append(('data-value', str(value)))
        reset_button_attributes.append(('data-namespace', ns))

        t = tag(txt, cls='easyio_reset', onclick=f"EasyIOSet(event)")
        for a in reset_button_attributes:
            t.attributes[a[0]] = a[1]
        return t


    def with_custom_tags(self, outer: dominate.tags, inner: dominate.tags, **kwargs):
        """
        Creates html containing relevant parts of the IO using table elements
        :param outer:         The tag type to use for the cell container (row)
        :param inner:         The tag type to use for the cell
        :param kwargs:
            show_name:  bool: optional value, set to false to hide name column.
            show_value: bool: optional, set to false to hide the value column.
            show_set:   bool: optional, set to True to show the 'set' button column.
            show_reset: bool: optional, set to False to show the 'reset' button column.
            show_change: bool: optional, on numeric entries, adds a change button.
            show_units: bool: optional, set to true so thow the units column.
            set_text:   str:  The text to place on the 'set' button
            reset_text: str:  The text to place on the 'reset' button)
            set_button_attributes: List[Tuple]: Allows additional attributes to be give to the set button
            reset_button_attributes: List[Tuple]: Allows additional attributes to be give to the reset button
            change_button_attributes: List[Tuple]: Allows additional attributes to be give to the change button
        :return: dominate tag object that can be rendered to html.
        """
        return self._build(tr, td, **kwargs)


    def name_cell(self, tag: dominate.tags = div) -> dominate.tags:
        return tag(self.io.name, cls=f'easyio_name')


    def value_cell(self, tag: dominate.tags = div, allow_entry: bool=False) -> dominate.tags:
        """Generate the html for generating the cell that contains the object value."""
        io = self.io
        name, addr, val, units, ns = io.name, io.addr, io.value, io.units, self.namespace
        val = False if val is None else val
        t = tag(val, cls=f'easyio_value', id=self.value_id, onchange='OnEasyIOValueChange(event)',
                 data_namespace=ns, data_addr=addr)

        if io.namespace is not None:
            t['data-namespace'] = io.namespace
        if hasattr(io, 'max') and io.max is not None:
            t['data-max'] = io.max
        if hasattr(io, 'min') and io.min is not None:
            t['data-min'] = io.min
        if io.units is not None:
            t['data-units'] = io.units

        if allow_entry:
            t['onenter'] = 'OnEasyIOValueMouseEnter(event)'