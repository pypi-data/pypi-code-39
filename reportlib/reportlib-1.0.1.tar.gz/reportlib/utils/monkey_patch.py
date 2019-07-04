from uuid import uuid1
from decimal import Decimal
from itertools import product

import numpy as np
import pandas.core.common as com
from IPython.display import display, HTML
from pandas import DataFrame, get_option, Index
from pandas.io.formats.style import Styler as BaseStyler, _get_level_lengths, _is_visible, _maybe_wrap_formatter
from pandas.core.indexing import _non_reducing_slice, _maybe_numeric_slice
from pandas.api.types import is_dict_like

from reportlib.utils.templating import template_loader

__all__ = ['patch']


def patch_pandas():
    def show(self, *args, **kwargs):
        display(HTML(self.to_html(*args, **kwargs)))

    DataFrame.show = show


class Styler(BaseStyler):
    template = template_loader.get_template('base/table.html')
    
    @staticmethod
    def format_attr(pair):
        return '{key}="{value}"'.format(**pair)
    
    @staticmethod
    def _number_formatter(divisor=None, precision=None, fillna=None, fillzero=None, percentage=False):
        postfix = '%' if percentage else ''
        precision_fmt = '.%df' % precision if precision is not None else ''
        def formatter(x):
            if fillna is not None and x == np.nan:
                return fillna
            if isinstance(x, (int, float, complex, Decimal, np.number)):
                if divisor is not None:
                    x /= divisor
                if precision is not None:
                    x = round(x, precision)
                if fillzero is not None and x == 0:
                    return fillzero
                return ('{:,%s}%s' % (precision_fmt, postfix)).format(x)
            else:
                return x
        return formatter
      
    def format_number(self, subset=None, **kwargs):          
        formatter = self._number_formatter(**kwargs)
        return self.add_class('text-right', subset=subset).format(formatter, subset=subset)
      
    def format(self, formatter, subset=None):
        """
        Format the text display value of cells.

        .. versionadded:: 0.18.0

        Parameters
        ----------
        formatter : str, callable, or dict
        subset : IndexSlice
            An argument to ``DataFrame.loc`` that restricts which elements
            ``formatter`` is applied to.

        Returns
        -------
        self : Styler

        Notes
        -----

        ``formatter`` is either an ``a`` or a dict ``{column name: a}`` where
        ``a`` is one of

        - str: this will be wrapped in: ``a.format(x)``
        - callable: called with the value of an individual cell

        The default display value for numeric values is the "general" (``g``)
        format with ``pd.options.display.precision`` precision.

        Examples
        --------

        >>> df = pd.DataFrame(np.random.randn(4, 2), columns=['a', 'b'])
        >>> df.style.format("{:.2%}")
        >>> df['c'] = ['a', 'b', 'c', 'd']
        >>> df.style.format({'c': str.upper})
        """
        if subset is None:
            row_locs = range(len(self.data))
            col_locs = range(len(self.data.columns))
        else:
            subset = _non_reducing_slice(subset)
            sub_df = self.data.loc[subset]
            row_locs = self.data.index.get_indexer_for(sub_df.index)
            col_locs = self.data.columns.get_indexer_for(sub_df.columns)

        if is_dict_like(formatter):
            for col, col_formatter in formatter.items():
                # formatter must be callable, so '{}' are converted to lambdas
                col_formatter = _maybe_wrap_formatter(col_formatter)
                col_num = self.data.columns.get_indexer_for([col])[0]

                for row_num in row_locs:
                    self._display_funcs[(row_num, col_num)] = col_formatter
        else:
            # single scalar to format all cells with
            locs = product(*(row_locs, col_locs))
            for i, j in locs:
                formatter = _maybe_wrap_formatter(formatter)
                self._display_funcs[(i, j)] = formatter
        return self
                
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cell_context = {}

    def add_class(self, class_name, subset=None):
        n_rlvls = self.data.index.nlevels
        rlabels = self.data.index.tolist()

        if n_rlvls == 1:
            rlabels = [[x] for x in rlabels]
            
        if subset is None:
            row_locs = range(len(self.data))
            col_locs = range(len(self.data.columns))
        else:
            subset = _non_reducing_slice(subset)
            sub_df = self.data.loc[subset]
            row_locs = self.data.index.get_indexer_for(sub_df.index)
            col_locs = self.data.columns.get_indexer_for(sub_df.columns)

        locs = product(*(row_locs, col_locs))
        for r, c in locs:
            self._add_class('data', r, c, class_name)
            
        return self

    def _add_class(self, key, r, c, class_name):
        if key not in self.cell_context:
            self.cell_context[key] = {}
        if r not in self.cell_context[key]:
            self.cell_context[key][r] = {}
        if c not in self.cell_context[key][r]:
            self.cell_context[key][r][c] = []
        self.cell_context[key][r][c].append(class_name)

    def show(self, **kwargs):
        display(HTML(self.render(**kwargs)))
        
    def render(self, **kwargs):
        if 'table_attributes' not in kwargs:
            kwargs['table_attributes'] = self.format_attr({"key": "class", "value": "rp-table rp-table-default rp-table-hover"})
        return super().render(**kwargs)
      
    def _translate(self):
        """
        Convert the DataFrame in `self.data` and the attrs from `_build_styles`
        into a dictionary of {head, body, uuid, cellstyle}.
        """
        table_styles = self.table_styles or []
        caption = self.caption
        ctx = self.ctx
        precision = self.precision
        hidden_index = self.hidden_index
        hidden_columns = self.hidden_columns
        uuid = self.uuid or str(uuid1()).replace("-", "_")
        ROW_HEADING_CLASS = "row_heading"
        COL_HEADING_CLASS = "col_heading"
        INDEX_NAME_CLASS = "index_name"

        DATA_CLASS = "data"
        BLANK_CLASS = "blank"
        BLANK_VALUE = ""

        # for sparsifying a MultiIndex
        idx_lengths = _get_level_lengths(self.index)
        col_lengths = _get_level_lengths(self.columns, hidden_columns)

        cell_context = self.cell_context

        n_rlvls = self.data.index.nlevels
        n_clvls = self.data.columns.nlevels
        rlabels = self.data.index.tolist()
        clabels = self.data.columns.tolist()

        if n_rlvls == 1:
            rlabels = [[x] for x in rlabels]
        if n_clvls == 1:
            clabels = [[x] for x in clabels]
        clabels = list(zip(*clabels))

        cellstyle = []
        head = []

        for r in range(n_clvls):
            # Blank for Index columns...
            row_es = [{"type": "th",
                       "value": BLANK_VALUE,
                       "display_value": BLANK_VALUE,
                       "is_visible": not hidden_index,
                       "class": " ".join([BLANK_CLASS])}] * (n_rlvls - 1)

            # ... except maybe the last for columns.names
            name = self.data.columns.names[r]
            cs = []
            name = BLANK_VALUE if name is None else name
            row_es.append({"type": "th",
                           "value": name,
                           "display_value": name,
                           "class": " ".join(cs),
                           "is_visible": not hidden_index})

            if clabels:
                for c, value in enumerate(clabels[r]):
                    cs = []
                    cs.extend(cell_context.get(
                        "col_headings", {}).get(r, {}).get(c, []))
                    es = {
                        "type": "th",
                        "value": value,
                        "display_value": value,
                        "class": " ".join(cs),
                        "is_visible": _is_visible(c, r, col_lengths),
                    }
                    colspan = col_lengths.get((r, c), 0)
                    if colspan > 1:
                        es["attributes"] = [
                            self.format_attr({"key": "colspan", "value": colspan})
                        ]
                    row_es.append(es)
                head.append(row_es)

        if (self.data.index.names and
                com._any_not_none(*self.data.index.names) and
                not hidden_index):
            index_header_row = []

            for c, name in enumerate(self.data.index.names):
                cs = [INDEX_NAME_CLASS,
                      "level{lvl}".format(lvl=c)]
                name = '' if name is None else name
                index_header_row.append({"type": "th", "value": name,
                                         "class": " ".join(cs)})

            index_header_row.extend(
                [{"type": "th",
                  "value": BLANK_VALUE,
                  "class": " ".join([BLANK_CLASS])
                  }] * (len(clabels[0]) - len(hidden_columns)))

            head.append(index_header_row)

        body = []
        for r, idx in enumerate(self.data.index):
            row_es = []
            for c, value in enumerate(rlabels[r]):
                rid = []
                rid.extend(cell_context.get("row_heading", {}).get(r, {}).get(c, []))
                es = {
                    "type": "th",
                    "is_visible": (_is_visible(r, c, idx_lengths) and
                                   not hidden_index),
                    "value": value,
                    "display_value": value,
                    "id": "_".join(rid[1:]),
                    "class": " ".join(rid)
                }
                rowspan = idx_lengths.get((c, r), 0)
                if rowspan > 1:
                    es["attributes"] = [
                        self.format_attr({"key": "rowspan", "value": rowspan})
                    ]
                row_es.append(es)

            for c, col in enumerate(self.data.columns):
                cs = []
                cs.extend(cell_context.get("data", {}).get(r, {}).get(c, []))
                formatter = self._display_funcs[(r, c)]
                value = self.data.iloc[r, c]
                row_dict = {"type": "td",
                            "value": value,
                            "class": " ".join(cs),
                            "display_value": formatter(value),
                            "is_visible": (c not in hidden_columns)}
                # only add an id if the cell has a style
                if (self.cell_ids or
                        not(len(ctx[r, c]) == 1 and ctx[r, c][0] == '')):
                    row_dict["id"] = "_".join(cs[1:])
                row_es.append(row_dict)
                props = []
                for x in ctx[r, c]:
                    # have to handle empty styles like ['']
                    if x.count(":"):
                        props.append(x.split(":"))
                    else:
                        props.append(['', ''])
                cellstyle.append({'props': props,
                                  'selector': "row{row}_col{col}"
                                  .format(row=r, col=c)})
            body.append(row_es)

        table_attr = self.table_attributes
        use_mathjax = get_option("display.html.use_mathjax")
        if not use_mathjax:
            table_attr = table_attr or ''
            if 'class="' in table_attr:
                table_attr = table_attr.replace('class="',
                                                'class="tex2jax_ignore ')
            else:
                table_attr += ' class="tex2jax_ignore"'

        return dict(head=head, cellstyle=cellstyle, body=body, uuid=uuid,
                    precision=precision, table_styles=table_styles,
                    caption=caption, table_attributes=table_attr)


def patch_styler():
    def style(self):
        return Styler(self)

    setattr(DataFrame, 'style', property(style))


def patch():
    patch_pandas()
    patch_styler()
