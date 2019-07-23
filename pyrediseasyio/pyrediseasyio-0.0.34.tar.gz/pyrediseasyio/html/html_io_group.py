from pyrediseasyio.io.boolean_io import BooleanIO
from pyrediseasyio.io.io_group import IOGroup
from pyrediseasyio.html.html_io import HTMLIO
from typing import List, Callable
from dominate.tags import div, table, tr, th
import dominate
import json


class HMTLIOGroup:

    def __init__(self, io_group: IOGroup):
        self._io_group = io_group
        self.namespace = io_group.namespace


    def _heading(self, headers, row_tag: dominate.tags, cell_tag: dominate.tags):
        if headers:
            with row_tag(cls="easyio_header_row"):
                for h in headers:
                    cell_tag(h, cls="easyio_header_cell")


    def html(self, headers: List[str] = None, html_id: str = None, **kwargs):
        """
        :param headers: An optional list of headers that can be applied to the table
        :param html_id: An optional ID that can be given to the table
        :param kwargs: (by_names, by_type, by_lambda_each, by_lambda_results,
                        show_units, show_set, show_reset, set_text, reset_text)
        :return:    Returns a dominate table object that can be rendered to html.
        """
        attrs = self._io_group.get_attributes(**kwargs)
        html_id = f'{attrs[0].key}_io_container' if html_id is None else html_id

        with div(cls=f'easyio_container', id=html_id) as container:
            self._heading(headers, div, div)
            for attr in attrs:
                HTMLIO(attr).as_divs(**kwargs)
        return container



    def html_table(self, headers: List[str] = None, html_id: str = None, **kwargs) -> table:
        """
        :param headers: An optional list of headers that can be applied to the table
        :param html_id: An optional ID that can be given to the table
        :param kwargs: (by_names, by_type, by_lambda_each, by_lambda_results,
                        show_units, show_set, show_reset, set_text, reset_text)
        :return:    Returns a dominate table object that can be rendered to html.
        """
        attrs = self._io_group.get_attributes(**kwargs)
        html_id = f'{attrs[0].addr}_io_container' if html_id is None else html_id

        with table(cls=f'easyio_container', id=html_id) as container:
            self._heading(headers, tr, th)
            for attr in attrs:
                HTMLIO(attr).as_table_row(**kwargs)
        return container



    def dumps(self, **kwargs):
        """
        Create a json string giving relevant information about each member of the IO Group useful at the web side.
        :param kwargs: (by_names, by_type, by_lambda_each, by_lambda_results)
        :return:
        """
        attrs = self._io_group.get_attributes(**kwargs)

        def f(a):
            io = HTMLIO(a)
            value, display_value = io.value, a.display_value
            return dict(id=io.value_id, name=io.name, value=io.value, units=io.units, display_value=display_value,
                        namespace=a.namespace, addr=a.addr)

        results = [f(a) for a in attrs]

        return json.dumps(results)


