# -*- coding: utf-8 -*-
"""

Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: ellen.teradata@teradata.com
Secondary Owner:

This file implements the teradataml dataframe.
A teradataml dataframe maps virtually to teradata tables and views.
"""
import sys
import inspect
import sqlalchemy
import numbers
import decimal
import teradataml.context.context as tdmlctx
import pandas as pd

from collections import OrderedDict
from sqlalchemy import Table, Column
from teradataml.dataframe.sql import _MetaExpression
from teradataml.dataframe.sql_interfaces import ColumnExpression

from teradataml.series.series import Series

from teradataml.common.utils import UtilFuncs
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes

from teradataml.common.constants import AEDConstants
from teradataml.common.constants import SourceType, PythonTypes, TeradataConstants, TeradataTypes
from teradataml.dataframe.dataframe_utils import DataFrameUtils as df_utils
from teradataml.dataframe.indexer import _LocationIndexer
from teradataml.common.aed_utils import AedUtils
from teradataml.options.display import display
from teradataml.common.wrapper_utils import AnalyticsWrapperUtils
from teradataml.dataframe.copy_to import copy_to_sql
from teradatasqlalchemy.dialect import preparer, dialect as td_dialect, TeradataTypeCompiler as td_type_compiler

#TODO use logger when available on master branch
#logger = teradatapylog.getLogger()

in_schema = UtilFuncs._in_schema

class DataFrame():
    """
    The teradataml DataFrame enables data manipulation, exploration, and analysis
    on tables, views, and queries on Teradata Vantage.
    """

    def __init__(self, table_name=None, index=True, index_label=None, query=None, materialize=False):
        """
        Constructor for TerdataML DataFrame.

        PARAMETERS:
            table_name:
                Optional Argument.
                The table name or view name in Teradata Vantage referenced by this DataFrame.
                Types: str

            index:
                Optional Argument.
                True if using index column for sorting, otherwise False.
                Default Value: True
                Types: bool

            index_label:
                Optional Argument.
                Column/s used for sorting.
                Types: str

            query:
                Optional Argument.
                SQL query for this Dataframe. Used by class method from_query.
                Types: str

            materialize:
                Optional Argument.
                Whether to materialize DataFrame or not when created.
                Used by class method from_query.

                One should use enable materialization, when the query  passed to from_query(),
                is expected to produce non-deterministic results, when it is executed multiple
                times. Using this option will help user to have deterministic results in the
                resulting teradataml DataFrame.
                Default Value: False (No materialization)
                Types: bool

        EXAMPLES:
            from teradataml.dataframe.dataframe import DataFrame
            df = DataFrame("mytab")
            df = DataFrame("myview")
            df = DataFrame("myview", False)
            df = DataFrame("mytab", True, "Col1, Col2")

        RAISES:
            TeradataMlException - TDMLDF_CREATE_FAIL

        """
        self._table_name = None
        self._query = None
        self._metadata = None
        self._column_names_and_types = None
        self._td_column_names_and_types = None
        self._nodeid = None
        self._metaexpr = None
        self._index = index
        self._index_label = index_label
        self._aed_utils = AedUtils()
        self._source_type = None
        self._orderby = None
        self._undropped_index = None
        # This attribute added to add setter for columns property,
        # it is required when setting columns from groupby
        self._columns = None
        try:
            if table_name is not None:
                self._table_name = UtilFuncs._quote_table_names(table_name)
                self._source_type = SourceType.TABLE
                self._nodeid = self._aed_utils._aed_table(self._table_name)
                self._metadata = df_utils._get_metadata_from_table(self._table_name)
                if self._index_label is None:
                    try:
                        self._index_label = df_utils._get_primary_index_from_table(self._table_name)
                    except Exception as err:
                        # DataFrames generated from views (top node), _index_label is None when PI fetch fails.
                        self._index_label = None

            elif query is not None:
                self._query = query
                self._source_type = SourceType.QUERY

                if materialize:
                    # If user requests to materialize the the query, then we should create a
                    # table instead of view and add the same in the GarbageCollector.
                    temp_table_name = UtilFuncs._generate_temp_table_name(prefix = "_frmqry_t", use_default_database=True, quote=False,
                                                                          table_type=TeradataConstants.TERADATA_TABLE)
                else:
                    temp_table_name = UtilFuncs._generate_temp_table_name(prefix = "_frmqry_v", use_default_database=True, quote=False)

                self._table_name = UtilFuncs._quote_table_names(temp_table_name)
                if materialize:
                    UtilFuncs._create_table(self._table_name, self._query)
                else:
                    UtilFuncs._create_view(self._table_name, self._query)

                self._metadata = df_utils._get_metadata_from_table(self._table_name)
                self._nodeid = self._aed_utils._aed_query(self._query, temp_table_name)

            else:
                if inspect.stack()[1][3] not in ['_from_node', '__init__']:
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_CREATE_FAIL), MessageCodes.TDMLDF_CREATE_FAIL)

            if self._metadata is not None:
                self._column_names_and_types = UtilFuncs._describe_column(self._metadata)
                self._td_column_names_and_types = UtilFuncs._describe_column(self._metadata, to_type = "TD")

                if table_name or query:
                    self._metaexpr = self._get_metaexpr()

            self._loc = _LocationIndexer(self)
            self._iloc = _LocationIndexer(self, integer_indexing=True)

        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_CREATE_FAIL), MessageCodes.TDMLDF_CREATE_FAIL) from err

    @classmethod
    def from_table(cls, table_name, index=True, index_label=None):
        """
        Class method for creating a DataFrame from a table or a view.

        PARAMETERS:
            table_name:
                Required Argument.
                The table name in Teradata Vantage referenced by this DataFrame.
                Types: str

            index:
                Optional Argument.
                True if using index column for sorting otherwise False.
                Default Value: True
                Types: bool

            index_label:
                Optional
                Column/s used for sorting.
                Types: str

        EXAMPLES:
            from teradataml.dataframe.dataframe import DataFrame
            load_example_data("dataframe","sales")
            df = DataFrame.from_table('sales')
            df = DataFrame.from_table("sales", False)
            df = DataFrame.from_table("sales", True, "accounts")

        RETURNS:
            DataFrame

        RAISES:
            TeradataMlException - TDMLDF_CREATE_FAIL

        """
        return cls(table_name, index, index_label)

    @classmethod
    def from_query(cls, query, index=True, index_label=None, materialize=False):
        """
        Class method for creating a DataFrame from a table or view.

        PARAMETERS:
            query:
                Required Argument.
                The Teradata Vantage SQL query referenced by this DataFrame.
                Types: str

            index:
                Optional Argument.
                True if using index column for sorting otherwise False.
                Default Value: True
                Types: bool

            index_label:
                Optional Argument.
                Column/s used for sorting.
                Types: str

            materialize:
                Optional Argument.
                Whether to materialize DataFrame or not when created.

                One should use enable materialization, when the query  passed to from_query(),
                is expected to produce non-deterministic results, when it is executed multiple
                times. Using this option will help user to have deterministic results in the
                resulting teradataml DataFrame.
                Default Value: False (No materialization)
                Types: bool

        EXAMPLES:
            from teradataml.dataframe.dataframe import DataFrame
            load_example_data("dataframe","sales")
            df = DataFrame.from_query("select accounts, Jan, Feb from sales")
            df = DataFrame.from_query("select accounts, Jan, Feb from sales", False)
            df = DataFrame.from_query("select * from sales", True, "accounts")

        RETURNS:
            DataFrame

        RAISES:
            TeradataMlException - TDMLDF_CREATE_FAIL

        """
        return cls(index=index, index_label=index_label, query=query, materialize=materialize)

    @classmethod
    def _from_node(cls, nodeid, metaexpr, index_label=None, undropped_index=None):
        """
        Private class method for creating a DataFrame from a nodeid and parent metadata.

        PARAMETERS:
            nodeid:
                Required Argument.
                Node ID for the DataFrame.

            metaexpr:
                Required Argument.
                Parent metadata (_MetaExpression Object).

            index_label:
                Optional Argument.
                List specifying index column(s) for the DataFrame.

            undropped_index:
                Optional Argument.
                List specifying index column(s) to be retained as columns for printing.

        EXAMPLES:
            from teradataml.dataframe.dataframe import DataFrame
            df = DataFrame._from_node(1234, metaexpr)
            df = DataFrame._from_node(1234, metaexpr, ['col1'], ['col2'])

        RETURNS:
            DataFrame

        RAISES:
            TeradataMlException - TDMLDF_CREATE_FAIL

        """
        df = cls()
        df._nodeid = nodeid
        df._source_type = SourceType.TABLE
        df._get_metadata_from_metaexpr(metaexpr)

        if isinstance(index_label, str):
            index_label = [index_label]

        if index_label is not None and all(elem in [col.name for col in metaexpr.c] for elem in index_label):
            df._index_label = index_label
        elif index_label is not None and all(UtilFuncs._teradata_quote_arg(elem, "\"", False)
                                             in [col.name for col in metaexpr.c] for elem in index_label):
            df._index_label = index_label

        if isinstance(undropped_index, str):
            undropped_index = [undropped_index]

        if undropped_index is not None and all(elem in [col.name for col in metaexpr.c] for elem in undropped_index):
            df._undropped_index = undropped_index
        elif undropped_index is not None and all(UtilFuncs._teradata_quote_arg(elem, "\"", False)
                                             in [col.name for col in metaexpr.c] for elem in undropped_index):
             df._undropped_index = undropped_index

        return df

    def __execute_node_and_set_table_name(self, nodeid, metaexpr = None):
        """
        Private method for executing node and setting _table_name,
        if not set already.

        PARAMETERS:
            nodeid:
                Required Argument.
                nodeid to execute.

            metaexpression:
                Optional Argument.
                Updated _metaexpr to validate

        EXAMPLES:
             __execute_node_and_set_table_name(nodeid)
             __execute_node_and_set_table_name(nodeid, metaexpr)

        """
        if self._table_name is None:
            self._table_name = df_utils._execute_node_return_db_object_name(nodeid, metaexpr)

    def _get_metadata_from_metaexpr(self, metaexpr):
        """
        Private method for setting _metaexpr and retrieving column names and types
        if _metadata is None.

        PARAMETERS:
            metaexpr - Parent meta data (_MetaExpression object).

        RETURNS:
            Python type.

        RAISES:
            TeradataMlException - TDMLDF_CREATE_FAIL

        """
        self._metaexpr = metaexpr
        #if there is no metadata from HELP COLUMN then use the metadata from metaexpr
        if self._metadata is None:
            self._column_names_and_types = []
            self._td_column_names_and_types = []
            for col in metaexpr.c:
                if isinstance(col.type, sqlalchemy.sql.sqltypes.NullType):
                    tdtype = TeradataTypes.TD_NULL_TYPE
                else:
                    tdtype = "{}".format(col.type)

                self._column_names_and_types.append((col.name, UtilFuncs._teradata_type_to_python_type(col.type)))
                self._td_column_names_and_types.append((col.name, tdtype))

    def _get_metaexpr(self):
        """
        Private method that returns a TableExpression object for this dataframe.

        RETURNS:
            TableExpression object

        EXAMPLES:
            table_meta = self._get_metaexpr()

            # you can access the columns with the 'c' attribute
            table_meta.c

        """
        eng = tdmlctx.get_context()
        meta = sqlalchemy.MetaData(eng)
        db_schema = UtilFuncs._extract_db_name(self._table_name)
        db_table_name = UtilFuncs._extract_table_name(self._table_name)

        #Remove quotes because sqlalchemy.Table() does not like the quotes.
        if db_schema is not None:
            db_schema = db_schema[1:-1]
        db_table_name = db_table_name[1:-1]

        t = sqlalchemy.Table(db_table_name, meta, schema=db_schema, autoload=True, autoload_with=eng)
        return _MetaExpression(t, column_order = self.columns)


    def __getattr__(self, name):
        """
        Returns an attribute of the DataFrame

        PARAMETERS:
          name: the name of the attribute

        RETURNS:
          Return the value of the named attribute of object (if found).

        EXAMPLES:
          df = DataFrame('table')

          # you can access a column from the DataFrame
          df.c1

        RAISES:
          Attribute Error when the named attribute is not found
        """

        # look in the underlying _MetaExpression for columns
        for col in self._metaexpr.c:
            if col.name == name:
                return col

        raise AttributeError("'DataFrame' object has no attribute %s" % name)

    def __getitem__(self, key):
        """
        Return a column from the DataFrame or filter the DataFrame using an expression
        The following operators are supported:
          comparison: ==, !=, <, <=, >, >=
          boolean: & (and), | (or), ~ (not), ^ (xor)

        Operands can be python literals and instances of ColumnExpressions from the DataFrame

        EXAMPLES:
          df = DataFrame('table')

          # filter the DataFrame df
          df[df.c1 > df.c2]

          df[df.c1 >= 1]

          df[df.c1 == 'string']

          df[1 != df.c2]

          df[~(1 < df.c2)]

          df[(df.c1 > 0) & (df.c2 > df.c1)]

          # retrieve column c1 from df
          df['c1']

        PARAMETERS:
          key: A column name as a string or filter expression (ColumnExpression)

        RETURNS:
          DataFrame or ColumnExpression instance

        RAISES:
          1. KeyError   - If key is not found
          2. ValueError - When columns of different dataframes are given in ColumnExpression.
        """

        try:
            # get the ColumnExpression from the _MetaExpression
            if isinstance(key, str):
                return self.__getattr__(key)

            # apply the filter expression
            if isinstance(key, ColumnExpression):

                if self._metaexpr is None:
                    msg = Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR)
                    raise TeradataMlException(msg, MessageCodes.TDMLDF_INFO_ERROR)

                if key.get_flag_has_multiple_dataframes():
                    raise ValueError("Combining Columns from different dataframes is unsupported "
                                     "for filter [] operation.")

                clause_exp = key.compile()
                new_nodeid = self._aed_utils._aed_filter(self._nodeid, clause_exp)

                return DataFrame._from_node(new_nodeid, self._metaexpr, self._index_label)

        except TeradataMlException:
            raise

        except ValueError:
             raise

        except Exception as err:
            errcode = MessageCodes.TDMLDF_INFO_ERROR
            msg = Messages.get_message(errcode)
            raise TeradataMlException(msg, errcode) from err

        raise KeyError('Unable to find key: %s' % str(key))

    def keys(self):
        """
        RETURNS:
            a list containing the column names

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')
            >>> df.keys()
            ['accounts', 'Feb', 'Jan', 'Mar', 'Apr', 'datetime']
        """
        if self._column_names_and_types is not None:
            return [i[0] for i in self._column_names_and_types]
        else:
            return []

    @property
    def columns(self):
        """
        RETURNS:
            a list containing the column names

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')
            >>> df.columns
            ['accounts', 'Feb', 'Jan', 'Mar', 'Apr', 'datetime']
        """
        return self.keys()

    @property
    def loc(self):
        """
        Access a group of rows and columns by label(s) or a boolean array.

        VALID INPUTS:

            - A single label, e.g. ``5`` or ``'a'``, (note that ``5`` is
            interpreted as a label of the index, it is not interpreted as an
            integer position along the index).

            - A list or array of column or index labels, e.g. ``['a', 'b', 'c']``.

            - A slice object with labels, e.g. ``'a':'f'``.
            Note that unlike the usual python slices where the stop index is not included, both the
                start and the stop are included

            - A conditional expression for row access.

            - A boolean array of the same length as the column axis for column access.

        RETURNS:
            teradataml DataFrame

        RAISE:
            TeradataMlException

        EXAMPLES
        --------
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame('sales')
            >>> df
                        Feb   Jan   Mar   Apr    datetime
            accounts
            Blue Inc     90.0    50    95   101  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            Jones LLC   200.0   150   140   180  04/01/2017
            Yellow Inc   90.0  None  None  None  04/01/2017
            Orange Inc  210.0  None  None   250  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017

            # Retrieve row using a single label.
            >>> df.loc['Blue Inc']
                    Feb Jan Mar  Apr    datetime
            accounts
            Blue Inc  90.0  50  95  101  04/01/2017

            # List of labels. Note using ``[[]]``
            >>> df.loc[['Blue Inc', 'Jones LLC']]
                        Feb  Jan  Mar  Apr    datetime
            accounts
            Blue Inc    90.0   50   95  101  04/01/2017
            Jones LLC  200.0  150  140  180  04/01/2017

            # Single label for row and column (index)
            >>> df.loc['Yellow Inc', 'accounts']
            Empty DataFrame
            Columns: []
            Index: [Yellow Inc]

            # Single label for row and column
            >>> df.loc['Yellow Inc', 'Feb']
                Feb
            0  90.0

            # Single label for row and column access using a tuple
            >>> df.loc[('Yellow Inc', 'Feb')]
                Feb
            0  90.0

            # Slice with labels for row and single label for column. As mentioned
            # above, note that both the start and stop of the slice are included.
            >>> df.loc['Jones LLC':'Red Inc', 'accounts']
            Empty DataFrame
            Columns: []
            Index: [Orange Inc, Jones LLC, Red Inc]

            # Slice with labels for row and single label for column. As mentioned
            # above, note that both the start and stop of the slice are included.
            >>> df.loc['Jones LLC':'Red Inc', 'Jan']
                Jan
            0  None
            1   150
            2   150

            # Slice with labels for row and labels for column. As mentioned
            # above, note that both the start and stop of the slice are included.
            >>> df.loc['Jones LLC':'Red Inc', 'accounts':'Apr']
                        Mar   Jan    Feb   Apr
            accounts
            Orange Inc  None  None  210.0   250
            Red Inc      140   150  200.0  None
            Jones LLC    140   150  200.0   180

            # Empty slice for row and labels for column.
            >>> df.loc[:, :]
                        Feb   Jan   Mar    datetime   Apr
            accounts
            Jones LLC   200.0   150   140  04/01/2017   180
            Blue Inc     90.0    50    95  04/01/2017   101
            Yellow Inc   90.0  None  None  04/01/2017  None
            Orange Inc  210.0  None  None  04/01/2017   250
            Alpha Co    210.0   200   215  04/01/2017   250
            Red Inc     200.0   150   140  04/01/2017  None

            # Conditional expression
            >>> df.loc[df['Feb'] > 90]
                        Feb   Jan   Mar   Apr    datetime
            accounts
            Jones LLC   200.0   150   140   180  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            Orange Inc  210.0  None  None   250  04/01/2017

            # Conditional expression with column labels specified
            >>> df.loc[df['Feb'] > 90, ['accounts', 'Jan']]
                        Jan
            accounts
            Jones LLC    150
            Red Inc      150
            Alpha Co     200
            Orange Inc  None

            # Conditional expression with multiple column labels specified
            >>> df.loc[df['accounts'] == 'Jones LLC', ['accounts', 'Jan', 'Feb']]
                    Jan    Feb
            accounts
            Jones LLC  150  200.0

            # Conditional expression and slice with column labels specified
            >>> df.loc[df['accounts'] == 'Jones LLC', 'accounts':'Mar']
                    Mar  Jan    Feb
            accounts
            Jones LLC  140  150  200.0

            # Conditional expression and boolean array for column access
            >>> df.loc[df['Feb'] > 90, [True, True, False, False, True, True]]
                      Feb   Apr    datetime
            accounts
            Alpha Co    210.0   250  04/01/2017
            Jones LLC   200.0   180  04/01/2017
            Red Inc     200.0  None  04/01/2017
            Orange Inc  210.0   250  04/01/2017
            >>>
        """
        return self._loc

    @property
    def iloc(self):
        """
        Access a group of rows and columns by integer values or a boolean array.
        VALID INPUTS:
            - A single integer values, e.g. 5.

            - A list or array of integer values, e.g. ``[1, 2, 3]``.

            - A slice object with integer values, e.g. ``1:6``.
              Note: The stop value is excluded.

            - A boolean array of the same length as the column axis for column access,

            Note: For integer indexing on row access, the integer index values are
            applied to a sorted teradataml DataFrame on the index column or the first column if
            there is no index column.

        RETURNS:
            teradataml DataFrame

        RAISE:
            TeradataMlException

        EXAMPLES
        --------
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame('sales')
            >>> df
                        Feb   Jan   Mar   Apr    datetime
            accounts
            Blue Inc     90.0    50    95   101  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            Jones LLC   200.0   150   140   180  04/01/2017
            Yellow Inc   90.0  None  None  None  04/01/2017
            Orange Inc  210.0  None  None   250  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017

            # Retrieve row using a single integer.
            >>> df.iloc[1]
                    Feb Jan Mar  Apr    datetime
            accounts
            Blue Inc  90.0  50  95  101  04/01/2017

            # List of integers. Note using ``[[]]``
            >>> df.iloc[[1, 2]]
                        Feb  Jan  Mar  Apr    datetime
            accounts
            Blue Inc    90.0   50   95  101  04/01/2017
            Jones LLC  200.0  150  140  180  04/01/2017

            # Single integer for row and column
            >>> df.iloc[5, 0]
            Empty DataFrame
            Columns: []
            Index: [Yellow Inc]

            # Single integer for row and column
            >>> df.iloc[5, 1]
                Feb
            0  90.0

            # Single integer for row and column access using a tuple
            >>> df.iloc[(5, 1)]
                Feb
            0  90.0

            # Slice for row and single integer for column access. As mentioned
            # above, note the stop for the slice is excluded.
            >>> df.iloc[2:5, 0]
            Empty DataFrame
            Columns: []
            Index: [Orange Inc, Jones LLC, Red Inc]

            # Slice for row and a single integer for column access. As mentioned
            # above, note the stop for the slice is excluded.
            >>> df.iloc[2:5, 2]
                Jan
            0  None
            1   150
            2   150

            # Slice for row and column access. As mentioned
            # above, note the stop for the slice is excluded.
            >>> df.iloc[2:5, 0:5]
                        Mar   Jan    Feb   Apr
            accounts
            Orange Inc  None  None  210.0   250
            Red Inc      140   150  200.0  None
            Jones LLC    140   150  200.0   180

            # Empty slice for row and column access.
            >>> df.iloc[:, :]
                          Feb   Jan   Mar   Apr    datetime
            accounts
            Blue Inc     90.0    50    95   101  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            Jones LLC   200.0   150   140   180  04/01/2017
            Yellow Inc   90.0  None  None  None  04/01/2017
            Orange Inc  210.0  None  None   250  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017

            # List of integers and boolean array for column access
            >>> df.iloc[[0, 2, 3, 4], [True, True, False, False, True, True]]
                          Feb   Apr    datetime
            accounts
            Orange Inc  210.0   250  04/01/2017
            Red Inc     200.0  None  04/01/2017
            Jones LLC   200.0   180  04/01/2017
            Alpha Co    210.0   250  04/01/2017
        """
        return self._iloc

    @columns.setter
    def columns(self, columns):
        """
        Assigns self._columns for the passed columns

        PARAMETERS:
            columns

        EXAMPLES:
            df.columns

        """
        self._columns = columns

    @property
    def dtypes(self):
        """
        Returns a MetaData containing the column names and types.

        PARAMETERS:

        RETURNS:
            MetaData containing the column names and Python types

        RAISES:

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')
            >>> print(df.dtypes)
            accounts              str
            Feb                 float
            Jan                   int
            Mar                   int
            Apr                   int
            datetime    datetime.date
            >>>

        """
        return MetaData(self._column_names_and_types)

    def info(self, verbose=True, buf=None, max_cols=None, null_counts=None):
        """
        DESCRIPTION:
            Print a summary of the DataFrame.

        PARAMETERS:
            verbose:
                Optional Argument.
                Print full summary if True. Print short summary if False.
                Default Value: True
                Types: bool

            buf:
                Optional Argument.
                The writable buffer to send the output to. By default, the output is
                sent to sys.stdout.

            max_cols:
                Optional Argument.
                The maximum number of columns allowed for printing the full summary.
                Types: int

            null_counts:
                Optional Argument.
                Whether to show the non-null counts.
                Display the counts if True, otherwise do not display the counts.
                Types: bool

        RETURNS:

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')
            >>> df.info()
            <class 'teradataml.dataframe.dataframe.DataFrame'>
            Data columns (total 6 columns):
            accounts              str
            Feb                 float
            Jan                   int
            Mar                   int
            Apr                   int
            datetime    datetime.date
            dtypes: datetime.date(1), float(1), str(1), int(3)
            >>>
            >>> df.info(null_counts=True)
            <class 'teradataml.dataframe.dataframe.DataFrame'>
            Data columns (total 6 columns):
            accounts    6 non-null str
            Feb         6 non-null float
            Jan         4 non-null int
            Mar         4 non-null int
            Apr         4 non-null int
            datetime    6 non-null datetime.date
            dtypes: datetime.date(1), float(1), str(1), int(3)
            >>>
            >>> df.info(verbose=False)
            <class 'teradataml.dataframe.dataframe.DataFrame'>
            Data columns (total 6 columns):
            dtypes: datetime.date(1), float(1), str(1), int(3)
            >>>
        """
        try:
            output_buf = sys.stdout
            if buf is not None:
                output_buf = buf

            num_columns = len(self._column_names_and_types)
            suffix = ""
            if num_columns > 1:
                suffix = "s"

            col_names = [i[0] for i in self._column_names_and_types]
            col_types = [i[1] for i in self._column_names_and_types]

            #print the class name for self.
            print(str(type(self)), file=output_buf)
            #print the total number of columns
            print("Data columns (total {0} column{1}):".format(num_columns, suffix), file=output_buf)

            #if max_cols and the number of columns exceeds max_cols, do not print the column names and types
            if max_cols is not None and len(col_names) > max_cols:
                verbose = False

            #if verbose, print the column names and types.
            if verbose:
                #if null_counts, print the number of non-null values for each column if this is not an empty dataframe.
                if null_counts is not None and null_counts and self._table_name is not None:
                    null_count_str = UtilFuncs._get_non_null_counts(col_names, self._table_name)
                    zipped = zip(col_names, col_types, null_count_str)
                    column_names_and_types = list(zipped)
                    null_count = True
                #else just print the column names and types
                else:
                    column_names_and_types = self._column_names_and_types
                    null_count = False
                print("{}".format(df_utils._get_pprint_dtypes(column_names_and_types, null_count)), file=output_buf)

            #print the dtypes and count of each dtypes
            unique_types = list(set(col_types))
            for i in range(0, len(unique_types)):
                unique_types[i] = "{0}({1})".format(unique_types[i], col_types.count(unique_types[i]))
            print("dtypes: {}".format(", ".join(unique_types)), file=output_buf)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def head(self, n=display.max_rows):
        """
        DESCRIPTION:
            Print the first n rows of the sorted teradataml DataFrame.
            Note: The DataFrame is sorted on the index column or the first column if
            there is no index column. The column type must support sorting.
            Unsupported types: ['BLOB', 'CLOB', 'ARRAY', 'VARRAY']

        PARAMETERS:
            n:
                Optional argument.
                Specifies the number of rows to select.
                Default Value: 10.
                Type: int

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame.from_table('admissions_train')
            >>> df
               masters   gpa     stats programming admitted
            id
            15     yes  4.00  Advanced    Advanced        1
            7      yes  2.33    Novice      Novice        1
            22     yes  3.46    Novice    Beginner        0
            17      no  3.83  Advanced    Advanced        1
            13      no  4.00  Advanced      Novice        1
            38     yes  2.65  Advanced    Beginner        1
            26     yes  3.57  Advanced    Advanced        1
            5       no  3.44    Novice      Novice        0
            34     yes  3.85  Advanced    Beginner        0
            40     yes  3.95    Novice    Beginner        0
            
            >>> df.head()
               masters   gpa     stats programming admitted
            id
            3       no  3.70    Novice    Beginner        1
            5       no  3.44    Novice      Novice        0
            6      yes  3.50  Beginner    Advanced        1
            7      yes  2.33    Novice      Novice        1
            9       no  3.82  Advanced    Advanced        1
            10      no  3.71  Advanced    Advanced        1
            8       no  3.60  Beginner    Advanced        1
            4      yes  3.50  Beginner      Novice        1
            2      yes  3.76  Beginner    Beginner        0
            1      yes  3.95  Beginner    Beginner        0
            
            >>> df.head(15)
               masters   gpa     stats programming admitted
            id
            3       no  3.70    Novice    Beginner        1
            5       no  3.44    Novice      Novice        0
            6      yes  3.50  Beginner    Advanced        1
            7      yes  2.33    Novice      Novice        1
            9       no  3.82  Advanced    Advanced        1
            10      no  3.71  Advanced    Advanced        1
            11      no  3.13  Advanced    Advanced        1
            12      no  3.65    Novice      Novice        1
            13      no  4.00  Advanced      Novice        1
            14     yes  3.45  Advanced    Advanced        0
            15     yes  4.00  Advanced    Advanced        1
            8       no  3.60  Beginner    Advanced        1
            4      yes  3.50  Beginner      Novice        1
            2      yes  3.76  Beginner    Beginner        0
            1      yes  3.95  Beginner    Beginner        0
            
            >>> df.head(5)
               masters   gpa     stats programming admitted
            id
            3       no  3.70    Novice    Beginner        1
            5       no  3.44    Novice      Novice        0
            4      yes  3.50  Beginner      Novice        1
            2      yes  3.76  Beginner    Beginner        0
            1      yes  3.95  Beginner    Beginner        0
        """
        try:
            if not isinstance(n, numbers.Integral) or n <= 0:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_POSITIVE_INT).format("n"), MessageCodes.TDMLDF_POSITIVE_INT)
            if self._metaexpr is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR)
            sort_col = self._get_sort_col()
            return df_utils._get_sorted_nrow(self, n, sort_col[0], asc=True)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def tail(self, n=display.max_rows):
        """
        DESCRIPTION:
            Print the last n rows of the sorted teradataml DataFrame.
            Note: The Dataframe is sorted on the index column or the first column if
            there is no index column. The column type must support sorting.
            Unsupported types: ['BLOB', 'CLOB', 'ARRAY', 'VARRAY']

        PARAMETERS:
            n:
                Optional argument.
                Specifies the number of rows to select.
                Default Value: 10.
                Type: int

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame.from_table('admissions_train')
            >>> df
               masters   gpa     stats programming admitted
            id
            15     yes  4.00  Advanced    Advanced        1
            7      yes  2.33    Novice      Novice        1
            22     yes  3.46    Novice    Beginner        0
            17      no  3.83  Advanced    Advanced        1
            13      no  4.00  Advanced      Novice        1
            38     yes  2.65  Advanced    Beginner        1
            26     yes  3.57  Advanced    Advanced        1
            5       no  3.44    Novice      Novice        0
            34     yes  3.85  Advanced    Beginner        0
            40     yes  3.95    Novice    Beginner        0

            >>> df.tail()
               masters   gpa     stats programming admitted
            id
            38     yes  2.65  Advanced    Beginner        1
            36      no  3.00  Advanced      Novice        0
            35      no  3.68    Novice    Beginner        1
            34     yes  3.85  Advanced    Beginner        0
            32     yes  3.46  Advanced    Beginner        0
            31     yes  3.50  Advanced    Beginner        1
            33      no  3.55    Novice      Novice        1
            37      no  3.52    Novice      Novice        1
            39     yes  3.75  Advanced    Beginner        0
            40     yes  3.95    Novice    Beginner        0

            >>> df.tail(3)
               masters   gpa     stats programming admitted
            id
            38     yes  2.65  Advanced    Beginner        1
            39     yes  3.75  Advanced    Beginner        0
            40     yes  3.95    Novice    Beginner        0

            >>> df.tail(15)
               masters   gpa     stats programming admitted
            id
            38     yes  2.65  Advanced    Beginner        1
            36      no  3.00  Advanced      Novice        0
            35      no  3.68    Novice    Beginner        1
            34     yes  3.85  Advanced    Beginner        0
            32     yes  3.46  Advanced    Beginner        0
            31     yes  3.50  Advanced    Beginner        1
            30     yes  3.79  Advanced      Novice        0
            29     yes  4.00    Novice    Beginner        0
            28      no  3.93  Advanced    Advanced        1
            27     yes  3.96  Advanced    Advanced        0
            26     yes  3.57  Advanced    Advanced        1
            33      no  3.55    Novice      Novice        1
            37      no  3.52    Novice      Novice        1
            39     yes  3.75  Advanced    Beginner        0
            40     yes  3.95    Novice    Beginner        0
        """
        try:
            if not isinstance(n, numbers.Integral) or n <= 0:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_POSITIVE_INT).format("n"), MessageCodes.TDMLDF_POSITIVE_INT)
            if self._metaexpr is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR)

            sort_col = self._get_sort_col()
            return df_utils._get_sorted_nrow(self, n, sort_col[0], asc=False)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def _get_axis(self, axis):
        """
        Private method to retrieve axis value, 0 for index or 1 for columns

        PARAMETERS:
            axis - 0 or 'index' for index labels
                   1 or 'columns' for column labels

        RETURNS:
            0 or 1

        RAISE:
            TeradataMlException

        EXAMPLES:
            a = self._get_axis(0)
            a = self._get_axis(1)
            a = self._get_axis('index')
            a = self._get_axis('columns')
        """
        if isinstance(axis, str):
            if axis == "index":
                return 0
            elif axis == "columns":
                return 1
            else:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INVALID_DROP_AXIS), MessageCodes.TDMLDF_INVALID_DROP_AXIS)
        elif isinstance(axis, numbers.Integral):
            if axis in [0, 1]:
                return axis
            else:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INVALID_DROP_AXIS), MessageCodes.TDMLDF_INVALID_DROP_AXIS)
        else:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INVALID_DROP_AXIS), MessageCodes.TDMLDF_INVALID_DROP_AXIS)

    def _get_sort_col(self):
        """
        Private method to retrieve sort column.
        If _index_labels is not None, return first column and type in _index_labels.
        Otherwise return first column and type in _metadata.

        PARAMETERS:

        RETURNS:
            A tuple containing the column name and type in _index_labels or first column in _metadata.

        RAISE:

        EXAMPLES:
            sort_col = self._get_sort_col()
        """
        unsupported_types = ['BLOB', 'CLOB', 'ARRAY', 'VARRAY']

        if self._index_label is not None:
            if isinstance(self._index_label, list):
                col_name = self._index_label[0]
            else:
                col_name = self._index_label
        else: #Use the first column from metadata
            col_name = self.columns[0]

        col_type = PythonTypes.PY_NULL_TYPE
        for name, py_type in self._column_names_and_types:
            if col_name == name:
                col_type = py_type

        if col_type == PythonTypes.PY_NULL_TYPE:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR)

        sort_col_sqlalchemy_type = (self._metaexpr.t.c[col_name].type)
        # convert types to string from sqlalchemy type for the columns entered for sort
        sort_col_type = repr(sort_col_sqlalchemy_type).split("(")[0]
        if sort_col_type in unsupported_types:
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, sort_col_type, "ANY, except following {}".format(unsupported_types)), MessageCodes.UNSUPPORTED_DATATYPE)

        return (col_name, col_type)

    def drop(self, labels=None, axis=0, columns=None):
        """
        DESCRIPTION:
            Drop specified labels from rows or columns.

            Remove rows or columns by specifying label names and corresponding
            axis, or by specifying the index or column names directly.

        PARAMETERS:
            labels:
                Optional Argument.
                Single label or list-like. Can be Index or column labels to drop depending on axis.
                Types: str OR list of Strings (str)

            axis:
                Optional Argument.
                0 or 'index' for index labels
                1 or 'columns' for column labels
                Default Values: 0
                Permitted Values: 0, 1, 'index', 'columns'
                Types: int OR str

            columns:
                Optional Argument.
                Single label or list-like. This is an alternative to specifying axis=1 with labels.
                Cannot specify both labels and columns.
                Types: str OR list of Strings (str)

        RETURNS:
            teradataml DataFrame

        RAISE:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame('admissions_train')
            >>> df
               masters   gpa     stats programming admitted
            id
            5       no  3.44    Novice      Novice        0
            7      yes  2.33    Novice      Novice        1
            22     yes  3.46    Novice    Beginner        0
            17      no  3.83  Advanced    Advanced        1
            13      no  4.00  Advanced      Novice        1
            19     yes  1.98  Advanced    Advanced        0
            36      no  3.00  Advanced      Novice        0
            15     yes  4.00  Advanced    Advanced        1
            34     yes  3.85  Advanced    Beginner        0
            40     yes  3.95    Novice    Beginner        0

            # Drop columns
            >>> df.drop(['stats', 'admitted'], axis=1)
               programming masters   gpa
            id
            5       Novice      no  3.44
            34    Beginner     yes  3.85
            13      Novice      no  4.00
            40    Beginner     yes  3.95
            22    Beginner     yes  3.46
            19    Advanced     yes  1.98
            36      Novice      no  3.00
            15    Advanced     yes  4.00
            7       Novice     yes  2.33
            17    Advanced      no  3.83

            >>> df.drop(columns=['stats', 'admitted'])
               programming masters   gpa
            id
            5       Novice      no  3.44
            34    Beginner     yes  3.85
            13      Novice      no  4.00
            19    Advanced     yes  1.98
            15    Advanced     yes  4.00
            40    Beginner     yes  3.95
            7       Novice     yes  2.33
            22    Beginner     yes  3.46
            36      Novice      no  3.00
            17    Advanced      no  3.83

            # Drop a row by index
            >>> df1 = df[df.gpa == 4.00]
            >>> df1
               masters  gpa     stats programming admitted
            id
            13      no  4.0  Advanced      Novice        1
            29     yes  4.0    Novice    Beginner        0
            15     yes  4.0  Advanced    Advanced        1
            >>> df1.drop([13,15], axis=0)
               masters  gpa   stats programming admitted
            id
            29     yes  4.0  Novice    Beginner        0
            >>>
        """
        try:
            column_labels = None
            index_labels = None
            if labels is not None and columns is not None:
                #Cannot specify both 'labels' and 'columns'
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ARGS), MessageCodes.TDMLDF_DROP_ARGS)
            elif labels is None and columns is None:
                #Need to specify at least one of 'labels' or 'columns'
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ARGS), MessageCodes.TDMLDF_DROP_ARGS)

            if labels is not None:
                if self._get_axis(axis) == 0:
                    index_labels = labels
                else:
                    column_labels = labels
            else: #columns is not None
                column_labels = columns

            if index_labels is not None:
                sort_col = self._get_sort_col()
                df_utils._validate_sort_col_type(sort_col[1], index_labels)

                if isinstance(index_labels, list):
                    if len(index_labels) == 0:
                        raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ARGS), MessageCodes.TDMLDF_DROP_ARGS)

                    if sort_col[1] == PythonTypes.PY_STRING_TYPE:
                        index_labels = ["'{}'".format(x) for x in index_labels]
                    index_expr = ",".join(map(str, (index_labels)))
                else:
                    if sort_col[1] == PythonTypes.PY_STRING_TYPE:
                        index_expr = "'{}'".format(index_labels)
                    else:
                        index_expr = index_labels

                filter_expr = "{0} not in ({1})".format(sort_col[0], index_expr)
                new_nodeid= self._aed_utils._aed_filter(self._nodeid, filter_expr)
                return DataFrame._from_node(new_nodeid, self._metaexpr, self._index_label)
            else: #column labels
                select_cols = []
                cols = [x.name for x in self._metaexpr.columns]
                if isinstance(column_labels, list):
                    if len(column_labels) == 0:
                        raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ARGS), MessageCodes.TDMLDF_DROP_ARGS)

                    if not all(isinstance(n, str) for n in column_labels):
                        raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES), MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES)
                    drop_cols = [x for x in column_labels]
                elif isinstance(column_labels, (tuple, dict)):
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ARGS), MessageCodes.TDMLDF_DROP_ARGS)
                else:
                    if not isinstance(column_labels, str):
                        raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES), MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES)
                    drop_cols = [column_labels]

                for drop_name in drop_cols:
                    if drop_name not in cols:
                        msg = Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL).format(drop_name, cols)
                        raise TeradataMlException(msg, MessageCodes.TDMLDF_DROP_INVALID_COL)

                for colname in cols:
                    if colname not in drop_cols:
                        select_cols.append(colname)
                if len(select_cols) > 0:
                    return self.select(select_cols)
                else: # no columns selected
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ALL_COLS), MessageCodes.TDMLDF_DROP_ALL_COLS)

        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def dropna(self, how='any', thresh=None, subset=None):
        """
        DESCRIPTION:
            Removes rows with null values.

        PARAMETERS:
            how:
                Optional Argument.
                Specifies how rows are removed.
                'any' removes rows with at least one null value.
                'all' removes rows with all null values.
                Default Value: 'any'
                Permitted Values: 'any' or 'all'
                Types: str

            thresh:
                Optional Argument.
                Specifies the minimum number of non null values in a row to include.
                Types: int

            subset:
                Optional Argument.
                Specifies list of column names to include, in array-like format.
                Types: str OR list of Strings (str)

        RETURNS:
            teradataml DataFrame

        RAISE:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame('sales')
            >>> df
                          Feb   Jan   Mar   Apr    datetime
            accounts
            Jones LLC   200.0   150   140   180  04/01/2017
            Yellow Inc   90.0  None  None  None  04/01/2017
            Orange Inc  210.0  None  None   250  04/01/2017
            Blue Inc     90.0    50    95   101  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017

            # Drop the rows where at least one element is null.
            >>> df.dropna()
                         Feb  Jan  Mar  Apr    datetime
            accounts
            Blue Inc    90.0   50   95  101  04/01/2017
            Jones LLC  200.0  150  140  180  04/01/2017
            Alpha Co   210.0  200  215  250  04/01/2017

            # Drop the rows where all elements are nulls for columns 'Jan' and 'Mar'.
            >>> df.dropna(how='all', subset=['Jan','Mar'])
                         Feb  Jan  Mar   Apr    datetime
            accounts
            Alpha Co   210.0  200  215   250  04/01/2017
            Jones LLC  200.0  150  140   180  04/01/2017
            Red Inc    200.0  150  140  None  04/01/2017
            Blue Inc    90.0   50   95   101  04/01/2017

            # Keep only the rows with at least 4 non null values.
            >>> df.dropna(thresh=4)
                          Feb   Jan   Mar   Apr    datetime
            accounts
            Jones LLC   200.0   150   140   180  04/01/2017
            Blue Inc     90.0    50    95   101  04/01/2017
            Orange Inc  210.0  None  None   250  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017

            # Keep only the rows with at least 5 non null values.
            >>> df.dropna(thresh=5)
                         Feb  Jan  Mar   Apr    datetime
            accounts
            Alpha Co   210.0  200  215   250  04/01/2017
            Jones LLC  200.0  150  140   180  04/01/2017
            Blue Inc    90.0   50   95   101  04/01/2017
            Red Inc    200.0  150  140  None  04/01/2017
        """
        try:
            col_names = [item.lower() for item in self.keys()]

            if not isinstance(how, str) or how not in ['any', 'all']:
                msg = Messages.get_message(MessageCodes.INVALID_ARG_VALUE, how, "how", "'any' or 'all'")
                raise TeradataMlException(msg, MessageCodes.INVALID_ARG_VALUE)

            #if there is a thresh value, the thresh value must be a positive number greater than 0
            if thresh is not None and (not isinstance(thresh, numbers.Integral) or thresh <= 0):
                msg = Messages.get_message(MessageCodes.TDMLDF_POSITIVE_INT).format('thresh')
                raise TeradataMlException(msg, MessageCodes.TDMLDF_POSITIVE_INT)

            #if there is a subset value, the subset value must be a list containing at least one element.
            if subset is not None and (not isinstance(subset, list) or len(subset) == 0):
                msg = Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "subset", "list of column names")
                raise TeradataMlException(msg, MessageCodes.UNSUPPORTED_DATATYPE)

            if subset is not None:
                if not all(isinstance(n, str) for n in subset):
                    msg = Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "subset", "list of column names")
                    raise TeradataMlException(msg, MessageCodes.UNSUPPORTED_DATATYPE)
                for n in subset:
                    if n.lower() not in col_names:
                        msg = Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL).format(n, self.keys())
                        raise TeradataMlException(msg, MessageCodes.TDMLDF_DROP_INVALID_COL)
                col_filters = subset
            else:
                col_filters = col_names

            col_filters_decode = ["decode(\"{}\", null, 0, 1)".format(col_name) for col_name in col_filters]
            fmt_filter = " + ".join(col_filters_decode)

            if thresh is not None:
                filter_expr = "{0} >= {1}".format(fmt_filter, thresh)
            elif how == 'any':
                filter_expr = "{0} = {1}".format(fmt_filter, len(col_filters))
            else: #how == 'all'
                filter_expr = "{0} > 0".format(fmt_filter)

            new_nodeid= self._aed_utils._aed_filter(self._nodeid, filter_expr)
            return DataFrame._from_node(new_nodeid, self._metaexpr, self._index_label)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def sort(self, columns, ascending=True):
        """
        DESCRIPTION:
            Get Sorted data by one or more columns in either ascending or descending order for a Dataframe.
            Unsupported column types for sorting: ['BLOB', 'CLOB', 'ARRAY', 'VARRAY']

        PARAMETERS:
            columns:
                Required Argument.
                Column names as a string or a list of strings to sort on.
                Types: str OR list of Strings (str)

            ascending:
                Optional Argument.
                Order ASC or DESC to be applied for each column.
                True for ascending order and False for descending order.
                Default value: True
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame('admissions_train')
            >>> df
               masters   gpa     stats programming admitted
            id
            22     yes  3.46    Novice    Beginner        0
            37      no  3.52    Novice      Novice        1
            35      no  3.68    Novice    Beginner        1
            12      no  3.65    Novice      Novice        1
            4      yes  3.50  Beginner      Novice        1
            38     yes  2.65  Advanced    Beginner        1
            27     yes  3.96  Advanced    Advanced        0
            39     yes  3.75  Advanced    Beginner        0
            7      yes  2.33    Novice      Novice        1
            40     yes  3.95    Novice    Beginner        0
            >>> df.sort("id")
               masters   gpa     stats programming admitted
            id
            1      yes  3.95  Beginner    Beginner        0
            2      yes  3.76  Beginner    Beginner        0
            3       no  3.70    Novice    Beginner        1
            4      yes  3.50  Beginner      Novice        1
            5       no  3.44    Novice      Novice        0
            6      yes  3.50  Beginner    Advanced        1
            7      yes  2.33    Novice      Novice        1
            8       no  3.60  Beginner    Advanced        1
            9       no  3.82  Advanced    Advanced        1
            10      no  3.71  Advanced    Advanced        1
            >>> df.sort(["id"])
               masters   gpa     stats programming admitted
            id
            1      yes  3.95  Beginner    Beginner        0
            2      yes  3.76  Beginner    Beginner        0
            3       no  3.70    Novice    Beginner        1
            4      yes  3.50  Beginner      Novice        1
            5       no  3.44    Novice      Novice        0
            6      yes  3.50  Beginner    Advanced        1
            7      yes  2.33    Novice      Novice        1
            8       no  3.60  Beginner    Advanced        1
            9       no  3.82  Advanced    Advanced        1
            10      no  3.71  Advanced    Advanced        1
            >>> df.sort(["masters","gpa"])
               masters   gpa     stats programming admitted
            id
            24      no  1.87  Advanced      Novice        1
            36      no  3.00  Advanced      Novice        0
            11      no  3.13  Advanced    Advanced        1
            5       no  3.44    Novice      Novice        0
            37      no  3.52    Novice      Novice        1
            33      no  3.55    Novice      Novice        1
            8       no  3.60  Beginner    Advanced        1
            12      no  3.65    Novice      Novice        1
            35      no  3.68    Novice    Beginner        1
            16      no  3.70  Advanced    Advanced        1
            >>> # In next example, sort dataframe with masters column in Ascending ('True')
            >>> # order and gpa column with Descending (False)
            >>> df.sort(["masters","gpa"], ascending=[True,False])
               masters   gpa     stats programming admitted
            id
            13      no  4.00  Advanced      Novice        1
            25      no  3.96  Advanced    Advanced        1
            28      no  3.93  Advanced    Advanced        1
            21      no  3.87    Novice    Beginner        1
            17      no  3.83  Advanced    Advanced        1
            9       no  3.82  Advanced    Advanced        1
            10      no  3.71  Advanced    Advanced        1
            3       no  3.70    Novice    Beginner        1
            16      no  3.70  Advanced    Advanced        1
            35      no  3.68    Novice    Beginner        1
            >>>
        """
        try:
            columns_expr=""
            orderexpr=""
            type_expr=[]
            invalid_types = []
            unsupported_types = ['BLOB', 'CLOB', 'ARRAY', 'VARRAY']

            if (isinstance(columns, str)):
                columns=[columns]
            if isinstance(ascending, bool):
                ascending=[ascending] * len(columns)
            # validating columns and validating each argument value for columns of passed lists
            if not ((isinstance(columns, list) or (isinstance(columns, str)))
                    and all(isinstance(col, str) for col in columns)):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "columns", ["list","str"]), MessageCodes.UNSUPPORTED_DATATYPE)
            # validating order types which has to be a list
            if not ((isinstance(ascending, list) or (isinstance(ascending, bool)))
                    and all(isinstance(asc, bool) for asc in ascending)):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "ascending", ["list","bool"]), MessageCodes.UNSUPPORTED_DATATYPE)
            # validating lengths of passed arguments which are passed i.e. length of columns
            # must be same as ascending
            if ascending and len(columns) != len(ascending):
                raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_LENGTH_ARGS), MessageCodes.INVALID_LENGTH_ARGS)
            # getting all the columns and data types for given metaexpr
            col_names, col_types = df_utils._get_column_names_and_types_from_metaexpr(self._metaexpr)
            # checking each element in passed columns to be valid column in dataframe
            for col in columns:
                if not df_utils._check_column_exists(col, col_names):
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDF_UNKNOWN_COLUMN, ": {}".format(col)), MessageCodes.TDF_UNKNOWN_COLUMN)
                else:
                    type_expr.append(self._metaexpr.t.c[col].type)
            # convert types to string from sqlalchemy type for the columns entered for sort
            columns_types = [repr(type_expr[i]).split("(")[0] for i in range(len(type_expr))]
            # checking each element in passed columns_types to be valid a data type for sort
            # and create a list of invalid_types
            for col_type in columns_types:
                if col_type in unsupported_types:
                    invalid_types.append(col_type)
            if len(invalid_types) > 0:
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, invalid_types, "ANY, except following {}".format(unsupported_types)), MessageCodes.UNSUPPORTED_DATATYPE)

            columns_expr = UtilFuncs._teradata_quote_arg(columns, "\"", False)
            if (len(ascending) != 0):
                val=['ASC' if i==True else 'DESC' for i in ascending]
                for c,v in zip(columns_expr,val):
                    orderexpr='{}{} {}, '.format(orderexpr,c,v)
                orderexpr=orderexpr[:-2]
            else:
                orderexpr=", ".join(columns_expr)
            # We are just updating orderby clause in exisitng teradataml dataframe
            # and returning new teradataml dataframe.
            sort_df = self._from_node(self._nodeid, self._metaexpr, self._index_label)
            sort_df._orderby = orderexpr
            # Assigning self attributes to newly created dataframe.
            sort_df._table_name = self._table_name
            sort_df._index = self._index
            sort_df._index_label = self._index_label
            return sort_df
        except TeradataMlException:
            raise

    def filter(self, items = None, like = None, regex = None, axis = 1, **kw):
        """
        DESCRIPTION:
            Filter rows or columns of dataframe according to labels in the specified index.
            The filter is applied to the columns of the index when axis is set to 'rows'.

            Must use one of the parameters 'items', 'like', and 'regex' only.

        PARAMETERS:
            axis:
                Optional Argument.
                Specifies the axis to filter on.
                1 denotes column axis (default). Alternatively, 'columns' can be specified.
                0 denotes row axis. Alternatively, 'rows' can be specified.
                Default Values: 1
                Permitted Values: 0, 1, 'rows', 'columns'
                Types: int OR str

            items:
                Optional Argument.
                List of values that the info axis should be restricted to
                When axis is 1, items is a list of column names
                When axis is 0, items is a list of literal values
                Types: list of Strings (str) or literals

            like:
                Optional Argument.
                When axis is 1, substring pattern for matching column names
                When axis is 0, substring pattern for checking index values with REGEXP_SUBSTR
                Types: str

            regex:
                Optional Argument.
                Specified a regular expression pattern.
                When axis is 1, regex pattern for re.search(regex, column_name)
                When axis is 0, regex pattern for checking index values with REGEXP_SUBSTR
                Types: str

            **kw: optional keyword arguments

                varchar_size:
                    An integer to specify the size of varchar-casted index.
                    Used when axis = 0/'rows' and index must be char-like in "like" and "regex" filtering
                    Default Value: configure.default_varchar_size
                    Types: int

                match_arg: string
                    argument to pass if axis is 0/'rows' and regex is used

                    Valid values for match_arg are:
                    - 'i' = case-insensitive matching.
                    - 'c' = case sensitive matching.
                    - 'n' = the period character (match any character) can match the newline character.
                    - 'm' = index value is treated as multiple lines instead of as a single line. With this option, the
                            '^' and '$' characters apply to each line in source_string instead of the entire index value.
                    - 'l' = if index value exceeds the current maximum allowed size (currently 16 MB), a NULL is returned
                            instead of an error.
                            This is useful for long-running queries where you do not want long strings
                            causing an error that would make the query fail.
                    - 'x' = ignore whitespace.

            The 'match_arg' argument may contain more than one character.
            If a character in 'match_arg' is not valid, then that character is ignored.

            See Teradata® Database SQL Functions, Operators, Expressions, and Predicates, Release 16.20
            for more information on specifying arguments for REGEXP_SUBSTR.

            NOTES:
                - Using 'regex' or 'like' with axis equal to 0 will attempt to cast the values in the index to a VARCHAR.
                  Note that conversion between BYTE data and other types is not supported.
                  Also, LOBs are not allowed to be compared.

                - When using 'like' or 'regex', datatypes are casted into VARCHAR.
                  This may alter the format of the value in the column(s)
                  and thus whether there is a match or not. The size of the VARCHAR may also
                  play a role since the casted value is truncated if the size is not big enough.
                  See varchar_size under **kw: optional keyword arguments.

        RETURNS:
            teradataml DataFrame

        RAISES:
            ValueError if more than one parameter: 'items', 'like', or 'regex' is used.
            TeradataMlException if invalid argument values are given.

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame('admissions_train')
            >>> df
               masters   gpa     stats programming admitted
            id
            22     yes  3.46    Novice    Beginner        0
            37      no  3.52    Novice      Novice        1
            35      no  3.68    Novice    Beginner        1
            12      no  3.65    Novice      Novice        1
            4      yes  3.50  Beginner      Novice        1
            38     yes  2.65  Advanced    Beginner        1
            27     yes  3.96  Advanced    Advanced        0
            39     yes  3.75  Advanced    Beginner        0
            7      yes  2.33    Novice      Novice        1
            40     yes  3.95    Novice    Beginner        0
            >>>
            >>> # retrieve columns masters, gpa, and stats in df
            ... df.filter(items = ['masters', 'gpa', 'stats'])
              masters   gpa     stats
            0     yes  4.00  Advanced
            1     yes  3.45  Advanced
            2     yes  3.50  Advanced
            3     yes  4.00    Novice
            4     yes  3.59  Advanced
            5      no  3.87    Novice
            6     yes  3.50  Beginner
            7     yes  3.79  Advanced
            8      no  3.00  Advanced
            9     yes  1.98  Advanced
            >>>
            >>> # retrieve rows where index matches ‘2’, ‘4’
            ... df.filter(items = ['2', '4'], axis = 0)
               masters   gpa     stats programming admitted
            id
            2      yes  3.76  Beginner    Beginner        0
            4      yes  3.50  Beginner      Novice        1
            >>>
            >>> df = DataFrame('admissions_train', index_label="programming")
            >>> df
                         id masters   gpa     stats admitted
            programming
            Beginner     22     yes  3.46    Novice        0
            Novice       37      no  3.52    Novice        1
            Beginner     35      no  3.68    Novice        1
            Novice       12      no  3.65    Novice        1
            Novice        4     yes  3.50  Beginner        1
            Beginner     38     yes  2.65  Advanced        1
            Advanced     27     yes  3.96  Advanced        0
            Beginner     39     yes  3.75  Advanced        0
            Novice        7     yes  2.33    Novice        1
            Beginner     40     yes  3.95    Novice        0
            >>>
            >>> # retrieve columns with a matching substring
            ... df.filter(like = 'masters')
              masters
            0     yes
            1     yes
            2     yes
            3     yes
            4     yes
            5      no
            6     yes
            7     yes
            8      no
            9     yes
            >>>
            >>> # retrieve rows where index values have ‘vice’ as a subtring
            ... df.filter(like = 'vice', axis = 'rows')
                         id masters   gpa     stats admitted
            programming
            Novice       12      no  3.65    Novice        1
            Novice        5      no  3.44    Novice        0
            Novice       24      no  1.87  Advanced        1
            Novice       36      no  3.00  Advanced        0
            Novice       23     yes  3.59  Advanced        1
            Novice       13      no  4.00  Advanced        1
            Novice       33      no  3.55    Novice        1
            Novice       30     yes  3.79  Advanced        0
            Novice        4     yes  3.50  Beginner        1
            Novice       37      no  3.52    Novice        1
            >>>
            >>> # give a regular expression to match column names
            ... df.filter(regex = '^a.+')
              admitted
            0        0
            1        1
            2        1
            3        1
            4        1
            5        1
            6        0
            7        0
            8        1
            9        0
            >>>
            >>> # give a regular expression to match values in index
            ... df.filter(regex = '^B.+', axis = 0)
                         id masters   gpa     stats admitted
            programming
            Beginner     39     yes  3.75  Advanced        0
            Beginner     38     yes  2.65  Advanced        1
            Beginner      3      no  3.70    Novice        1
            Beginner     31     yes  3.50  Advanced        1
            Beginner     21      no  3.87    Novice        1
            Beginner     34     yes  3.85  Advanced        0
            Beginner     32     yes  3.46  Advanced        0
            Beginner     29     yes  4.00    Novice        0
            Beginner     35      no  3.68    Novice        1
            Beginner     22     yes  3.46    Novice        0
            >>>
            >>> # case-insensitive, ignore white space when matching index values
            ... df.filter(regex = '^A.+', axis = 0, match_args = 'ix')
                         id masters   gpa     stats admitted
            programming
            Advanced     20     yes  3.90  Advanced        1
            Advanced      8      no  3.60  Beginner        1
            Advanced     25      no  3.96  Advanced        1
            Advanced     19     yes  1.98  Advanced        0
            Advanced     14     yes  3.45  Advanced        0
            Advanced      6     yes  3.50  Beginner        1
            Advanced     17      no  3.83  Advanced        1
            Advanced     11      no  3.13  Advanced        1
            Advanced     15     yes  4.00  Advanced        1
            Advanced     18     yes  3.81  Advanced        1
            >>>
            >>> # case-insensitive/ ignore white space/ match up to 32 characters
            ... df.filter(regex = '^A.+', axis = 0, match_args = 'ix', varchar_size = 32)
                         id masters   gpa     stats admitted
            programming
            Advanced     20     yes  3.90  Advanced        1
            Advanced      8      no  3.60  Beginner        1
            Advanced     25      no  3.96  Advanced        1
            Advanced     19     yes  1.98  Advanced        0
            Advanced     14     yes  3.45  Advanced        0
            Advanced      6     yes  3.50  Beginner        1
            Advanced     17      no  3.83  Advanced        1
            Advanced     11      no  3.13  Advanced        1
            Advanced     15     yes  4.00  Advanced        1
            Advanced     18     yes  3.81  Advanced        1
            >>>
        """

        # check that DataFrame has a valid axis

        if axis not in (0, 1, 'columns', 'rows'):
            raise ValueError("axis must be 0 ('rows') or 1 ('columns')")

        if self._index_label is None and axis in (0, 'rows'):
            raise AttributeError('DataFrame must have index_label set to a valid column')

        axis = 1 if axis == 'columns' or axis == 1 else 0
        errcode = MessageCodes.UNSUPPORTED_DATATYPE

        # validate items, like, regex type and value
        op = ''

        if items is not None:
            op += 'items'
            valid_value = (type(items) is list) and len(set(map(lambda x: type(x), items))) == 1

        if like is not None:
            op += 'like'
            valid_value = type(like) is str

        if regex is not None:
            op += 'regex'
            valid_value = type(regex) is str

        if op not in('items', 'like', 'regex'):
            raise ValueError('Must use exactly one of the parameters items, like, and regex.')

        if not valid_value:
            msg = 'The "items" parameter must be list of strings or tuples of column labels/index values. ' +\
                'The "regex" parameter and "like" parameter must be strings.'
            raise TeradataMlException(msg, errcode)

        # validate multi index labels for items
        if op == 'items' and axis == 0:

            num_col_indexes = len(self._index_label)
            if num_col_indexes > 1 and not all(map(lambda entry: len(entry) == num_col_indexes, items)):
                raise ValueError('tuple length in items must match length of multi index: %d' % num_col_indexes)

        # validate the optional keyword args
        if kw is not None and 'match_arg' in kw:
            if not isinstance(kw['match_arg'], str):
                msg = Messages.get_message(errcode, type(kw['match_arg']), 'match_arg', 'string')
                raise TeradataMlException(msg, errcode)

        if kw is not None and 'varchar_size' in kw:
            if not isinstance(kw['varchar_size'], int):
                msg = Messages.get_message(errcode, type(kw['varchar_size']), 'varchar_size', 'int')
                raise TeradataMlException(msg, errcode)

        # generate the sql expression
        expression = self._metaexpr._filter(axis, op, self._index_label,
                                            items=items,
                                            like=like,
                                            regex=regex,
                                            **kw)

        if axis == 1 and isinstance(expression, list):
            return self.select(expression)

        elif axis == 0 and isinstance(expression, ColumnExpression):
            return self.__getitem__(expression)

        else:
            errcode = MessageCodes.TDMLDF_INFO_ERROR
            msg = Messages.get_message(errcode)
            raise TeradataMlException(msg, errcode)

    def describe(self, percentiles=[.25, .5, .75], include=None):
        """
        DESCRIPTION:
            Generates statistics for numeric columns. Computes the count, mean, std, min, percentiles, and max for numeric columns.

        PARAMETERS:
            percentiles:
                Optional Argument.
                A list of values between 0 and 1.
                Defaulf Value: [.25, .5, .75], which returns the 25th, 50th, and 75th percentiles.
                Types: List of floats

            include:
                Optional Argument.
                Values can be either None or "all".
                If the value is "all", then both numeric and non-numeric columns are included.
                Computes count, mean, std, min, percentiles, and max for numeric columns.
                Computes count and unique for non-numeric columns.
                If the value is None, only numeric columns are used for collecting statics.
                Default Value: None
                Types: str

        RETURNS:
            teradataml DataFrame

        RAISE:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame('sales')
            >>> print(df)
                          Feb   Jan   Mar   Apr    datetime
            accounts
            Blue Inc     90.0    50    95   101  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            Jones LLC   200.0   150   140   180  04/01/2017
            Yellow Inc   90.0  None  None  None  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017
            Orange Inc  210.0  None  None   250  04/01/2017

            # Computes count, mean, std, min, percentiles, and max for numeric columns.
            >>> df.describe()
                      Apr      Feb     Mar     Jan
            func
            count       4        6       4       4
            mean   195.25  166.667   147.5   137.5
            std    70.971   59.554  49.749  62.915
            min       101       90      95      50
            25%    160.25    117.5  128.75     125
            50%       215      200     140     150
            75%       250    207.5  158.75   162.5
            max       250      210     215     200

            # Computes count, mean, std, min, percentiles, and max for numeric columns with 30th and 60th percentiles.
            >>> df.describe(percentiles=[.3, .6])
                      Apr      Feb     Mar     Jan
            func
            count       4        6       4       4
            mean   195.25  166.667   147.5   137.5
            std    70.971   59.554  49.749  62.915
            min       101       90      95      50
            30%     172.1      145   135.5     140
            60%       236      200     140     150
            max       250      210     215     200

            # Computes count, mean, std, min, percentiles, and max for numeric columns group by "datetime" and "Feb".
            >>> df1 = df.groupby(["datetime", "Feb"])
            >>> df1.describe()
                                     Jan   Mar   Apr
            datetime   Feb   func
            04/01/2017 90.0  25%      50    95   101
                             50%      50    95   101
                             75%      50    95   101
                             count     1     1     1
                             max      50    95   101
                             mean     50    95   101
                             min      50    95   101
                             std    None  None  None
                       200.0 25%     150   140   180
                             50%     150   140   180
                             75%     150   140   180
                             count     2     2     1
                             max     150   140   180
                             mean    150   140   180
                             min     150   140   180
                             std       0     0  None
                       210.0 25%     200   215   250
                             50%     200   215   250
                             75%     200   215   250
                             count     1     1     2
                             max     200   215   250
                             mean    200   215   250
                             min     200   215   250
                             std    None  None     0

            # Computes count, mean, std, min, percentiles, and max for numeric columns and
            # computes count and unique for non-numeric columns
            >>> df.describe(include="all")
                   accounts      Feb     Jan     Mar     Apr datetime
            func
            25%        None    117.5     125  128.75  160.25     None
            75%        None    207.5   162.5  158.75     250     None
            count         6        6       4       4       4        6
            mean       None  166.667   137.5   147.5  195.25     None
            max        None      210     200     215     250     None
            min        None       90      50      95     101     None
            50%        None      200     150     140     215     None
            std        None   59.554  62.915  49.749  70.971     None
            unique        6     None    None    None    None        1
        """
        function_label = "func"
        try:
            # percentiles must be a list of values between 0 and 1.
            if not isinstance(percentiles, list) or not all(p > 0 and p < 1 for p in percentiles):
                raise TeradataMlException(
                    Messages.get_message(MessageCodes.INVALID_ARG_VALUE, percentiles, "percentiles", "percentiles must be a list of values between 0 and 1"),
                    MessageCodes.INVALID_ARG_VALUE)
            # include must be either None or "all".
            if include is not None and include.lower() != "all":
                raise TeradataMlException(
                    Messages.get_message(MessageCodes.INVALID_ARG_VALUE, include, "include", "include must be either None or 'all'"),
                    MessageCodes.INVALID_ARG_VALUE)

            groupby_column_list = None
            if isinstance(self, DataFrameGroupBy):
                groupby_column_list = self.groupby_column_list

            self.__execute_node_and_set_table_name(self._nodeid)

            # Construct the aggregate query.
            agg_query = df_utils._construct_describe_query(self._table_name, self._metaexpr, percentiles, function_label, groupby_column_list, include)
            if groupby_column_list is not None:
                sort_cols = [i for i in groupby_column_list]
                sort_cols.append(function_label)
                df = DataFrame.from_query(agg_query, index_label=sort_cols)
                df2 = df.sort(sort_cols)
                df2._metaexpr._n_rows = 100
                return df2
            else:
                return DataFrame.from_query(agg_query, index_label=function_label)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR) from err

    def min(self):
        """
        DESCRIPTION:
            Returns column-wise minimum value of the dataframe.

        PARAMETERS:
            None

        RETURNS:
            teradataml DataFrame object with min()
            operation performed.

        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If min() operation fails to
                generate the column-wise minimum value of the dataframe.

                Possible error message:
                Unable to perform 'min()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the min() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'min' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info"])

            # Create teradataml dataframe.
            >>> df1 = DataFrame("employee_info")
            >>> print(df1)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Prints minimum value of each column(with supported data types).
            >>> df1.min()
              min_employee_no min_first_name min_marks min_dob min_joined_date
            0             100           abcd      None    None        02/12/05
            >>>

            # Select only subset of columns from the DataFrame.
            # Prints minimum value of each column(with supported data types).
            >>> df3 = df1.select(['employee_no', 'first_name', 'joined_date'])
            >>> df3.min()
              min_employee_no min_first_name min_joined_date
            0             100           abcd        02/12/05
            >>>
        """

        return self._get_dataframe_aggregate(operation = 'min')

    def max(self):
        """
        DESCRIPTION:
            Returns column-wise maximum value of the dataframe.

        PARAMETERS:
            None

        RETURNS:
            teradataml DataFrame object with max()
            operation performed.

        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If max() operation fails to
                generate the column-wise maximum value of the dataframe.

                Possible error message:
                Unable to perform 'max()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the max() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'max' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info"])

            # Create teradataml dataframe.
            >>> df1 = DataFrame("employee_info")
            >>> print(df1)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Prints maximum value of each column(with supported data types).
            >>> df1.max()
              max_employee_no max_first_name max_marks max_dob max_joined_date
            0             112          abcde      None    None        18/12/05
            >>>

            # Select only subset of columns from the DataFrame.
            >>> df3 = df1.select(['employee_no', 'first_name', 'joined_date'])

            # Prints maximum value of each column(with supported data types).
            >>> df3.max()
              max_employee_no max_first_name max_joined_date
            0             112          abcde        18/12/05
            >>>
        """

        return self._get_dataframe_aggregate(operation = 'max')

    def mean(self):
        """
        DESCRIPTION:
            Returns column-wise mean value of the dataframe.

        PARAMETERS:
            None

        RETURNS:
            teradataml DataFrame object with mean()
            operation performed.

        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If mean() operation fails to
                generate the column-wise mean value of the dataframe.

                Possible error message:
                Unable to perform 'mean()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the mean() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'mean' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info"])

            # Create teradataml dataframe.
            >>> df1 = DataFrame("employee_info")
            >>> print(df1)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Select only subset of columns from the DataFrame.
            >>> df2 = df1.select(['employee_no', 'marks', 'first_name'])

            # Prints mean value of each column(with supported data types).
            >>> df2.mean()
               mean_employee_no mean_marks
            0        104.333333       None
            >>>
        """

        return self._get_dataframe_aggregate(operation='mean')

    def sum(self):
        """
        DESCRIPTION:
            Returns column-wise sum value of the dataframe.

        PARAMETERS:
            None

        RETURNS:
            teradataml DataFrame object with sum()
            operation performed.

        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If sum() operation fails to
                generate the column-wise summation value of the dataframe.

                Possible error message:
                Unable to perform 'sum()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the sum() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'sum' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info"])

            # Create teradataml dataframe.
            >>> df1 = DataFrame("employee_info")
            >>> print(df1)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Prints sum of the values of each column(with supported data types).
            >>> df1.sum()
              sum_employee_no sum_marks
            0             313      None
            >>>

        Note :  teradataml doesn't support sum operation on
                character-like columns.

        """

        return self._get_dataframe_aggregate(operation='sum')

    def count(self):
        """
        DESCRIPTION:
            Returns column-wise count of the dataframe.

        PARAMETERS:
            None

        RETURNS:
            teradataml DataFrame object with count() operation
            performed.

        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If count() operation fails to
                generate the column-wise count of the dataframe.

                Possible error message:
                Unable to perform 'count()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the count() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'count' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info"])

            # Create teradataml dataframe.
            >>> df1 = DataFrame("employee_info")
            >>> print(df1)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Select only subset of columns from the DataFrame.
            >>> df2 = df1.select(['employee_no', 'first_name', 'marks'])

            # Prints count of the values in all the selected columns
            # (excluding None types).
            >>> df2.count()
              count_employee_no count_first_name count_marks
            0                 3                2           0
            >>>
        """

        return self._get_dataframe_aggregate(operation = 'count')

    def std(self):
        """
        DESCRIPTION:
            Returns column-wise sample standard deviation value of the
            dataframe.

        PARAMETERS:
            None

        RETURNS:
            teradataml DataFrame object with std() operation performed.

        RAISES:
            1. TDMLDF_AGGREGATE_FAILED - If std() operation fails to
                generate the column-wise standard deviation of the
                dataframe.

                Possible error message:
                Unable to perform 'std()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the std() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'std' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info"])

            # Create teradataml dataframe.
            >>> df1 = DataFrame("employee_info")
            >>> print(df1)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Select only subset of columns from the DataFrame.
            >>> df2 = df1.select(['employee_no', 'first_name', 'marks', 'dob'])

            # Prints standard deviation of each column(with supported data types).
            >>> df2.std()
               std_employee_no std_marks std_dob
            0         6.658328      None    None
            >>>
        """

        return self._get_dataframe_aggregate(operation = 'std')

    def median(self):
        """
        DESCRIPTION:
            Returns column-wise median value of the dataframe.

        PARAMETERS:
            None

        RETURNS:
            teradataml DataFrame object with median() operation
            performed.

        RAISES:
            1. TDMLDF_AGGREGATE_FAILED - If median() operation fails to
                generate the column-wise median value of the dataframe.

                Possible error message:
                Unable to perform 'median()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the median() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'median' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info"])

            # Create teradataml dataframe.
            >>> df1 = DataFrame("employee_info")
            >>> print(df1)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Prints median value of each column(with supported data types).
            >>> df1.median()
              median_employee_no median_marks
            0                101         None
            >>>
        """

        return self._get_dataframe_aggregate(operation = 'median')

    def var(self):
        """
        DESCRIPTION:
            Returns column-wise unbiased variance value of the dataframe.

        PARAMETERS:
            None
            
        RETURNS:
            teradataml DataFrame object with var() operation performed.

        RAISES:
            1. TDMLDF_AGGREGATE_FAILED - If var() operation fails to
                generate the column-wise variance of the dataframe.

                Possible error message:
                Unable to perform 'var()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the var() operation
                doesn't support all the columns in the dataframe.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col2 -  PERIOD_TIME), (col3 -
                BLOB)] is/are unsupported for 'var' operation.

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info", "sales"])

            # Example 1 - Applying var on table 'employee_info' that has all
            #             NULL values in marks and dob columns which are
            #             captured as None in variance dataframe.

            # Create teradataml dataframe.
            >>> df1 = DataFrame("employee_info")
            >>> print(df1)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Select only subset of columns from the DataFrame.
            >>> df3 = df1.select(["employee_no", "first_name", "dob", "marks"])

            # Prints unbiased variance of each column(with supported data types).
            >>> df3.var()
                   var_employee_no var_dob var_marks
                0        44.333333    None      None

            # Example 2 - Applying var on table 'sales' that has different
            #             types of data like floats, integers, strings
            #             some of which having NULL values which are ignored.

            # Create teradataml dataframe.
            >>> df1 = DataFrame("sales")
            >>> print(df1)
                              Feb   Jan   Mar   Apr    datetime
            accounts
            Blue Inc     90.0    50    95   101  04/01/2017
            Orange Inc  210.0  None  None   250  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017
            Yellow Inc   90.0  None  None  None  04/01/2017
            Jones LLC   200.0   150   140   180  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017

            # Prints unbiased variance of each column(with supported data types).
            >>> df3 = df1.select(["accounts","Feb","Jan","Mar","Apr"])
            >>> df3.var()
                   var_Feb      var_Jan  var_Mar      var_Apr
            0  3546.666667  3958.333333   2475.0  5036.916667
            >>>
        """
        return self._get_dataframe_aggregate(operation = 'var')

    def agg(self, func = None):
        """
        DESCRIPTION:
            Perform aggregates using one or more operations.

        PARAMETERS:
            func:
                Required Argument.
                Specifies the function(s) to apply on DataFrame columns.

                Valid values for func are:
                    'count', 'sum', 'min', 'max', 'mean', 'std', 'percentile', 'unique',
                    'median', 'var'

                Acceptable formats for function(s) are
                    string, dictionary or list of strings/functions.

                Accepted combinations are:
                    1. String function name
                    2. List of string functions
                    3. Dictionary containing column name as key and
                       aggregate function name (string or list of
                       strings) as value

        RETURNS:
            teradataml DataFrame object with operations
            mentioned in parameter 'func' performed on specified
            columns.

        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If operations on given columns
                fail to generate aggregate dataframe.

                Possible error message:
                Unable to perform 'agg()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the provided
                aggregate operations do not support specified columns.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col1 - VARCHAR)] is/are
                unsupported for 'sum' operation.

            3. TDMLDF_INVALID_AGGREGATE_OPERATION - If the aggregate
                operation(s) received in parameter 'func' is/are
                invalid.

                Possible error message:
                Invalid aggregate operation(s): minimum, counter.
                Valid aggregate operation(s): count, max, mean, min,
                std, sum.

            4. TDMLDF_AGGREGATE_INVALID_COLUMN - If any of the columns
                specified in 'func' is not present in the dataframe.

                Possible error message:
                Invalid column(s) given in parameter func: col1.
                Valid column(s) : A, B, C, D.

            5. MISSING_ARGS - If the argument 'func' is missing.

                Possible error message:
                Following required arguments are missing: func.

            6. UNSUPPORTED_DATATYPE - If the argument 'func' is not of
                valid datatype.

                Possible error message:
                Invalid type(s) passed to argument 'func', should be:"\
                             "['str', 'list', 'dict'].

        EXAMPLES :
            # Load the data to run the example.
            >>> from teradataml.data.load_example_data import load_example_data
            >>> load_example_data("dataframe", ["employee_info", "sales"])

            # Create teradataml dataframe.
            >>> df = DataFrame("employee_info")
            >>> print(df)
                        first_name marks   dob joined_date
            employee_no
            101              abcde  None  None    02/12/05
            100               abcd  None  None        None
            112               None  None  None    18/12/05
            >>>

            # Dictionary of column names to string function/list of string functions as parameter.
            >>> df.agg({'employee_no' : ['min', 'sum', 'var'], 'first_name' : ['min', 'mean']})
                  min_employee_no sum_employee_no  var_employee_no min_first_name
                0             100             313        44.333333           abcd

            # List of string functions as parameter.
            >>> df.agg(['min', 'sum'])
                  min_employee_no sum_employee_no min_first_name min_marks sum_marks min_dob min_joined_date
                0             100             313           abcd      None      None    None      1902-05-12

            # A string function as parameter.
            >>> df.agg('mean')
               mean_employee_no mean_marks mean_dob mean_joined_date
            0        104.333333       None     None         60/12/04

            # Select only subset of columns from the DataFrame.
            >>> df1 = df.select(['employee_no', 'first_name', 'joined_date'])

            # List of string functions as parameter.
            >>> df1.agg(['mean', 'unique'])
               mean_employee_no unique_employee_no unique_first_name mean_joined_date unique_joined_date
            0        104.333333                  3                 2         60/12/04                  2

            >>> df.agg('percentile')
                  percentile_employee_no percentile_marks
                0                    101             None

            # Using another table 'sales' (having repeated values) to demonstrate operations
            # 'unique' and 'percentile'.

            # Create teradataml dataframe.
            >>> df = DataFrame('sales')
            >>> df
                              Feb   Jan   Mar   Apr    datetime
                accounts
                Yellow Inc   90.0  None  None  None  2017-04-01
                Alpha Co    210.0   200   215   250  2017-04-01
                Jones LLC   200.0   150   140   180  2017-04-01
                Orange Inc  210.0  None  None   250  2017-04-01
                Blue Inc     90.0    50    95   101  2017-04-01
                Red Inc     200.0   150   140  None  2017-04-01

            >>> df.agg('percentile')
                   percentile_Feb percentile_Jan percentile_Mar percentile_Apr
                0           200.0            150            140            215

            >>> df.agg('unique')
                  unique_accounts unique_Feb unique_Jan unique_Mar unique_Apr unique_datetime
                0               6          3          3          3          3               1
        """

        if func is None:
            raise TeradataMlException(Messages.get_message(MessageCodes.MISSING_ARGS, "func"),
                                      MessageCodes.MISSING_ARGS)

        if not isinstance(func, str) and not isinstance(func, list) and not isinstance(func, dict):
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE,
                                'func', ['str', 'list', 'dict']), MessageCodes.UNSUPPORTED_DATATYPE)

        return self._get_dataframe_aggregate(func)

    def _get_dataframe_aggregate(self, operation):
        """
        Returns the DataFrame given the aggregate operation or list of
        operations or dictionary of column names -> operations.

        PARAMETERS:
            operation - Required Argument. Specifies the function(s) to be
                    applied on teradataml DataFrame columns.
                    Acceptable formats for function(s) are string,
                    dictionary or list of strings/functions.
                    Accepted combinations are:
                    1. String function name
                    2. List of string functions
                    3. Dictionary containing column name as key and
                       aggregate function name (string or list of
                       strings) as value

        RETURNS:
            teradataml DataFrame object with required
            operations mentioned in 'operation' parameter performed.

        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_FAILED - If operations on given columns
                fail to generate output dataframe.

                Possible error message:
                Unable to perform 'agg()' on the dataframe.

            2. TDMLDF_AGGREGATE_COMBINED_ERR - If the provided
                aggregate operations do not support specified columns.

                Possible error message:
                No results. Below is/are the error message(s):
                All selected columns [(col1 - VARCHAR)] is/are
                unsupported for 'sum' operation.

            3. TDMLDF_INVALID_AGGREGATE_OPERATION - If the aggregate
                operation(s) received in parameter 'operation' is/are
                invalid.

                Possible error message:
                Invalid aggregate operation(s): minimum, counter.
                Valid aggregate operation(s): count, max, mean, min,
                std, sum.

            4. TDMLDF_AGGREGATE_INVALID_COLUMN - If any of the columns
                specified in the parameter 'operation' is not present
                in the dataframe.

                Possible error message:
                Invalid column(s) given in parameter func: col1.
                Valid column(s) : A, B, C, D.

        EXAMPLES :
            df = _get_dataframe_aggregate(operation = 'mean')
            or
            df = _get_dataframe_aggregate(operation = ['mean', 'min'])
            or
            df = _get_dataframe_aggregate(operation = {'col1' :
                                    ['mean', 'min'], 'col2' : 'count'})
        """

        try:
            col_names, col_types = df_utils._get_column_names_and_types_from_metaexpr(self._metaexpr)
            # Remove columns from metaexpr before passing to stated aggr func if dataframe
            # is of DataFrameGroupBy type so that no duplicate columns shown in result
            groupby_col_names = []
            groupby_col_types = []
            if isinstance(self, DataFrameGroupBy):
                for col in self.groupby_column_list:
                    colindex = col_names.index(col)
                    groupby_col_names.append(col)
                    groupby_col_types.append(col_types[colindex])
                    del col_names[colindex]
                    del col_types[colindex]
            # Return Empty DataFrame if all the columns are selected in groupby as parent has
            if len(col_names) == 0:
                aggregate_expression, new_column_names, new_column_types = \
                        df_utils._construct_sql_expression_for_aggregations(groupby_col_names, groupby_col_types,
                                                                            operation)
                self._index_label = new_column_names
            else:
                aggregate_expression, new_column_names, new_column_types = \
                        df_utils._construct_sql_expression_for_aggregations(col_names, col_types,
                                                                            operation)
                new_column_names = groupby_col_names + new_column_names
                new_column_types = groupby_col_types + new_column_types

            if isinstance(operation, dict) or isinstance(operation, list):
                operation = 'agg'

            aggregate_node_id = self._aed_utils._aed_aggregate(self._nodeid, aggregate_expression,
                                                               operation)

            new_metaexpr = UtilFuncs._get_metaexpr_using_columns(aggregate_node_id,
                                                                 zip(new_column_names,
                                                                     new_column_types))
            return DataFrame._from_node(aggregate_node_id, new_metaexpr, self._index_label)

        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(
                MessageCodes.TDMLDF_AGGREGATE_FAILED, str(err.exception)).format(operation),
                                      MessageCodes.TDMLDF_AGGREGATE_FAILED) from err

    def __repr__(self):
        """
        Returns the string representation for a teradataml DataFrame instance.
        The string contains:
            1. Column names of the dataframe.
            2. At most the first no_of_rows rows of the dataframe.
            3. A default index for row numbers.

        NOTES:
          - This makes an explicit call to get rows from the database.
          - To change number of rows to be printed set the max_rows option in options.display.display
          - Default value of max_rows is 10

        EXAMPLES:
            df = DataFrame.from_table("table1")
            print(df)

            df = DataFrame.from_query("select col1, col2, col3 from table1")
            print(df)
        """
        try:

            # Generate/Execute AED nodes
            self.__execute_node_and_set_table_name(self._nodeid, self._metaexpr)

            query = repr(self._metaexpr) + ' FROM ' + self._table_name

            if self._orderby is not None:
                query += ' ORDER BY ' + self._orderby

            context = tdmlctx.get_context()
            if self._index_label:
                pandas_df = pd.read_sql_query(query, context, index_col = self._index_label)
            else:
                pandas_df = pd.read_sql_query(query, context)

            if self._undropped_index is not None:
                for col in self._undropped_index:
                    pandas_df.insert(0, col, pandas_df.index.get_level_values(col).tolist(), allow_duplicates = True)

            return pandas_df.to_string()

        except TeradataMlException:
            raise

        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR) + str(err),
                                      MessageCodes.TDMLDF_INFO_ERROR) from err

    def select(self, select_expression):
        """
        DESCRIPTION:
            Select required columns from DataFrame using an expression.
            Returns a new teradataml DataFrame with selected columns only.

        PARAMETERS:

            select_expression:
                Required Argument.
                String or List representing columns to select.
                Types: str OR List of Strings (str)

                The following formats (only) are supported for select_expression:

                A] Single Column String: df.select("col1")
                B] Single Column List: df.select(["col1"])
                C] Multi-Column List: df.select(['col1', 'col2', 'col3'])
                D] Multi-Column List of List: df.select([["col1", "col2", "col3"]])

                Column Names ("col1", "col2"..) are Strings representing Teradata Vantage table Columns.
                All Standard Teradata Data-Types for columns supported: INTEGER, VARCHAR(5), FLOAT.

                Note: Multi-Column selection of the same column such as df.select(['col1', 'col1']) is not supported.

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException (TDMLDF_SELECT_INVALID_COLUMN, TDMLDF_SELECT_INVALID_FORMAT,
                                 TDMLDF_SELECT_DF_FAIL, TDMLDF_SELECT_EXPR_UNSPECIFIED,
                                 TDMLDF_SELECT_NONE_OR_EMPTY)

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame('admissions_train')
            >>> df
               masters   gpa     stats programming admitted
            id
            5       no  3.44    Novice      Novice        0
            7      yes  2.33    Novice      Novice        1
            22     yes  3.46    Novice    Beginner        0
            17      no  3.83  Advanced    Advanced        1
            13      no  4.00  Advanced      Novice        1
            19     yes  1.98  Advanced    Advanced        0
            36      no  3.00  Advanced      Novice        0
            15     yes  4.00  Advanced    Advanced        1
            34     yes  3.85  Advanced    Beginner        0
            40     yes  3.95    Novice    Beginner        0

            A] Single String Column
            >>> df.select("id")
            Empty DataFrame
            Columns: []
            Index: [22, 34, 13, 19, 15, 38, 26, 5, 36, 17]

            B] Single Column List
            >>> df.select(["id"])
            Empty DataFrame
            Columns: []
            Index: [15, 26, 5, 40, 22, 17, 34, 13, 7, 38]

            C] Multi-Column List
            >>> df.select(["id", "masters", "gpa"])
               masters   gpa
            id
            5       no  3.44
            36      no  3.00
            15     yes  4.00
            17      no  3.83
            13      no  4.00
            40     yes  3.95
            7      yes  2.33
            22     yes  3.46
            34     yes  3.85
            19     yes  1.98

            D] Multi-Column List of List
            >>> df.select([['id', 'masters', 'gpa']])
               masters   gpa
            id
            5       no  3.44
            34     yes  3.85
            13      no  4.00
            40     yes  3.95
            22     yes  3.46
            19     yes  1.98
            36      no  3.00
            15     yes  4.00
            7      yes  2.33
            17      no  3.83
        """
        try:
            if self._metaexpr is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR), MessageCodes.TDMLDF_INFO_ERROR)

            # If invalid, appropriate exception raised; Processing ahead only for valid expressions
            select_exp_col_list = self.__validate_select_expression(select_expression)

            # Constructing New Column names & Types for selected columns ONLY using Parent _metaexpr
            col_names_types = df_utils._get_required_columns_types_from_metaexpr(self._metaexpr, select_exp_col_list)

            meta = sqlalchemy.MetaData()
            aed_utils = AedUtils()

            column_expression = ','.join(select_exp_col_list)
            sel_nodeid = aed_utils._aed_select(self._nodeid, column_expression)

            # Constructing new Metadata (_metaexpr) without DB; using dummy select_nodeid
            cols = (Column(col_name, col_type) for col_name, col_type in col_names_types.items())
            t = Table(sel_nodeid, meta, *cols)
            new_metaexpr = _MetaExpression(t)

            return DataFrame._from_node(sel_nodeid, new_metaexpr, self._index_label)

        except TeradataMlException:
            raise

        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_SELECT_DF_FAIL, str(err.exception)),
                                      MessageCodes.TDMLDF_SELECT_DF_FAIL) from err

    def __validate_select_expression(self, select_expression):
        """
        This is an internal function used to validate the select expression for the Select API.
        When the select expression is valid, a list of valid columns to be selected is returned.
        Appropriate TeradataMlException is raised when validation fails.

        PARAMETERS:
            select_expression - The expression to be validated.
            Type: Single String or List of Strings or List of List (single-level)
            Required: Yes

        RETURNS:
            List of column name strings, when valid select_expression is passed.

        RAISES:
            TeradataMlException, when parameter validation fails.

        EXAMPLES:
            self.__validate_select_expression(select_expression = 'col1')
            self.__validate_select_expression(select_expression = ["col1"])
            self.__validate_select_expression(select_expression = [['col1', 'col2', 'col3']])
        """
        tdp = preparer(td_dialect)

        if select_expression is None:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_SELECT_EXPR_UNSPECIFIED),
                                      MessageCodes.TDMLDF_SELECT_EXPR_UNSPECIFIED)

        else:
            # _extract_select_string returns column list only if valid; else raises appropriate exception
            select_exp_col_list = df_utils._extract_select_string(select_expression)
            df_column_list = [tdp.quote("{0}".format(column.name)) for column in self._metaexpr.c]

            # TODO: Remove this check when same column multiple selection enabled
            if len(select_exp_col_list) > len(df_column_list):
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_SELECT_INVALID_COLUMN, ', '.join(df_column_list)),
                                          MessageCodes.TDMLDF_SELECT_INVALID_COLUMN)

            all_cols_exist =  all(col in df_column_list for col in select_exp_col_list)

            if not all_cols_exist:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_SELECT_INVALID_COLUMN, ', '.join(df_column_list)),
                                          MessageCodes.TDMLDF_SELECT_INVALID_COLUMN)

            return select_exp_col_list

    def to_pandas(self, index_column = None, num_rows = 99999):
        """
        DESCRIPTION:
            Returns a Pandas DataFrame for the corresponding teradataml DataFrame Object.

        PARAMETERS:

            index_column:
                Optional Argument.
                Specifies column(s) to be used as Pandas index.
                When the arguemnt is provided, the specified column is used as the Pandas index.
                Otherwise, the teradataml DataFrame's index (if exists) is used as the Pandas index
                or the primary index of the table on Vantage is used as the Pandas index.
                The default integer index is used if none of the above indexes exists.
                Default Value: Integer index
                Types: str OR list of Strings (str)

            num_rows:
                Optional Argument.
                The number of rows to retrieve from DataFrame while creating Pandas Dataframe.
                Default Value: 99999
                Types: int

        RETURNS:
            Pandas DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:

            Teradata supports the following formats:

            A] No parameter(s): df.to_pandas()
            B] Single index_column parameter: df.to_pandas(index_column = "col1")
            C] Multiple index_column (list) parameters: df.to_pandas(index_column = ['col1', 'col2'])
            D] Only num_rows parameter specified:  df.to_pandas(num_rows = 100)
            E] Both index_column & num_rows specified: df.to_pandas(index_column = 'col1', num_rows = 100)

            Column names ("col1", "col2"..) are strings representing Teradata Vantage table Columns.
            It supports all standard Teradata data types for columns: INTEGER, VARCHAR(5), FLOAT etc.
            df is a Teradata DataFrame object: df = DataFrame.from_table('admissions_train')

            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming admitted
            id
            22     yes  3.46    Novice    Beginner        0
            37      no  3.52    Novice      Novice        1
            35      no  3.68    Novice    Beginner        1
            12      no  3.65    Novice      Novice        1
            4      yes  3.50  Beginner      Novice        1
            38     yes  2.65  Advanced    Beginner        1
            27     yes  3.96  Advanced    Advanced        0
            39     yes  3.75  Advanced    Beginner        0
            7      yes  2.33    Novice      Novice        1
            40     yes  3.95    Novice    Beginner        0
            >>> pandas_df = df.to_pandas()
            >>> pandas_df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            14     yes  3.45  Advanced    Advanced         0
            31     yes  3.50  Advanced    Beginner         1
            29     yes  4.00    Novice    Beginner         0
            23     yes  3.59  Advanced      Novice         1
            21      no  3.87    Novice    Beginner         1
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            32     yes  3.46  Advanced    Beginner         0
            11      no  3.13  Advanced    Advanced         1
            ...

            >>> pandas_df = df.to_pandas(index_column = 'id')
            >>> pandas_df
               masters   gpa     stats programming  admitted
            id
            15     yes  4.00  Advanced    Advanced         1
            14     yes  3.45  Advanced    Advanced         0
            31     yes  3.50  Advanced    Beginner         1
            29     yes  4.00    Novice    Beginner         0
            23     yes  3.59  Advanced      Novice         1
            21      no  3.87    Novice    Beginner         1
            17      no  3.83  Advanced    Advanced         1
            34     yes  3.85  Advanced    Beginner         0
            13      no  4.00  Advanced      Novice         1
            32     yes  3.46  Advanced    Beginner         0
            11      no  3.13  Advanced    Advanced         1
            28      no  3.93  Advanced    Advanced         1
            ...

            >>> pandas_df = df.to_pandas(index_column = 'gpa')
            >>> pandas_df
                  id masters     stats programming  admitted
            gpa
            4.00  15     yes  Advanced    Advanced         1
            3.45  14     yes  Advanced    Advanced         0
            3.50  31     yes  Advanced    Beginner         1
            4.00  29     yes    Novice    Beginner         0
            3.59  23     yes  Advanced      Novice         1
            3.87  21      no    Novice    Beginner         1
            3.83  17      no  Advanced    Advanced         1
            3.85  34     yes  Advanced    Beginner         0
            4.00  13      no  Advanced      Novice         1
            3.46  32     yes  Advanced    Beginner         0
            3.13  11      no  Advanced    Advanced         1
            3.93  28      no  Advanced    Advanced         1
            ...

            >>> pandas_df = df.to_pandas(index_column = ['masters', 'gpa'])
            >>> pandas_df
                          id     stats programming  admitted
            masters gpa
            yes     4.00  15  Advanced    Advanced         1
                    3.45  14  Advanced    Advanced         0
                    3.50  31  Advanced    Beginner         1
                    4.00  29    Novice    Beginner         0
                    3.59  23  Advanced      Novice         1
            no      3.87  21    Novice    Beginner         1
                    3.83  17  Advanced    Advanced         1
            yes     3.85  34  Advanced    Beginner         0
            no      4.00  13  Advanced      Novice         1
            yes     3.46  32  Advanced    Beginner         0
            no      3.13  11  Advanced    Advanced         1
                    3.93  28  Advanced    Advanced         1
            ...

            >>> pandas_df = df.to_pandas(index_column = 'gpa', num_rows = 3)
            >>> pandas_df
                  id masters   stats programming  admitted
            gpa
            3.46  22     yes  Novice    Beginner         0
            2.33   7     yes  Novice      Novice         1
            3.95  40     yes  Novice    Beginner         0

        """
        try:
            pandas_df = None

            df_utils._validate_to_pandas_parameters(self, index_column, num_rows)

            # Un-executed - Generate/Execute Nodes & Set Table Name
            if self._nodeid:
                self.__execute_node_and_set_table_name(self._nodeid, self._metaexpr)
            else:
                raise TeradataMlException(Messages.get_message(MessageCodes.TO_PANDAS_FAILED),
                                          MessageCodes.TO_PANDAS_FAILED)

            pandas_df = df_utils._get_pandas_dataframe(self._table_name, index_column,
                                                       self._index_label, num_rows, self._orderby)
            if pandas_df is not None:
                return pandas_df
            else:
                raise TeradataMlException(Messages.get_message(MessageCodes.EMPTY_DF_RETRIEVED),
                                              MessageCodes.EMPTY_DF_RETRIEVED)
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TO_PANDAS_FAILED) + str(err),
                                      MessageCodes.TO_PANDAS_FAILED) from err

    def __validate_to_pandas_parameters(self, index_column, num_rows):
        """
        Validates the to_pandas API parameters.

        PARAMETERS:
            index_column - User Specified String/List specifying columns to use as Pandas Index.
            num_rows - Integer specifying number of rows to use to create Pandas Dataframe;

        EXAMPLES:
             __validate_to_pandas_parameters(index_column, num_rows)

        RETURNS:
            None

        RAISES:
            TeradataMlException (TDMLDF_INFO_ERROR, UNSUPPORTED_DATATYPE,
                                 INVALID_ARG_VALUE, DF_LABEL_MISMATCH)
        """

        if self._metaexpr is not None:
            df_column_list = [col.name for col in self._metaexpr.c]
        else:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR),
                                      MessageCodes.TDMLDF_INFO_ERROR)

        if index_column is not None:
            # Check Format validity for index_column
            if not (isinstance(index_column, str) or isinstance(index_column, list)):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "index_column",
                                                               "string or list of strings"),
                                          MessageCodes.UNSUPPORTED_DATATYPE)

            self.__check_column_in_dataframe(index_column, 'index_column')

        # Check if TDML DF has appropriate index_label set when required
        df_index_label = self._index_label

        if df_index_label is not None:
            if isinstance(df_index_label, str):
                if df_index_label.lower() not in df_column_list:
                    raise TeradataMlException(Messages.get_message(MessageCodes.DF_LABEL_MISMATCH), MessageCodes.DF_LABEL_MISMATCH)
            elif isinstance(df_index_label, list):
                for index_label in df_index_label:
                    if index_label.lower() not in df_column_list:
                        raise TeradataMlException(Messages.get_message(MessageCodes.DF_LABEL_MISMATCH), MessageCodes.DF_LABEL_MISMATCH)

        # Check Format validity for num_rows
        if num_rows is not None:
            if not isinstance(num_rows, int):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "num_rows", "int"),
                                          MessageCodes.UNSUPPORTED_DATATYPE)
            elif num_rows <= 0:
                awuObj = AnalyticsWrapperUtils()
                arg_name = awuObj._deparse_arg_name(num_rows)
                raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_ARG_VALUE,num_rows, arg_name,
                                                               "integer value greater than zero"),
                                          MessageCodes.INVALID_ARG_VALUE)

    def __check_column_in_dataframe(self, column_names, error_message_arg = 'Dataframe column name'):
        """
        Internal Utility function to check if given column(s) (String or list of strings)
        exists in the Dataframe columns or not.

        PARAMETERS:
            column_names - String or List of strings specifying column names to be checked.

            error_message_arg Optional Argument. - Specifies column name/argument to be used in the
                exception message of the format: "Invalid value passed for argument: error_message_arg"
                Default: 'Dataframe column name'

        RETURNS:
            True, when all columns specified are valid (exist in DataFrame)
            TeradataMlException, otherwise.

        RAISES:
            TeradataMlException (INVALID_ARG_VALUE)

        EXAMPLES:
            __check_column_in_dataframe('column_name')
            __check_column_in_dataframe(['column_name1', 'column_name2'])
            __check_column_in_dataframe('column_name', error_message_arg = 'index_column')

        """
        if self._metaexpr is not None:
            df_column_list = [col.name for col in self._metaexpr.c]

        if isinstance(column_names, list):
            for column in column_names:
                #if not isinstance(column, str) or (column.lower() not in df_column_list):
                if not isinstance(column, str) or not df_utils._check_column_exists(column.lower(), df_column_list):
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_COLUMN_NOT_FOUND,column,""),
                                          MessageCodes.TDMLDF_COLUMN_NOT_FOUND)

        elif isinstance(column_names, str):
            #if column_names.lower() not in df_column_list:
            if not df_utils._check_column_exists(column_names.lower(), df_column_list):
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_COLUMN_NOT_FOUND, column_names, ""),
                                          MessageCodes.TDMLDF_COLUMN_NOT_FOUND)
        return True

    def join(self, other, on=None, how="left", lsuffix=None, rsuffix=None):
        """
        DESCRIPTION:
            Joins two different teradataml DataFrames together based on column comparisons
            specified in argument 'on' and type of join is specified in the argument 'how'.
            Supported join operations are:
            • Inner join: Returns only matching rows, non matching rows are eliminated.
            • Left outer join: Returns all matching rows plus non matching rows from the left table.
            • Right outer join: Returns all matching rows plus non matching rows from the right table.
            • Full outer join: Returns all rows from both tables, including non matching rows.
            • Cross join: Returns all rows from both tables where each row from the first table
                          is joined with each row from the second table. The result of the join
                          is a cartesian cross product.
                          Note: For a cross join, the 'on' argument is ignored.
            Supported join operators are =, ==, <, <=, >, >=, <> and != (= and <> operators are
            not supported when using DataFrame columns as operands).

            Note:
                1.  When multiple join conditions are given, they are joined using AND boolean
                    operator. Other boolean operators are not supported.
                2.  Nesting of join on conditions in column expressions using & and | is not
                    supported. The example for unsupported nested join on conditions is:
                    on = [(df1.a == df1.b) & (df1.c == df1.d)]

                    One can use [df1.a == df1.b, df1.c == df1.d] in place of
                    [(df1.a == df1.b) & (df1.c == df1.d)].

        PARAMETERS:

            other:
                Required argument.
                Specifies right teradataml DataFrame on which join is to be performed.
                Types: teradataml DataFrame

            on:
                Optional argument when "how" is "cross", otherwise required.
                If specified when "how" is "cross", it is ignored.
                Specifies list of conditions that indicate the columns to be join keys.

                It can take the following forms:
                • String comparisons, in the form of "col1 <= col2", where col1 is
                  the column of left dataframe df1 and col2 is the column of right
                  dataframe df2.
                  Examples:
                    1. ["a","b"] indicates df1.a = df2.a and df1.b = df2.b.
                    2. ["a = b", "c == d"] indicates df1.a = df2.b and df1.c = df2.d.
                    3. ["a <= b", "c > d"] indicates df1.a <= df2.b and df1.c > df2.d.
                    4. ["a < b", "c >= d"] indicates df1.a < df2.b and df1.c >= df2.d.
                    5. ["a <> b"] indicates df1.a != df2.b. Same is the case for ["a != b"].
                • Column comparisons, in the form of df1.col1 <= df1.col2, where col1
                  is the column of left dataframe df1 and col2 is the column of right
                  dataframe df2.
                  Examples:
                    1. [df1.a == df2.a, df1.b == df2.b] indicates df1.a = df2.a and df1.b = df2.b.
                    2. [df1.a == df2.b, df1.c == df2.d] indicates df1.a = df2.b and df1.c = df2.d.
                    3. [df1.a <= df2.b and df1.c > df2.d] indicates df1.a <= df2.b and df1.c > df2.d.
                    4. [df1.a < df2.b and df1.c >= df2.d] indicates df1.a < df2.b and df1.c >= df2.d.
                    5. df1.a != df2.b indicates df1.a != df2.b.
                • The combination of both string comparisons and comparisons as column expressions.
                  Examples:
                    1. ["a", df1.b == df2.b] indicates df1.a = df2.a and df1.b = df2.b.
                    2. [df1.a <= df2.b, "c > d"] indicates df1.a <= df2.b and df1.c > df2.d.

                Types: str (or) ColumnExpression (or) List of strings(str) or ColumnExpressions

            how:
                Optional argument.
                Specifies the type of join to perform.
                Default value is "left".
                Permitted Values : "inner", "left", "right", "full" and "cross"
                Types: str

            lsuffix:
                Optional argument.
                Specifies the suffix to be added to the left table columns.
                Default Value: None.
                Types: str

            rsuffix:
                Optional argument.
                Specifies the suffix to be added to the right table columns.
                Default Value: None.
                Types: str

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            # Load the data to run the example.
            >>> from teradataml import load_example_data
            >>> load_example_data("dataframe", ["join_table1", "join_table2"])
            >>> load_example_data("glm", "admissions_train") # used in cross join

            >>> df1 = DataFrame("join_table1")
            >>> df2 = DataFrame("join_table2")

            # Print dataframe.
            >>> df1
                       col2  col3 col5
            col1
            2     analytics   2.3    b
            1      teradata   1.3    a
            3      platform   3.3    c

            # Print dataframe.
            >>> df2
                       col4  col3 col7
            col1
            2     analytics   2.3    b
            1      teradata   1.3    a
            3       are you   4.3    d

            # Both on conditions as strings.
            >>> df1.join(other = df2, on = ["col2=col4", "col1"], how = "inner", lsuffix = "t1", rsuffix = "t2")
              t1_col1 t2_col1       col2  t1_col3  t2_col3 col5       col4 col7
            0       2       2  analytics      2.3      2.3    b  analytics    b
            1       1       1   teradata      1.3      1.3    a   teradata    a

            # One on condition is ColumnExpression and other is string having two columns with left
            # outer join.
            >>> df1.join(df2, on = [df1.col2 == df2.col4,"col5 = col7"], how = "left", lsuffix = "t1", rsuffix = "t2")
              t1_col1 t2_col1       col2  t1_col3  t2_col3 col5       col4  col7
            0       3    None   platform      3.3      NaN    c       None  None
            1       2       2  analytics      2.3      2.3    b  analytics     b
            2       1       1   teradata      1.3      1.3    a   teradata     a

            # One on condition is ColumnExpression and other is string having only one column.
            >>> df1.join(other = df2, on = [df1.col2 == df2.col4,"col3"], how = "inner", lsuffix = "t1", rsuffix = "t2")
              t1_col1 t2_col1       col2  t1_col3  t2_col3 col5       col4 col7
            0       2       2  analytics      2.3      2.3    b  analytics    b
            1       1       1   teradata      1.3      1.3    a   teradata    a

            # One on condition is ColumnExpression and other is string having two columns with
            # full join.
            >>> df1.join(other = df2, on = ["col2=col4",df1.col5 == df2.col7], how = "full", lsuffix = "t1", rsuffix = "t2")
              t1_col1 t2_col1       col2  t1_col3  t2_col3  col5       col4  col7
            0       3    None   platform      3.3      NaN     c       None  None
            1    None       3       None      NaN      4.3  None    are you     d
            2       1       1   teradata      1.3      1.3     a   teradata     a
            3       2       2  analytics      2.3      2.3     b  analytics     b

            # Using not equal operation in ColumnExpression condition.
            >>> df1.join(other = df2, on = ["col5==col7",df1.col2 != df2.col4], how = "full", lsuffix = "t1", rsuffix = "t2")
              t1_col1 t2_col1       col2  t1_col3  t2_col3  col5       col4  col7
            0       1    None   teradata      1.3      NaN     a       None  None
            1       2    None  analytics      2.3      NaN     b       None  None
            2    None       2       None      NaN      2.3  None  analytics     b
            3    None       1       None      NaN      1.3  None   teradata     a
            4       3    None   platform      3.3      NaN     c       None  None
            5    None       3       None      NaN      4.3  None    are you     d

            # Using only one string expression with <> operation.
            >>> df1.join(other = df2, on = "col2<>col4", how = "left", lsuffix = "t1", rsuffix = "t2")
              t1_col1 t2_col1       col2  t1_col3  t2_col3 col5       col4 col7
            0       2       3  analytics      2.3      4.3    b    are you    d
            1       2       1  analytics      2.3      1.3    b   teradata    a
            2       3       2   platform      3.3      2.3    c  analytics    b
            3       1       2   teradata      1.3      2.3    a  analytics    b
            4       3       1   platform      3.3      1.3    c   teradata    a
            5       1       3   teradata      1.3      4.3    a    are you    d
            6       3       3   platform      3.3      4.3    c    are you    d

            # Using only one ColumnExpression in on conditions.
            >>> df1.join(other = df2, on = df1.col5 != df2.col7, how = "full", lsuffix = "t1", rsuffix = "t2")
              t1_col1 t2_col1       col2  t1_col3  t2_col3 col5       col4 col7
            0       1       3   teradata      1.3      4.3    a    are you    d
            1       3       1   platform      3.3      1.3    c   teradata    a
            2       1       2   teradata      1.3      2.3    a  analytics    b
            3       3       2   platform      3.3      2.3    c  analytics    b
            4       2       1  analytics      2.3      1.3    b   teradata    a
            5       3       3   platform      3.3      4.3    c    are you    d
            6       2       3  analytics      2.3      4.3    b    are you    d

            # Both on conditions as ColumnExpressions.
            >>> df1.join(df2, on = [df1.col2 == df2.col4, df1.col5 > df2.col7], how = "right", lsuffix = "t1", rsuffix ="t2")
              t1_col1 t2_col1  col2 t1_col3  t2_col3  col5       col4 col7
            0    None       2  None    None      2.3  None  analytics    b
            1    None       1  None    None      1.3  None   teradata    a
            2    None       3  None    None      4.3  None    are you    d

            # cross join "admissions_train" with "admissions_train".
            >>> df1 = DataFrame("admissions_train").head(3).sort("id")
            >>> print(df1)
            masters   gpa     stats programming admitted
            id
            1      yes  3.95  Beginner    Beginner        0
            2      yes  3.76  Beginner    Beginner        0
            3       no  3.70    Novice    Beginner        1

            >>> df2 = DataFrame("admissions_train").head(3).sort("id")
            >>> print(df2)
            masters   gpa     stats programming admitted
            id
            1      yes  3.95  Beginner    Beginner        0
            2      yes  3.76  Beginner    Beginner        0
            3       no  3.70    Novice    Beginner        1

            >>> df3 = df1.join(other=df2, how="cross", lsuffix="l", rsuffix="r")
            >>> df3.set_index("l_id").sort("l_id")
                 l_programming   r_stats r_id  r_gpa r_programming  l_gpa   l_stats r_admitted l_admitted l_masters r_masters
            l_id
            1         Beginner    Novice    3   3.70      Beginner   3.95  Beginner          1          0       yes        no
            1         Beginner  Beginner    1   3.95      Beginner   3.95  Beginner          0          0       yes       yes
            1         Beginner  Beginner    2   3.76      Beginner   3.95  Beginner          0          0       yes       yes
            2         Beginner  Beginner    1   3.95      Beginner   3.76  Beginner          0          0       yes       yes
            2         Beginner  Beginner    2   3.76      Beginner   3.76  Beginner          0          0       yes       yes
            2         Beginner    Novice    3   3.70      Beginner   3.76  Beginner          1          0       yes        no
            3         Beginner  Beginner    1   3.95      Beginner   3.70    Novice          0          1        no       yes
            3         Beginner  Beginner    2   3.76      Beginner   3.70    Novice          0          1        no       yes
            3         Beginner    Novice    3   3.70      Beginner   3.70    Novice          1          1        no        no
        """
        if not isinstance(other, DataFrame):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "other", "TeradataML DataFrame"),
                MessageCodes.UNSUPPORTED_DATATYPE)

        if not isinstance(how, str):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "how", "str"),
                MessageCodes.UNSUPPORTED_DATATYPE)

        how_lc = how.lower()
        if how_lc not in TeradataConstants.TERADATA_JOINS.value:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.INVALID_ARG_VALUE, how, "how", TeradataConstants.TERADATA_JOINS.value),
                MessageCodes.INVALID_ARG_VALUE)

        if on is None and how_lc != "cross":
            raise TeradataMlException(
                Messages.get_message(MessageCodes.MISSING_ARGS, "on"),
                MessageCodes.MISSING_ARGS)

        for column in self.columns:
            if column in other.columns:
                if lsuffix is None or rsuffix is None:
                    raise TeradataMlException(
                        Messages.get_message(MessageCodes.TDMLDF_REQUIRED_TABLE_ALIAS),MessageCodes.TDMLDF_REQUIRED_TABLE_ALIAS)

        if lsuffix is None:
            lsuffix = "df1"

        if rsuffix is None:
            rsuffix = "df2"

        if isinstance(lsuffix,str) is False or isinstance(rsuffix,str) is False:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "'lsuffix' or 'rsuffix'", "'str'"),
                MessageCodes.UNSUPPORTED_DATATYPE)
        # Both suffix shuold not be equal to perform join
        if lsuffix == rsuffix:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.TDMLDF_INVALID_TABLE_ALIAS, "'lsuffix' and 'rsuffix'"),
                MessageCodes.TDMLDF_INVALID_TABLE_ALIAS)

        if how_lc != "cross":
            if isinstance(on, str):
                on = [on]
            if isinstance(on, ColumnExpression):
                on = [on]

            if not isinstance(on, list):
                raise TeradataMlException(
                    Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "on",
                        "str (or) ColumnExpression (or) List of strings(str) or ColumnExpressions"),
                    MessageCodes.TDMLDF_UNKNOWN_TYPE)

            all_join_conditions = []
            invalid_join_conditions = []
            # Forming join condition
            for condition in on:
                # Process only when the on condition is string or a ColumneExpression
                if isinstance(condition, str) or isinstance(condition, ColumnExpression):
                    if isinstance(condition, ColumnExpression):
                        condition = condition.compile()

                    for op in TeradataConstants.TERADATA_JOIN_OPERATORS.value:
                        if op in condition:
                            conditional_separator = op
                            break
                    else:
                        # If no join condition is mentioned, default is taken as equal.
                        # If on is ['a'], then it is equal to 'df1.a = df2.a'
                        condition = "{0} = {0}".format(condition)
                        conditional_separator = "="

                    columns = [column.strip() for column in condition.split(sep=conditional_separator)
                            if len(column) > 0]
                    if len(columns) != 2:
                        invalid_join_conditions.append(condition)
                    else:
                        left_col = self.__add_alias_to_column(columns[0], self.columns, lsuffix, "left")
                        right_col = self.__add_alias_to_column(columns[1], other.columns, rsuffix, "right")
                        if conditional_separator == "!=":
                            # "!=" is python way of expressing 'not equal to'. "<>" is Teradata way of
                            # expressing 'not equal to'. Adding support for "!=".
                            conditional_separator = "<>"
                        all_join_conditions.append('{0} {1} {2}'.format(left_col, conditional_separator, right_col))
                else:
                    invalid_join_conditions.append(str(condition))

            if len(invalid_join_conditions) > 0:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INVALID_JOIN_CONDITION,
                            ", ".join(invalid_join_conditions)), MessageCodes.TDMLDF_INVALID_JOIN_CONDITION)

            join_condition = " and ".join(all_join_conditions)
        else:
            join_condition = ""

        df1_columns_types = df_utils._get_required_columns_types_from_metaexpr(self._metaexpr)
        df2_columns_types = df_utils._get_required_columns_types_from_metaexpr(other._metaexpr)

        select_columns = []
        new_metaexpr_columns_types = OrderedDict()

        for column in self.columns:
            if df_utils._check_column_exists(column, other.columns):
                df1_column_with_suffix = self.__check_and_return_new_column_name(lsuffix, column, other.columns, "right")
                select_columns.append("{0} as {1}".format(self.__add_suffix(column,lsuffix),df1_column_with_suffix))

                df2_column_with_suffix = self.__check_and_return_new_column_name(rsuffix, column, self.columns, "left")
                select_columns.append("{0} as {1}".format(self.__add_suffix(column, rsuffix),df2_column_with_suffix))

                # As we are creating new column name, adding it to new metadata dict for new dataframe from join
                self.__add_column_type_item_to_dict(new_metaexpr_columns_types,
                                               UtilFuncs._teradata_unquote_arg(df1_column_with_suffix, "\""), column, df1_columns_types)
                self.__add_column_type_item_to_dict(new_metaexpr_columns_types,
                                                    UtilFuncs._teradata_unquote_arg(df2_column_with_suffix, "\""), column, df2_columns_types)
            else:
                # As column not present in right dataframe, directly adding column to new metadata dict.
                self.__add_column_type_item_to_dict(new_metaexpr_columns_types,
                                                    column, column, df1_columns_types)
                select_columns.append(UtilFuncs._teradata_quote_arg(column, "\"", False))

        for column in other.columns:
            if not df_utils._check_column_exists(column, self.columns):
                # As column not present in left dataframe, directly adding column to new metadata dict.
                self.__add_column_type_item_to_dict(new_metaexpr_columns_types,
                                                    column, column, df2_columns_types)
                select_columns.append(UtilFuncs._teradata_quote_arg(column, "\"", False))

        join_node_id = self._aed_utils._aed_join(self._nodeid, other._nodeid, ", ".join(select_columns),
                                                 how_lc, join_condition, lsuffix, rsuffix)

        # Forming metadata expression
        meta = sqlalchemy.MetaData()

        # Creting sqlalchemy table expression
        t = Table(join_node_id, meta,
                  *(Column(col_name, col_type) for col_name, col_type in new_metaexpr_columns_types.items()))

        return DataFrame._from_node(join_node_id, _MetaExpression(t), self._index_label)

    def __add_alias_to_column(self, column, df_columns, alias, df_side):
        """
        This function check column exists in list of columns, if exists add suffix to column and
        adds to join columns list.

        PARAMETERS:
            column  - Column name.
            self_columns - List of left dataframe columns.
            other_columns - List of right dataframe columns.
            alias - alias to be added to column.
            df_side - Position of data frame in join (left or right).

        EXAMPLES:
            df1 = DataFrame("table1")
            df2 = DataFrame("table2")
            __add_alias_to_column("a", df1.columns, df2.columns, "t1", "left")

        RAISES:
            TDMLDF_COLUMN_NOT_FOUND
        """
        if df_utils._check_column_exists(column, df_columns):
            return  self.__add_suffix(column, alias)
        else:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.TDMLDF_COLUMN_NOT_FOUND, column, df_side),
                MessageCodes.TDMLDF_COLUMN_NOT_FOUND)

    def __add_suffix(self, column, alias):
        """
        Adds alias to column

        PARAMETERS:
            column  - Column name.
            alias - alias to be appended to column.

        EXAMPLES:
            __add_suffix("a", "t1")

        RAISES:
            None
        """
        return "{0}.{1}".format(UtilFuncs._teradata_quote_arg(alias, "\"", False),
                                UtilFuncs._teradata_quote_arg(column, "\"", False))

    def __check_and_return_new_column_name(self, suffix, column, col_list, df_side):
        """
         Check new column name alias with column exists in col_list or not, if exists throws exception else
         returns new column name.

         PARAMETERS:
             suffix  - alias to be added to column.
             column - column name.
             col_list - list of columns to check in which new column is exists or not.
             df_side - Side of the dataframe.

         EXAMPLES:
             df = DataFrame("t1")
             __check_and_return_new_column_name("df1", "column_name", df.columns, "right")

         RAISES:
             None
         """
        df1_column_with_suffix = "{0}_{1}".format(suffix,
                                                  UtilFuncs._teradata_unquote_arg(column, "\""))
        if df_utils._check_column_exists(df1_column_with_suffix, col_list):
            if df_side == "right":
                suffix_side = "lsuffix"
            else:
                suffix_side = "rsuffix"
            raise TeradataMlException(
                Messages.get_message(MessageCodes.TDMLDF_COLUMN_ALREADY_EXISTS, df1_column_with_suffix, df_side,
                                     suffix_side),
                MessageCodes.TDMLDF_COLUMN_ALREADY_EXISTS)
        return UtilFuncs._teradata_quote_arg(df1_column_with_suffix, "\"", False)

    def __add_column_type_item_to_dict(self, new_metadata_dict, new_column,column, column_types):
        """
        Add a column as key and datatype as a value to dictionary

        PARAMETERS:
            new_metadata_dict  - Dictionary to which new item to be added.
            new_column - key fo new item.
            column - column to which datatype to be get.
            column_types - datatypes of the columns.
        EXAMPLES:
            __add_to_column_types_dict( metadata_dict, "col1","integer")

        RAISES:
            None
        """
        try:
            new_metadata_dict[new_column] = column_types[column]
        except KeyError:
            try:
                new_metadata_dict[new_column] = column_types[UtilFuncs._teradata_quote_arg(column, "\"", False)]
            except KeyError:
                new_metadata_dict[new_column] = column_types[UtilFuncs._teradata_unquote_arg(column, "\"")]

    def __get_sorted_list(self, colnames_list, ascending, kind):
        """
        Private method to return sorted list with different algoritms in either ascending or decending order.
        
        PARAMETERS:
            colnames_list - List of values to be sorted
            ascending - Specifies a flag to sort columns in either ascending (True) or descending (False).
            kind - Type of sorting algorithm to be applied upon.            
        
        EXAMPLES:
            __get_sorted_list(colnames_list, False, 'mergesort')
            
        RAISES:
            None
            
        RETURNS:
            Sorted list of column names
        """
        if kind == 'quicksort':
            less = []
            equal = []
            greater = []
            if len(colnames_list) > 1:
                pivot = colnames_list[0]
                for col in colnames_list:
                    if col < pivot:
                        less.append(col)
                    elif col == pivot:
                        equal.append(col)
                    else:
                        greater.append(col)
                greater = self.__get_sorted_list(greater, ascending=ascending, kind=kind)
                less = self.__get_sorted_list(less, ascending=ascending, kind=kind)
                if ascending:
                    final = less + equal + greater
                else:
                    final = greater + equal + less
                return final
            else:
                return colnames_list
            
        elif kind == 'mergesort':
            if ascending == True:
                return sorted(colnames_list)
            else:
                return sorted(colnames_list, reverse=True)     
            
        elif kind == 'heapsort':
            end = len(colnames_list)  
            start = end // 2 - 1
            for i in range(start, -1, -1):   
                self.__get_heap(colnames_list, end, i)   
            for i in range(end-1, 0, -1):  
                #swap(i, 0)  
                colnames_list[i], colnames_list[0] = colnames_list[0], colnames_list[i]
                colnames_list = self.__get_heap(colnames_list, i, 0)
            if ascending == True:
                return colnames_list
            else:
                return colnames_list[::-1]

    def __get_heap(self, colnames_list, n, i):
        """
        Private method to make a subtree rooted at index i.
        
        PARAMETERS:
            colnames_list - List of values for which heap is to be created.
            n - Size of the heap.
            i - Index to be taken as a root.
            
        EXAMPLES:
            __get_heap(colnames_list, 5, 3)
            
        RAISES:
            None
            
        RETURNS:
            Sorted list of column names indexed at i
        """
        l=2 * i + 1
        r=2 * (i + 1) 
        max=i
        if l < n and colnames_list[i] < colnames_list[l]:
            max = l
        if r < n and colnames_list[max] < colnames_list[r]:
            max = r
        if max != i:
            colnames_list[i], colnames_list[max] = colnames_list[max], colnames_list[i]
            self.__get_heap(colnames_list, n, max)
        return colnames_list

    def to_sql(self, table_name, if_exists='fail', primary_index=None, temporary=False, schema_name=None, types = None,
               primary_time_index_name=None, timecode_column=None, timebucket_duration=None,
               timezero_date=None, columns_list=[], sequence_column=None, seq_max=None, set_table=False):
        """
        DESCRIPTION:
            Writes records stored in a teradataml DataFrame to Teradata Vantage.

        PARAMETERS:

            table_name:
                Required Argument.
                Specifies the name of the table to be created in Teradata Vantage.
                Types: str

            schema_name:
                Optional Argument.
                Specifies the name of the SQL schema in Teradata Vantage to write to.
                Default Value: None (Use default Teradata Vantage schema).
                Types: str

                Note: schema_name will be ignored when temporary=True.

            if_exists:
                Optional Argument.
                Specifies the action to take when table already exists in Teradata Vantage.
                Default Value: 'fail'
                Permitted Values: 'fail', 'replace', 'append'
                    - fail: If table exists, do nothing.
                    - replace: If table exists, drop it, recreate it, and insert data.
                    - append: If table exists, insert data. Create if does not exist.
                Types: str

                Note: Replacing a table with the contents of a teradataml DataFrame based on
                      the same underlying table is not supported.

            primary_index:
                Optional Argument.
                Creates Teradata Table(s) with Primary index column(s) when specified.
                When None, No Primary Index Teradata tables are created.
                Default Value: None
                Types: str or List of Strings (str)
                    Example:
                        primary_index = 'my_primary_index'
                        primary_index = ['my_primary_index1', 'my_primary_index2', 'my_primary_index3']

            temporary:
                Optional Argument.
                Creates Teradata SQL tables as permanent or volatile.
                When True,
                1. volatile tables are created, and
                2. schema_name is ignored.
                When False, permanent tables are created.
                Default Value: False
                Types: boolean
                
            types:
                Optional Argument.
                Specifies required data-types for requested columns to be saved in Vantage.
                This argument accepts a dictionary of columns names and their required teradata types
                as key-value pairs; allowing to specify a subset of the columns of a specific type.
                When only a subset of all columns are provided, the rest are defaulted to appropriate types.
                When types argument is not provided, all column types are appropriately assigned and defaulted.
                Default Value: None
                Type: Python dictionary ({column_name1: type_value1, ... column_nameN: type_valueN})

            primary_time_index_name:
                Optional Argument.
                Specifies a name for the Primary Time Index (PTI) when the table
                to be created must be a PTI table.
                Type: String

                Note: This argument is not required or used when the table to be created
                      is not a PTI table. It will be ignored if specified without the timecode_column.

            timecode_column:
                Optional argument.
                Required when the DataFrame must be saved as a PTI table.
                Specifies the column in the DataFrame that reflects the form
                of the timestamp data in the time series.
                This column will be the TD_TIMECODE column in the table created.
                It should be of SQL type TIMESTAMP(n), TIMESTAMP(n) WITH TIMEZONE, or DATE,
                corresponding to Python types datetime.datetime or datetime.date.
                Type: String

                Note: When you specify this parameter, an attempt to create a PTI table
                      will be made. This argument is not required when the table to be created
                      is not a PTI table. If this argument is specified, primary_index will be ignored.

            timezero_date:
                Optional Argument.
                Used when the DataFrame must be saved as a PTI table.
                Specifies the earliest time series data that the PTI table will accept;
                a date that precedes the earliest date in the time series data.
                Value specified must be of the following format: DATE 'YYYY-MM-DD'
                Default Value: DATE '1970-01-01'.
                Type: String

                Note: This argument is not required or used when the table to be created
                      is not a PTI table. It will be ignored if specified without the timecode_column.

            timebucket_duration:
                Optional Argument.
                Required if columns_list is not specified or is empty.
                Used when the DataFrame must be saved as a PTI table.
                Specifies a duration that serves to break up the time continuum in
                the time series data into discrete groups or buckets.
                Specified using the formal form time_unit(n), where n is a positive
                integer, and time_unit can be any of the following:
                CAL_YEARS, CAL_MONTHS, CAL_DAYS, WEEKS, DAYS, HOURS, MINUTES,
                SECONDS, MILLISECONDS, or MICROSECONDS.
                Type:  String

                Note: This argument is not required or used when the table to be created
                      is not a PTI table. It will be ignored if specified without the timecode_column.

            columns_list:
                Optional Argument.
                Required if timebucket_duration is not specified.
                Used when the DataFrame must be saved as a PTI table.
                Specifies a list of one or more PTI table column names.
                Type: String or list of Strings

                Note: This argument is not required or used when the table to be created
                      is not a PTI table. It will be ignored if specified without the timecode_column.

            sequence_column:
                Optional Argument.
                Used when the DataFrame must be saved as a PTI table.
                Specifies the column of type Integer containing the unique identifier for
                time series data readings when they are not unique in time.
                * When specified, implies SEQUENCED, meaning more than one reading from the same
                  sensor may have the same timestamp.
                  This column will be the TD_SEQNO column in the table created.
                * When not specified, implies NONSEQUENCED, meaning there is only one sensor reading
                  per timestamp.
                  This is the default.
                Type: str

                Note: This argument is not required or used when the table to be created
                      is not a PTI table. It will be ignored if specified without the timecode_column.

            seq_max:
                Optional Argument.
                Used when the DataFrame must be saved as a PTI table.
                Specifies the maximum number of sensor data rows that can have the
                same timestamp. Can be used when 'sequenced' is True.
                Accepted range:  1 - 2147483647.
                Default Value: 20000.
                Type: int

                Note: This argument is not required or used when the table to be created
                      is not a PTI table. It will be ignored if specified without the timecode_column.

            set_table:
                Optional Argument.
                Specifies a flag to determine whether to create a SET or a MULTISET table.
                When True, a SET table is created.
                When False, a MULTISET table is created.
                Default value: False
                Type: boolean

                Note: 1. Specifying set_table=True also requires specifying primary_index or timecode_column.
                      2. Creating SET table (set_table=True) may result in loss of duplicate rows.
                      3. This argument has no effect if the table already exists and if_exists='append'.

        RETURNS:
            None

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df2 = df[(df.gpa == 4.00)]
            >>> df2.to_sql('to_sql_example', primary_index='id')
            >>> df3 = DataFrame('to_sql_example')
            >>> df3
               masters  gpa     stats programming admitted
            id
            13      no  4.0  Advanced      Novice        1
            29     yes  4.0    Novice    Beginner        0
            15     yes  4.0  Advanced    Advanced        1
            >>>
            >>> # Save as PTI table making sure it is a SET table
            >>> load_example_data("sessionize", "sessionize_table")
            >>> df4 = DataFrame('sessionize_table')
            >>> df4.to_sql("test_copyto_pti",
                           timecode_column='clicktime',
                           columns_list='event',
                           set_table=True
                          )
            >>> df5 = DataFrame('test_copyto_pti')
            >>> df5
                                    TD_TIMECODE partition_id adid productid
            event
            click    2009-07-04 09:18:17.000000         1231    1      1001
            click    2009-07-24 04:18:10.000000         1167    2      1001
            click    2009-08-08 02:18:12.000000         9231    3      1001
            click    2009-08-11 00:01:24.000000         9231    3      1001
            page_02  2009-08-22 04:20:05.000000         1039    5      1001
            page_02  2009-08-27 23:03:05.000000         1039    5      1001
            view     2009-02-09 15:17:59.000000         1263    4      1001
            view     2009-03-09 21:17:59.000000         1199    2      1001
            view     2009-03-13 17:17:59.000000         1071    4      1001
            view     2009-03-19 01:17:59.000000         1199    1      1001

        """

        return copy_to_sql(df = self, table_name = table_name, schema_name = schema_name,
                    index = False, index_label = None, temporary = temporary,
                    primary_index = primary_index, if_exists = if_exists, types = types,
                    primary_time_index_name = primary_time_index_name, timecode_column = timecode_column,
                    timebucket_duration = timebucket_duration, timezero_date = timezero_date, columns_list = columns_list,
                    sequence_column = sequence_column, seq_max = seq_max, set_table = set_table)

    def assign(self, drop_columns = False, **kwargs):
        """
        DESCRIPTION:
            Assign new columns to a teradataml DataFrame

        PARAMETERS:

             drop_columns:
                Optional Argument.
                If True, drop columns that are not specified in assign.
                Default Value: False
                Types: bool

             kwargs: keyword, value pairs
                 - keywords are the column names.
                 - values can be column arithmetic expressions and int/float/string literals.

        RETURNS:
             teradataml DataFrame
             A new DataFrame with the new columns in addition to
             all the existing columns if drop_columns is equal to False.
             Otherwise, if drop_columns = True, a new DataFrame with only columns in kwargs.

        NOTES:
             - The values in kwargs cannot be callable (functions).
             - The original DataFrame is not modified.
             - Since ``kwargs`` is a dictionary, the order of your
               arguments may not be preserved. To make things predicatable,
               the columns are inserted in alphabetical order, at the end of
               your DataFrame. Assigning multiple columns within the same
               ``assign`` is possible, but you cannot reference other columns
               created within the same ``assign`` call.
             - The maximum number of columns in a DataFrame is 2048.

        RAISES:
             1. ValueError - When a value that is callable is given in kwargs.
             2. ValueError - When columns of different dataframes are given in ColumnExpression.
             3. TeradataMlException - When there is an internal error in DataFrame or invalid
                                      argument type.

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> c1 = df.gpa
            >>> c2 = df.id
            >>>
            >>> df.assign(new_column = c1 + c2).sort("id")
               masters   gpa     stats programming admitted  new_column
            id
            1      yes  3.95  Beginner    Beginner        0        4.95
            2      yes  3.76  Beginner    Beginner        0        5.76
            3       no  3.70    Novice    Beginner        1        6.70
            4      yes  3.50  Beginner      Novice        1        7.50
            5       no  3.44    Novice      Novice        0        8.44
            6      yes  3.50  Beginner    Advanced        1        9.50
            7      yes  2.33    Novice      Novice        1        9.33
            8       no  3.60  Beginner    Advanced        1       11.60
            9       no  3.82  Advanced    Advanced        1       12.82
            10      no  3.71  Advanced    Advanced        1       13.71
            >>> df.assign(new_column = c1 * c2).sort("id")
               masters   gpa     stats programming admitted  new_column
            id
            1      yes  3.95  Beginner    Beginner        0        3.95
            2      yes  3.76  Beginner    Beginner        0        7.52
            3       no  3.70    Novice    Beginner        1       11.10
            4      yes  3.50  Beginner      Novice        1       14.00
            5       no  3.44    Novice      Novice        0       17.20
            6      yes  3.50  Beginner    Advanced        1       21.00
            7      yes  2.33    Novice      Novice        1       16.31
            8       no  3.60  Beginner    Advanced        1       28.80
            9       no  3.82  Advanced    Advanced        1       34.38
            10      no  3.71  Advanced    Advanced        1       37.10
            >>> df.assign(new_column = c2 / c1).sort("id")
               masters   gpa     stats programming admitted  new_column
            id
            1      yes  3.95  Beginner    Beginner        0    0.253165
            2      yes  3.76  Beginner    Beginner        0    0.531915
            3       no  3.70    Novice    Beginner        1    0.810811
            4      yes  3.50  Beginner      Novice        1    1.142857
            5       no  3.44    Novice      Novice        0    1.453488
            6      yes  3.50  Beginner    Advanced        1    1.714286
            7      yes  2.33    Novice      Novice        1    3.004292
            8       no  3.60  Beginner    Advanced        1    2.222222
            9       no  3.82  Advanced    Advanced        1    2.356021
            10      no  3.71  Advanced    Advanced        1    2.695418
            >>> df.assign(new_column = c1 - c2).sort("id")
               masters   gpa     stats programming admitted  new_column
            id
            1      yes  3.95  Beginner    Beginner        0        2.95
            2      yes  3.76  Beginner    Beginner        0        1.76
            3       no  3.70    Novice    Beginner        1        0.70
            4      yes  3.50  Beginner      Novice        1       -0.50
            5       no  3.44    Novice      Novice        0       -1.56
            6      yes  3.50  Beginner    Advanced        1       -2.50
            7      yes  2.33    Novice      Novice        1       -4.67
            8       no  3.60  Beginner    Advanced        1       -4.40
            9       no  3.82  Advanced    Advanced        1       -5.18
            10      no  3.71  Advanced    Advanced        1       -6.29
            >>> df.assign(new_column = c2 % c1).sort("id")
               masters   gpa     stats programming admitted  new_column
            id
            1      yes  3.95  Beginner    Beginner        0        1.00
            2      yes  3.76  Beginner    Beginner        0        2.00
            3       no  3.70    Novice    Beginner        1        3.00
            4      yes  3.50  Beginner      Novice        1        0.50
            5       no  3.44    Novice      Novice        0        1.56
            6      yes  3.50  Beginner    Advanced        1        2.50
            7      yes  2.33    Novice      Novice        1        0.01
            8       no  3.60  Beginner    Advanced        1        0.80
            9       no  3.82  Advanced    Advanced        1        1.36
            10      no  3.71  Advanced    Advanced        1        2.58
            >>>
            >>> df.assign(c1 = c2, c2 = c1).sort("id")
               masters   gpa     stats programming admitted  c1    c2
            id
            1      yes  3.95  Beginner    Beginner        0   1  3.95
            2      yes  3.76  Beginner    Beginner        0   2  3.76
            3       no  3.70    Novice    Beginner        1   3  3.70
            4      yes  3.50  Beginner      Novice        1   4  3.50
            5       no  3.44    Novice      Novice        0   5  3.44
            6      yes  3.50  Beginner    Advanced        1   6  3.50
            7      yes  2.33    Novice      Novice        1   7  2.33
            8       no  3.60  Beginner    Advanced        1   8  3.60
            9       no  3.82  Advanced    Advanced        1   9  3.82
            10      no  3.71  Advanced    Advanced        1  10  3.71
            >>> df.assign(c3 = c1 + 1, c4 = c2 + 1).sort("id")
               masters   gpa     stats programming admitted    c3  c4
            id
            1      yes  3.95  Beginner    Beginner        0  4.95   2
            2      yes  3.76  Beginner    Beginner        0  4.76   3
            3       no  3.70    Novice    Beginner        1  4.70   4
            4      yes  3.50  Beginner      Novice        1  4.50   5
            5       no  3.44    Novice      Novice        0  4.44   6
            6      yes  3.50  Beginner    Advanced        1  4.50   7
            7      yes  2.33    Novice      Novice        1  3.33   8
            8       no  3.60  Beginner    Advanced        1  4.60   9
            9       no  3.82  Advanced    Advanced        1  4.82  10
            10      no  3.71  Advanced    Advanced        1  4.71  11
            >>>
            >>> df.assign(c1 = 1).sort("id")
               masters   gpa     stats programming admitted c1
            id
            1      yes  3.95  Beginner    Beginner        0  1
            2      yes  3.76  Beginner    Beginner        0  1
            3       no  3.70    Novice    Beginner        1  1
            4      yes  3.50  Beginner      Novice        1  1
            5       no  3.44    Novice      Novice        0  1
            6      yes  3.50  Beginner    Advanced        1  1
            7      yes  2.33    Novice      Novice        1  1
            8       no  3.60  Beginner    Advanced        1  1
            9       no  3.82  Advanced    Advanced        1  1
            10      no  3.71  Advanced    Advanced        1  1
            >>> df.assign(c3 = 'string').sort("id")
               masters   gpa     stats programming admitted      c3
            id
            1      yes  3.95  Beginner    Beginner        0  string
            2      yes  3.76  Beginner    Beginner        0  string
            3       no  3.70    Novice    Beginner        1  string
            4      yes  3.50  Beginner      Novice        1  string
            5       no  3.44    Novice      Novice        0  string
            6      yes  3.50  Beginner    Advanced        1  string
            7      yes  2.33    Novice      Novice        1  string
            8       no  3.60  Beginner    Advanced        1  string
            9       no  3.82  Advanced    Advanced        1  string
            10      no  3.71  Advanced    Advanced        1  string
            >>>
            >>> # + op is overidden for string columns
            ... df.assign(concatenated = "Completed? " + df.masters).sort("id")
               masters   gpa     stats programming admitted    concatenated
            id
            1      yes  3.95  Beginner    Beginner        0  Completed? yes
            2      yes  3.76  Beginner    Beginner        0  Completed? yes
            3       no  3.70    Novice    Beginner        1   Completed? no
            4      yes  3.50  Beginner      Novice        1  Completed? yes
            5       no  3.44    Novice      Novice        0   Completed? no
            6      yes  3.50  Beginner    Advanced        1  Completed? yes
            7      yes  2.33    Novice      Novice        1  Completed? yes
            8       no  3.60  Beginner    Advanced        1   Completed? no
            9       no  3.82  Advanced    Advanced        1   Completed? no
            10      no  3.71  Advanced    Advanced        1   Completed? no
            >>>
            >>> # setting drop_columns to True will only return assigned expressions
            ... df.assign(drop_columns = True, c1 = 1)
              c1
            0  1
            1  1
            2  1
            3  1
            4  1
            5  1
            6  1
            7  1
            8  1
            9  1
            >>>
        """
        # handle invalid inputs and empty input
        if not isinstance(drop_columns, bool):

            err_msg_code = MessageCodes.UNSUPPORTED_DATATYPE
            err = Messages.get_message(err_msg_code, "drop_columns", "bool")
            raise TeradataMlException(err, err_msg_code)

        if len(kwargs) == 0:
            return self

        elif len(kwargs) >= TeradataConstants['TABLE_COLUMN_LIMIT'].value:
            errcode = MessageCodes.TD_MAX_COL_MESSAGE
            raise TeradataMlException(Messages.get_message(errcode), errcode)

        allowed_types = (type(None), int, float, str, decimal.Decimal, ColumnExpression)

        for key, val in kwargs.items():

            if isinstance(val, ColumnExpression) and val.get_flag_has_multiple_dataframes():
                raise ValueError("Combining Columns from different dataframes is unsupported for "
                                 "assign operation.")

            is_allowed = lambda x: isinstance(*x) and type(x[0]) != bool
            value_type_allowed = map(is_allowed, ((val, t) for t in allowed_types))

            if callable(val):
                err = 'Unsupported callable value for key: {}'.format(key)
                raise ValueError(err)

            elif not any(list(value_type_allowed)):
                err = 'Unsupported values of type {t} for key {k}'.format(k = key, t = type(val))
                raise ValueError(err)

        if self._metaexpr is None:
            msg = Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR)
            raise TeradataMlException(msg, MessageCodes.TDMLDF_INFO_ERROR)

        try:

            # apply the assign expression
            (new_meta, result) = self._metaexpr._assign(drop_columns, **kwargs)

            # join the expressions in result
            assign_expression = ', '.join(list(map(lambda x: x[1], result)))
            new_nodeid = self._aed_utils._aed_assign(self._nodeid,
                                                     assign_expression,
                                                     AEDConstants.AED_ASSIGN_DROP_EXISITING_COLUMNS.value)
            return DataFrame._from_node(new_nodeid, new_meta, self._index_label)

        except Exception as err:
            errcode = MessageCodes.TDMLDF_INFO_ERROR
            msg = Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR)
            raise TeradataMlException(msg, errcode) from err

    def get(self, key):
        """
        DESCRIPTION:
            Retrieve required columns from DataFrame using column name(s) as key.
            Returns a new teradataml DataFrame with requested columns only.

        PARAMETERS:

            key:
                Required Argument.
                Specifies column(s) to retrieve from the teradataml DataFrame.
                Types: str OR List of Strings (str)

            teradataml supports the following formats (only) for the "get" method:

            1] Single Column String: df.get("col1")
            2] Single Column List: df.get(["col1"])
            3] Multi-Column List: df.get(['col1', 'col2', 'col3'])
            4] Multi-Column List of List: df.get([["col1", "col2", "col3"]])

            Note: Multi-Column retrieval of the same column such as df.get(['col1', 'col1']) is not supported.

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df.sort('id')
               masters   gpa     stats programming admitted
            id
            1      yes  3.95  Beginner    Beginner        0
            2      yes  3.76  Beginner    Beginner        0
            3       no  3.70    Novice    Beginner        1
            4      yes  3.50  Beginner      Novice        1
            ...

            1] Single String Column
            >>> df.get("gpa")
                gpa
            0  3.46
            1  3.52
            2  3.68
            3  3.65
            ...

            2] Single Column List
            >>> df.get(["gpa"])
                gpa
            0  3.46
            1  3.52
            2  3.68
            3  3.65
            ...

            3] Multi-Column List
            >>> df.get(["programming", "masters", "gpa"])
              programming masters   gpa
            0    Beginner     yes  3.46
            1      Novice      no  3.52
            2    Beginner      no  3.68
            3      Novice      no  3.65
            ...

            4] Multi-Column List of List
            >>> df.get([['programming', 'masters', 'gpa']])
              programming masters   gpa
            0    Advanced     yes  4.00
            1    Advanced     yes  3.45
            2    Beginner     yes  3.50
            3    Beginner     yes  4.00
            ...

        """
        return self.select(key)

    def set_index(self, keys, drop = True, append = False):
        """
        DESCCRIPTION:
            Assigns one or more existing columns as the new index to a teradataml DataFrame.

        PARAMETERS:

            keys:
                Required Argument.
                Specifies the column name or a list of column names to use as the DataFrame index.
                Types: str OR list of Strings (str)

            drop:
                Optional Argument.
                Specifies whether or not to display the column(s) being set as index as
                teradataml DataFrame columns anymore.
                When drop is True, columns are set as index and not displayed as columns.
                When drop is False, columns are set as index; but also displayed as columns.
                Note: When the drop argument is set to True, the column being set as index does not cease to
                      be a part of the underlying table upon which the teradataml DataFrame is based off.
                      A column that is dropped while being set as an index is merely not used for display
                      purposes anymore as a column of the teradataml DataFrame.
                Default Value: True
                Types: bool

            append:
                Optional Argument.
                Specifies whether or not to append requested columns to the existing index.
    `           When append is False, replaces existing index.
                When append is True, retains both existing & currently appended index.
                Default Value: False
                Types: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df.sort('id')
               masters   gpa     stats programming admitted
            id
            1      yes  3.95  Beginner    Beginner        0
            2      yes  3.76  Beginner    Beginner        0
            3       no  3.70    Novice    Beginner        1
            4      yes  3.50  Beginner      Novice        1
            5       no  3.44    Novice      Novice        0
            6      yes  3.50  Beginner    Advanced        1
            7      yes  2.33    Novice      Novice        1
            8       no  3.60  Beginner    Advanced        1
            9       no  3.82  Advanced    Advanced        1
            10      no  3.71  Advanced    Advanced        1

            >>> # Set new index.
            >>> df.set_index('masters').sort('id')
                     id   gpa     stats programming admitted
            masters
            yes       1  3.95  Beginner    Beginner        0
            yes       2  3.76  Beginner    Beginner        0
            no        3  3.70    Novice    Beginner        1
            yes       4  3.50  Beginner      Novice        1
            no        5  3.44    Novice      Novice        0
            yes       6  3.50  Beginner    Advanced        1
            yes       7  2.33    Novice      Novice        1
            no        8  3.60  Beginner    Advanced        1
            no        9  3.82  Advanced    Advanced        1
            no       10  3.71  Advanced    Advanced        1

            >>> # Set multiple indexes using list of columns
            >>> df.set_index(['masters', 'id']).sort('id')
                         gpa     stats programming admitted
            id masters
            1  yes      3.95  Beginner    Beginner        0
            2  yes      3.76  Beginner    Beginner        0
            3  no       3.70    Novice    Beginner        1
            4  yes      3.50  Beginner      Novice        1
            5  no       3.44    Novice      Novice        0
            6  yes      3.50  Beginner    Advanced        1
            7  yes      2.33    Novice      Novice        1
            8  no       3.60  Beginner    Advanced        1
            9  no       3.82  Advanced    Advanced        1
            10 no       3.71  Advanced    Advanced        1

            >>> # Append to new index to the existing set of index.
            >>> df.set_index(['masters', 'id']).set_index('gpa', drop = False, append = True).sort('id')
                                stats programming admitted
            gpa  masters id
            3.95 yes     1   Beginner    Beginner        0
            3.76 yes     2   Beginner    Beginner        0
            3.70 no      3     Novice    Beginner        1
            3.50 yes     4   Beginner      Novice        1
            3.44 no      5     Novice      Novice        0
            3.50 yes     6   Beginner    Advanced        1
            2.33 yes     7     Novice      Novice        1
            3.60 no      8   Beginner    Advanced        1
            3.82 no      9   Advanced    Advanced        1
            3.71 no      10  Advanced    Advanced        1
            >>>
        """
        try:
            if drop not in (True, False):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "drop", "Boolean (True/False)"),
                                          MessageCodes.UNSUPPORTED_DATATYPE)

            if append not in (True, False):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "append", "Boolean (True/False)"),
                                          MessageCodes.UNSUPPORTED_DATATYPE)

            if not (isinstance(keys, str) or isinstance(keys, list)):
                raise TeradataMlException(
                    Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "keys", "String or List of strings"),
                    MessageCodes.UNSUPPORTED_DATATYPE)

            # Check & proceed only if keys (requested index_column) is a valid DataFrame column
            df_utils._check_column_in_dataframe(self, keys)

            new_index_list = self._index_label if self._index_label is not None else []

            # Creating a list with requested index labels bases on append
            if append:
                if isinstance(keys, str):
                    new_index_list.append(keys)
                elif isinstance(keys, list):
                    new_index_list.extend(keys)
            else:
                if isinstance(keys, str):
                    new_index_list = [keys]
                elif isinstance(keys, list):
                    new_index_list = keys

            # Takes care of appending already existing index
            new_index_list = list(set(new_index_list))

            # In case requested index is same as existing index, return same DF
            if new_index_list == self._index_label:
                return self

            # Creating list of undropped columns for printing
            undropped_columns = []
            if not drop:
                if isinstance(keys, str):
                    undropped_columns = [keys]
                elif isinstance(keys, list):
                    undropped_columns = keys

            if len(undropped_columns) == 0:
                undropped_columns = None

            # Assigning self attributes to newly created dataframe.
            new_df = DataFrame._from_node(self._nodeid, self._metaexpr, new_index_list, undropped_columns)
            new_df._table_name = self._table_name
            new_df._index = self._index
            return new_df

        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR),
                                      MessageCodes.TDMLDF_INFO_ERROR) from err

    def groupby(self, columns_expr):
        """
        DESCRIPTION:
            Apply GroupBy to one or more columns of a teradataml Dataframe
            The result will always behaves like calling groupby with as_index = False in pandas

        PARAMETERS:
            columns_expr:
                Required Argument.
                Specifies the column name(s) to group by.
                Types: str OR list of Strings (str)

        NOTES:
            Users can still apply teradataml DataFrame methods (filters/sort/etc) on top of the result.

        RETURNS:
            teradataml DataFrameGroupBy Object

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df1 = df.groupby(["masters"])
            >>> df1.min()
              masters min_id  min_gpa min_stats min_programming min_admitted
            0      no      3     1.87  Advanced        Advanced            0
            1     yes      1     1.98  Advanced        Advanced            0

        """
        try:
            column_list=[]
            unsupported_types = ['BLOB', 'CLOB', 'PERIOD_DATE', 'PERIOD_TIME', 'PERIOD_TIMESTAMP', 'ARRAY', 'VARRAY', 'XML', 'JSON']
            type_expr=[]
            invalid_types = []
            # check for consecutive groupby operations
            if isinstance(self, DataFrameGroupBy):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_OPERATION), MessageCodes.UNSUPPORTED_OPERATION)
            # validating columns which has to be a list/string for columns_expr
            if not ((isinstance(columns_expr, list) or (isinstance(columns_expr, str))) and all(isinstance(col, str) for col in columns_expr)):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "columns", ["list","str"]), MessageCodes.UNSUPPORTED_DATATYPE)
            if (isinstance(columns_expr, list)):
                if len(columns_expr) == 0:
                    raise TeradataMlException(Messages.get_message(MessageCodes.ARG_EMPTY, "columns_expr"), MessageCodes.ARG_EMPTY)
                else:
                    column_list=columns_expr
            elif (isinstance(columns_expr, str)):
                if columns_expr ==  "":
                    raise TeradataMlException(Messages.get_message(MessageCodes.ARG_EMPTY, "columns_expr"), MessageCodes.ARG_EMPTY)
                else:
                    column_list.append(columns_expr)
            # getting all the columns and data types for given metaexpr
            col_names, col_types = df_utils._get_column_names_and_types_from_metaexpr(self._metaexpr)
            # checking each element in columns_expr to be valid column in dataframe
            for col in column_list:
                if not df_utils._check_column_exists(col, col_names):
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDF_UNKNOWN_COLUMN, ": {}".format(col)), MessageCodes.TDF_UNKNOWN_COLUMN)
                else:
                    type_expr.append(self._metaexpr.t.c[col].type)
            # convert types to string from sqlalchemy type
            columns_types = [repr(type_expr[i]).split("(")[0] for i in range(len(type_expr))]
            # checking each element in passed columns_types to be valid a data type for groupby
            # and create a list of invalid_types
            for col_type in columns_types:
                if col_type in unsupported_types:
                    invalid_types.append(col_type)
            if len(invalid_types) > 0:
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, invalid_types, "ANY, except following {}".format(unsupported_types)), MessageCodes.UNSUPPORTED_DATATYPE)
            groupbyexpr = ', '.join(UtilFuncs._teradata_quote_arg(col, "\"", False) for col in column_list)
            groupbyObj = DataFrameGroupBy(self._nodeid, self._metaexpr, self._column_names_and_types, self.columns, groupbyexpr, column_list)
            return groupbyObj
        except TeradataMlException:
            raise

    def get_values(self, num_rows = 99999):
        """
        DESCRIPTION:
            Retrieves all values (only) present in a teradataml DataFrame.
            Values are retrieved as per a numpy.ndarray representation of a teradataml DataFrame.
            This format is equivalent to the get_values() representation of a Pandas DataFrame.

        PARAMETERS:
            num_rows:
                Optional Argument.
                Specifies the number of rows to retrieve values for from a teradataml DataFrame.
                The num_rows parameter specified needs to be an integer value.
                Default Value: 99999
                Types: int

        RETURNS:
            Numpy.ndarray representation of a teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","admissions_train")
            >>> df1 = DataFrame.from_table('admissions_train')
            >>> df1
               masters   gpa     stats programming admitted
            id
            15     yes  4.00  Advanced    Advanced        1
            7      yes  2.33    Novice      Novice        1
            22     yes  3.46    Novice    Beginner        0
            17      no  3.83  Advanced    Advanced        1
            13      no  4.00  Advanced      Novice        1
            38     yes  2.65  Advanced    Beginner        1
            26     yes  3.57  Advanced    Advanced        1
            5       no  3.44    Novice      Novice        0
            34     yes  3.85  Advanced    Beginner        0
            40     yes  3.95    Novice    Beginner        0

            # Retrieve all values from the teradataml DataFrame

            >>> vals = df1.get_values()
            >>> vals
            array([['yes', 4.0, 'Advanced', 'Advanced', 1],
                   ['yes', 3.45, 'Advanced', 'Advanced', 0],
                   ['yes', 3.5, 'Advanced', 'Beginner', 1],
                   ['yes', 4.0, 'Novice', 'Beginner', 0],
                                 . . .
                   ['no', 3.68, 'Novice', 'Beginner', 1],
                   ['yes', 3.5, 'Beginner', 'Advanced', 1],
                   ['yes', 3.79, 'Advanced', 'Novice', 0],
                   ['no', 3.0, 'Advanced', 'Novice', 0],
                   ['yes', 1.98, 'Advanced', 'Advanced', 0]], dtype=object)

            # Retrieve values for a given number of rows from the teradataml DataFrame

            >>> vals = df1.get_values(num_rows = 3)
            >>> vals
            array([['yes', 4.0, 'Advanced', 'Advanced', 1],
                   ['yes', 3.45, 'Advanced', 'Advanced', 0],
                   ['yes', 3.5, 'Advanced', 'Beginner', 1]], dtype=object)

            # Access specific values from the entire set received as per below:
            # Retrieve all values from an entire row (for example, the first row):

            >>> vals[0]
            array(['yes', 4.0, 'Advanced', 'Advanced', 1], dtype=object)

            # Alternatively, specify a range to retrieve values from  a subset of rows (For example, first 3 rows):

            >>> vals[0:3]
            array([['yes', 4.0, 'Advanced', 'Advanced', 1],
            ['yes', 3.45, 'Advanced', 'Advanced', 0],
            ['yes', 3.5, 'Advanced', 'Beginner', 1]], dtype=object)

            # Alternatively, retrieve all values from an entire column (For example, the first column):

            >>> vals[:, 0]
            array(['yes', 'yes', 'yes', 'yes', 'yes', 'no', 'yes', 'yes', 'yes',
                   'yes', 'no', 'no', 'yes', 'yes', 'no', 'yes', 'no', 'yes', 'no',
                   'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes',
                   'yes', 'yes', 'no', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no',
                   'yes'], dtype=object)

            # Alternatively, retrieve a single value from a given row and column (For example, 3rd row, and 2nd column):
            >>> vals[2,1]
            3.5

            Note:
            1) Row and column indexing starts from 0, so the first column = index 0, second column = index 1, and so on...

            2) When a Pandas DataFrame is saved to Teradata Vantage & retrieved back as a teradataml DataFrame, the get_values()
               method on a Pandas DataFrame and the corresponding teradataml DataFrames have the following type differences:
                   - teradataml DataFrame get_values() retrieves 'bool' type Pandas DataFrame values (True/False) as BYTEINTS (1/0)
                   - teradataml DataFrame get_values() retrieves 'Timedelta' type Pandas DataFrame values as equivalent values in seconds.

        """
        return self.to_pandas(self._index_label, num_rows).get_values()

    @property
    def shape(self):
        """
        Returns a tuple representing the dimensionality of the DataFrame.

        PARAMETERS:
            None

        RETURNS:
            Tuple representing the dimensionality of this DataFrame.

        Examples:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')
            >>> df
                          Feb   Jan   Mar   Apr  datetime
            accounts
            Orange Inc  210.0  None  None   250  04/01/2017
            Yellow Inc   90.0  None  None  None  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017
            Blue Inc     90.0    50    95   101  04/01/2017
            Jones LLC   200.0   150   140   180  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            >>> df.shape
            (6, 6)
            >>>

        RAISES:
            TeradataMlException (TDMLDF_INFO_ERROR)
        """
        try:
            # To know the number of rows in a DF, we need to execute the node
            # Generate/Execute AED nodes
            self.__execute_node_and_set_table_name(self._nodeid)

            # The dimension of the DF is (# of rows, # of columns)
            return df_utils._get_row_count(self._table_name), len(self._column_names_and_types)

        except TeradataMlException:
            raise

        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR),
                                      MessageCodes.TDMLDF_INFO_ERROR) from err

    @property
    def size(self):
        """
        Returns a value representing the number of elements in the DataFrame.

        PARAMETERS:
            None

        RETURNS:
            Value representing the number of elements in the DataFrame.

        Examples:
            >>> load_example_data("dataframe","sales")
            >>> df = DataFrame.from_table('sales')
            >>> df
                          Feb   Jan   Mar   Apr  datetime
            accounts
            Orange Inc  210.0  None  None   250  04/01/2017
            Yellow Inc   90.0  None  None  None  04/01/2017
            Red Inc     200.0   150   140  None  04/01/2017
            Blue Inc     90.0    50    95   101  04/01/2017
            Jones LLC   200.0   150   140   180  04/01/2017
            Alpha Co    210.0   200   215   250  04/01/2017
            >>> df.size
            36

        RAISES:
            None
        """
        dimension = self.shape
        return dimension[0] * dimension[1]

    def merge(self, right, on=None, how="inner", left_on=None, right_on=None, use_index=False,
              lsuffix=None, rsuffix=None):
        """
        DESCRIPTION:
            Merges two teradataml DataFrames together.
         
            Supported merge operations are:
                - inner: Returns only matching rows, non-matching rows are eliminated.
                - left: Returns all matching rows plus non-matching rows from the left teradataml DataFrame.
                - right: Returns all matching rows plus non-matching rows from the right teradataml DataFrame.
                - full: Returns all rows from both teradataml DataFrames, including non matching rows.

        PARAMETERS:
         
            right:
                Required argument.
                Specifies right teradataml DataFrame on which merge is to be performed.
                Types: teradataml DataFrame
            
            on:
                Optional argument.
                Specifies list of conditions that indicate the columns used for the merge.
                When no arguments are provided for this condition, the merge is performed using the indexes
                of the teradataml DataFrames. Both teradataml DataFrames are required to have index labels to
                perform a merge operation when no arguments are provided for this condition.
                When either teradataml DataFrame does not have a valid index label in the above case,
                an exception is thrown.
                Examples:
                    1. ["a","b"] indicates df1.a = df2.a and df1.b = df2.b.
                    2. ["a = b", "c = d"] indicates df1.a = df2.b and df1.c = df2.d
                Default Value: None
                Types: str or list of str

            how:
                Optional argument.
                Specifies the type of merge to perform. Supports inner, left, right, full and cross merge operations.
                When how is "cross", the arguments on, left_on, right_on and use_index are ignored.
                Default Value: "inner".
                Types: str
                      
            left_on:
                Optional argument.
                Specifies column to merge on, in the left teradataml DataFrame.
                When both the 'on' and 'left_on' parameters are unspecified, the index columns
                of the teradataml DataFrames are used to perform the merge operation.
                Default Value: None.
                Types: str or list of str
                      
            right_on:
                Optional argument.
                Specifies column to merge on, in the right teradataml DataFrame.
                When both the 'on' and 'right_on' parameters are unspecified, the index columns
                of the teradataml DataFrames are used to perform the merge operation.
                Default Value: None.
                Types: str or list of str
                       
            use_index:
                Optional argument.
                Specifies whether (or not) to use index from the teradataml DataFrames as the merge key(s).
                When False, and 'on', 'left_on', and 'right_on' are all unspecified, the index columns
                of the teradataml DataFrames are used to perform the merge operation.
                Default value: False.
                Types: bool
                         
            lsuffix:
                Optional argument.
                Specifies suffix to be added to the left table columns.
                Default Value: None.
                Types: str
                         
                Note: A suffix is required if teradataml DataFrames being merged have columns with the same name.
                      
            rsuffix:
                Optional argument.
                Specifies suffix to be added to the right table columns.
                Default Value: None.
                Types: str
                     
                Note: A suffix is required if teradataml DataFrames being merged have columns with the same name.

        RAISES:
            TeradataMlException

        RETURNS:
            teradataml DataFrame

        EXAMPLES:
            
            # Example set-up teradataml DataFrames for merge
            >>> from datetime import datetime, timedelta
            >>> dob = datetime.strptime('31101991', '%d%m%Y').date()
            
            >>> df1 = pd.DataFrame(data={'col1': [1, 2,3],
                           'col2': ['teradata','analytics','platform'],
                           'col3': [1.3, 2.3, 3.3],
                           'col5': ['a','b','c'],
                            'col 6': [dob, dob + timedelta(1), dob + timedelta(2)],
                            "'col8'":[3,4,5]})
            
            >>> df2 = pd.DataFrame(data={'col1': [1, 2, 3],
                                'col4': ['teradata', 'analytics', 'are you'],
                                'col3': [1.3, 2.3, 4.3],
                                 'col7':['a','b','d'],
                                 'col 6': [dob, dob + timedelta(1), dob + timedelta(3)],
                                 "'col8'": [3, 4, 5]})
            >>> # Persist the Pandas DataFrames in Vantage.
            >>> copy_to_sql(df1, "table1", primary_index="col1")
            >>> copy_to_sql(df2, "table2", primary_index="col1")
            >>> df1 = DataFrame("table1")
            >>> df2 = DataFrame("table2")
            >>> df1
                 'col8'       col 6       col2  col3 col5
            col1                                         
            2         4  1991-11-01  analytics   2.3    b
            1         3  1991-10-31   teradata   1.3    a
            3         5  1991-11-02   platform   3.3    c
            >>> df2
                 'col8'       col 6  col3       col4 col7
            col1                                         
            2         4  1991-11-01   2.3  analytics    b
            1         3  1991-10-31   1.3   teradata    a
            3         5  1991-11-03   4.3    are you    d            
            
            >>> # 1) Specify both types of 'on' conditions as well as teradataml DataFrame indexes as merge keys:
            >>> df1.merge(right = df2, how = "left", on = ["col3","col2=col4"], use_index = True, lsuffix = "t1", rsuffix = "t2")
            
              t2_col1 col5    t2_col 6 t1_col1 t2_'col8'  t1_col3       col4  t2_col3  col7       col2    t1_col 6 t1_'col8'
            0       2    b  1991-11-01       2         4      2.3  analytics      2.3     b  analytics  1991-11-01         4
            1       1    a  1991-10-31       1         3      1.3   teradata      1.3     a   teradata  1991-10-31         3
            2    None    c        None       3      None      3.3       None      NaN  None   platform  1991-11-02         5

            
            >>> # 2) Specify left_on, right_on conditions along with teradataml DataFrame indexes as merge keys:
            >>> df1.merge(right = df2, how = "right", left_on = "col2", right_on = "col4", use_index = True, lsuffix = "t1", rsuffix = "t2")
              t1_col1 t2_col1       col2  t1_col3  t2_col3  col5    t1_col 6    t2_col 6 t1_'col8' t2_'col8'       col4 col7
            0       2       2  analytics      2.3      2.3     b  1991-11-01  1991-11-01         4         4  analytics    b
            1       1       1   teradata      1.3      1.3     a  1991-10-31  1991-10-31         3         3   teradata    a
            2    None       3       None      NaN      4.3  None        None  1991-11-03      None         5    are you    d
            
            
            >>> # 3) If teradataml DataFrames to be merged do not contain common columns, lsuffix and rsuffix are not required:
            >>> new_df1 = df1.select(['col2', 'col5'])
            >>> new_df2 = df2.select(['col4', 'col7'])
            >>> new_df1
              col5       col2
            0    b  analytics
            1    a   teradata
            2    c   platform
            >>> new_df2
              col7       col4
            0    b  analytics
            1    a   teradata
            2    d    are you
            >>> new_df1.merge(right = new_df2, how = "inner", on = "col5=col7")
              col5       col4       col2 col7
            0    b  analytics  analytics    b
            1    a   teradata   teradata    a
            
            
            >>> # 4) When no merge conditions are specified, teradataml DataFrame indexes are used as merge keys.
            >>> df1.merge(right = df2, how = "full", lsuffix = "t1", rsuffix = "t2")
              t2_col1 col5    t2_col 6 t1_col1 t2_'col8'  t1_col3       col4  t2_col3 col7       col2    t1_col 6 t1_'col8'
            0       2    b  1991-11-01       2         4      2.3  analytics      2.3    b  analytics  1991-11-01         4
            1       1    a  1991-10-31       1         3      1.3   teradata      1.3    a   teradata  1991-10-31         3
            2       3    c  1991-11-03       3         5      3.3    are you      4.3    d   platform  1991-11-02         5
            
         """
        tdp = preparer(td_dialect)

        if not isinstance(right, DataFrame):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "right", "TeradataML DataFrame"),
                MessageCodes.UNSUPPORTED_DATATYPE)

        if on is not None and not isinstance(on, str) and not isinstance(on, list):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "on", "'str' or 'list of str'"),
                MessageCodes.UNSUPPORTED_DATATYPE)

        if left_on is not None and not isinstance(left_on, str) and not isinstance(left_on, list):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "left_on", "'str' or 'list of str'"),
                MessageCodes.UNSUPPORTED_DATATYPE)

        if right_on is not None and not isinstance(right_on, str) and not isinstance(right_on, list):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "right_on", "'str' or 'list of str'"),
                MessageCodes.UNSUPPORTED_DATATYPE)

        if (right_on is not None and left_on is None) or (right_on is None and left_on is not None):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.MUST_PASS_ARGUMENT, "left_on", "right_on"),
                MessageCodes.MUST_PASS_ARGUMENT)

        if not isinstance(use_index, bool):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "use_index", "bool"),
                MessageCodes.UNSUPPORTED_DATATYPE)

        if isinstance(on,list) and all(isinstance(elem, str) for elem in on):
            join_conditions = on
        elif isinstance(on, str):
            join_conditions = [on]
        else:
            join_conditions = []

        if isinstance(left_on, list) and isinstance(right_on, list) and len(left_on) != len(right_on):
            raise TeradataMlException(
                  Messages.get_message(MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS, "left_on", "right_on"),
                  MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS)

        elif isinstance(left_on, list) and isinstance(right_on, str) and len(left_on) != 1:
            raise TeradataMlException(
                  Messages.get_message(MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS, "left_on", "right_on"),
                  MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS)

        elif isinstance(right_on, list) and isinstance(left_on, str) and len(right_on) != 1:
            raise TeradataMlException(
                  Messages.get_message(MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS, "left_on", "right_on"),
                MessageCodes.TDMLDF_UNEQUAL_NUMBER_OF_COLUMNS)

        if left_on is not None and not isinstance(left_on, list):
            left_on = [left_on]

        if right_on is not None and not isinstance(right_on, list):
            right_on = [right_on]

        if left_on is not None and right_on is not None:
            for left_column, right_column in zip(left_on, right_on):
                join_conditions.append("{} = {}".format(tdp.quote(left_column), tdp.quote(right_column)))

        # If user did not pass any arguments which form join conditions,
        # Merge is performed using index columns of TeradataML DataFrames
        if on is None and left_on is None and right_on is None and not use_index:
            if self._index_label is None or right._index_label is None:
                raise TeradataMlException(
                    Messages.get_message(MessageCodes.TDMLDF_INDEXES_ARE_NONE), MessageCodes.TDMLDF_INDEXES_ARE_NONE)
            else:
                use_index = True

        if use_index:
            if self._index_label is None or right._index_label is None:
                    raise TeradataMlException(
                    Messages.get_message(MessageCodes.TDMLDF_INDEXES_ARE_NONE), MessageCodes.TDMLDF_INDEXES_ARE_NONE)

            left_index_labels = self._index_label
            right_index_labels = right._index_label
            if not isinstance(self._index_label, list):
                left_index_labels = [left_index_labels]
            if not isinstance(right._index_label, list):
                right_index_labels = [right_index_labels]

            for left_index_label, right_index_label in zip(left_index_labels, right_index_labels):
                join_conditions.append("{} = {}".format(tdp.quote(left_index_label), tdp.quote(right_index_label)))


        return self.join(other=right, on=join_conditions, how=how, lsuffix=lsuffix, rsuffix=rsuffix)

    def squeeze(self, axis=None):
        """
        DESCRIPTION:
            Squeeze one-dimensional axis objects into scalars.
            teradataml DataFrames with a single element are squeezed to a scalar.
            teradataml DataFrames with a single column are squeezed to a Series.
            Otherwise the object is unchanged.

            Note: Currently only '1' and 'None' are supported for axis.
                  For now with axis = 0, the teradataml DataFrame is returned.

        PARAMETERS:
            axis:
                Optional Argument.
                A specific axis to squeeze. By default, all axes with
                length equals one are squeezed.
                Permitted Values: 0 or 'index', 1 or 'columns', None
                Default: None

        RETURNS:
            teradataml DataFrame, teradataml Series, or scalar,
            the projection after squeezing 'axis' or all the axes.

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe", "admissions_train")
            >>> df = DataFrame("admissions_train")
            >>> df
               masters   gpa     stats programming admitted
            id
            22     yes  3.46    Novice    Beginner        0
            36      no  3.00  Advanced      Novice        0
            15     yes  4.00  Advanced    Advanced        1
            38     yes  2.65  Advanced    Beginner        1
            5       no  3.44    Novice      Novice        0
            17      no  3.83  Advanced    Advanced        1
            34     yes  3.85  Advanced    Beginner        0
            13      no  4.00  Advanced      Novice        1
            26     yes  3.57  Advanced    Advanced        1
            19     yes  1.98  Advanced    Advanced        0

            >>> gpa = df.select(["gpa"])
            >>> gpa.squeeze()
            0    4.00
            1    2.33
            2    3.46
            3    3.83
            4    4.00
            5    2.65
            6    3.57
            7    3.44
            8    3.85
            9    3.95
            Name: gpa, dtype: float64
            >>> gpa.squeeze(axis = 1)
            0    3.46
            1    3.00
            2    4.00
            3    2.65
            4    3.44
            5    3.83
            6    3.85
            7    4.00
            8    3.57
            9    1.98
            Name: gpa, dtype: float64
            >>> gpa.squeeze(axis = 0)
                gpa
            0  3.46
            1  3.00
            2  4.00
            3  2.65
            4  3.44
            5  3.83
            6  3.85
            7  4.00
            8  3.57
            9  1.98

            >>> df = DataFrame.from_query('select gpa, stats from admissions_train where gpa=2.33')
            >>> s = df.squeeze()
            >>> s
                gpa   stats
            0  2.33  Novice

            >>> single_gpa = DataFrame.from_query('select gpa from admissions_train where gpa=2.33')
            >>> single_gpa
                gpa
            0  2.33
            >>> single_gpa.squeeze()
            2.33
            >>> single_gpa.squeeze(axis = 1)
            0    2.33
            Name: gpa, dtype: float64
            >>> single_gpa.squeeze(axis = 0)
                gpa
            0  2.33
        """
        num_row, num_col = self.shape

        # Check if the number of elements in DF = 1
        if (num_row, num_col) == (1,1) and axis is None:
            # To get the single row/column value in the DF, we need to execute the node
            # Generate/Execute AED nodes
            self.__execute_node_and_set_table_name(self._nodeid)
            return df_utils._get_scalar_value(self._table_name)

        if axis is None:
            if num_col == 1:
                axis = 1
            elif num_row == 1:
                axis = 0
            else:
                return self
        else:
            # Check if axis has valid/expected value
            if (not isinstance(axis, str) and not isinstance(axis, numbers.Integral)) or \
               ((isinstance(axis, str) and axis not in ["index", "columns"]) or \
               (isinstance(axis, numbers.Integral) and axis not in [0, 1])):
                raise TeradataMlException(Messages.get_message(MessageCodes.SERIES_INVALID_AXIS, axis,
                                                               "0, 'index', 1, 'columns', None"),
                                          MessageCodes.SERIES_INVALID_AXIS)
            if isinstance(axis, str):
                # Set the integer value to use further for based on the string value
                if axis == "index":
                    axis = 0
                else:
                    axis = 1

            if (axis == 0 and num_row != 1) or \
               (axis == 1 and num_col != 1):
                return self

        if axis == 1:
            return Series._from_dataframe(self, axis = 1)
        else:
            # TODO : Research and add capabilities to handle rowexpression based return objects
            # For now, returning the DataFrame as is
            return self

    def sort_index(self, axis=0, ascending=True, kind='quicksort'):
        """
        DESCRIPTION:
            Get sorted object by labels (along an axis) in either ascending or descending order for a teradataml DataFrame.
                
        PARAMETERS:
            axis:
                Optional Argument.
                Specifies the value to direct sorting on index or columns. 
                Values can be either 0 ('rows') OR 1 ('columns'), value as 0 will sort on index (if no index is present then parent DataFrame will be returned)
                and value as 1 will sort on columns names (if no index is present then parent DataFrame will be returned with sorted columns) for the DataFrame. 
                Default value: 0
                Types: int
                
            ascending:
                Optional Argument.
                Specifies a flag to sort columns in either ascending (True) or descending (False).
                Default value: True
                Types: bool
            
            kind:
                Optional Argument.
                Specifies a value for desired algorithm to be used. 
                Permitted values: 'quicksort', 'mergesort' or 'heapsort'
                Default value: 'quicksort'
                Types: str

        RETURNS:
            teradataml DataFrame
        
        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> load_example_data("dataframe","scale_housing_test")
            >>> df = DataFrame.from_table('scale_housing_test')
            >>> df
                      id    price  lotsize  bedrooms  bathrms  stories
            types                                                     
            classic   14  36000.0   2880.0       3.0      1.0      1.0
            bungalow  11  90000.0   7200.0       3.0      2.0      1.0
            classic   15  37000.0   3600.0       2.0      1.0      1.0
            classic   13  27000.0   1700.0       3.0      1.0      2.0
            classic   12  30500.0   3000.0       2.0      1.0      1.0
            
            >>> df.sort_index()
                      id    price  lotsize  bedrooms  bathrms  stories
            types                                                     
            bungalow  11  90000.0   7200.0       3.0      2.0      1.0
            classic   13  27000.0   1700.0       3.0      1.0      2.0
            classic   12  30500.0   3000.0       2.0      1.0      1.0
            classic   14  36000.0   2880.0       3.0      1.0      1.0
            classic   15  37000.0   3600.0       2.0      1.0      1.0
            
            >>> df.sort_index(0)
                      id    price  lotsize  bedrooms  bathrms  stories
            types                                                     
            bungalow  11  90000.0   7200.0       3.0      2.0      1.0
            classic   13  27000.0   1700.0       3.0      1.0      2.0
            classic   12  30500.0   3000.0       2.0      1.0      1.0
            classic   14  36000.0   2880.0       3.0      1.0      1.0
            classic   15  37000.0   3600.0       2.0      1.0      1.0
            
            >>> df.sort_index(1, False) # here 'False' means DESCENDING for respective axis
                      stories    price  lotsize  id  bedrooms  bathrms
            types                                                     
            classic       1.0  36000.0   2880.0  14       3.0      1.0
            bungalow      1.0  90000.0   7200.0  11       3.0      2.0
            classic       1.0  37000.0   3600.0  15       2.0      1.0
            classic       2.0  27000.0   1700.0  13       3.0      1.0
            classic       1.0  30500.0   3000.0  12       2.0      1.0
            
            >>> df.sort_index(1, True, 'mergesort')
                      bathrms  bedrooms  id  lotsize    price  stories
            types                                                     
            classic       1.0       3.0  14   2880.0  36000.0      1.0
            bungalow      2.0       3.0  11   7200.0  90000.0      1.0
            classic       1.0       2.0  15   3600.0  37000.0      1.0
            classic       1.0       3.0  13   1700.0  27000.0      2.0
            classic       1.0       2.0  12   3000.0  30500.0      1.0

        """
        try:
            if axis not in (0, 1, 'columns', 'rows'):
                raise ValueError("axis must be either 0 ('rows') or 1 ('columns')")
            
            if not (isinstance(ascending, bool)):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "ascending", "bool"), MessageCodes.UNSUPPORTED_DATATYPE)
            
            if kind not in ('quicksort', 'mergesort', 'heapsort'):
                raise ValueError("kind must be a valid value from: 'quicksort', 'mergesort' or 'heapsort' ")
                
            if axis in (0, 'rows'):
                # For NoPI objects
                if self._index_label is None:
                    return self
                else:
                    return self.sort(self._index_label, ascending)
            else:
                colnames_list, coltypes_list = df_utils._get_column_names_and_types_from_metaexpr(self._metaexpr)
                colnames_list = self.__get_sorted_list(colnames_list, ascending=ascending, kind=kind)
                return self.select(colnames_list)
        except TeradataMlException:
            raise

    def concat(self, other, join='OUTER', allow_duplicates=True, sort=False):
        """
        DESCRIPTION:
            Concatenates two teradataml DataFrames along the index axis.

        PARAMETERS:
            other:
                Required argument.
                Specifies the other teradataml DataFrame with which the concatenation is to be performed.
                Type: teradataml DataFrame

            join:
                Optional argument.
                Specifies how to handle indexes on columns axis.
                The supported values are:
                • 'OUTER': It instructs the function to project all columns from both the DataFrames.
                           Columns not present in either DataFrame will have a SQL NULL value.
                • 'INNER': It instructs the function to project only the columns common to both DataFrames.
                Default value: 'OUTER'
                Permitted values: 'INNER', 'OUTER'
                Type: str

            allow_duplicates:
                Optional argument.
                Specifies if the result of concatenation can have duplicate rows.
                Default value: True
                Type: bool

            sort:
                Optional argument.
                Specifies a flag to sort the columns axis if it is not already aligned when join is ‘outer’.
                Default value: False
                Type: bool

        RETURNS:
            teradataml DataFrame

        RAISES:
            TeradataMlException

        EXAMPLES:
            >>> from teradataml import load_example_data
            >>> load_example_data("dataframe", "admissions_train")
            >>>
            >>> # Default options
            >>> df = DataFrame('admissions_train')
            >>> df1 = df[df.gpa == 4].select(['id', 'stats', 'masters', 'gpa'])
            >>> df1
                   stats masters  gpa
            id
            13  Advanced      no  4.0
            29    Novice     yes  4.0
            15  Advanced     yes  4.0
            >>> df2 = df[df.gpa < 2].select(['id', 'stats', 'programming', 'admitted'])
            >>> df2
                   stats programming admitted
            id
            24  Advanced      Novice        1
            19  Advanced    Advanced        0
            >>>
            >>> cdf = df1.concat(df2)
            >>> cdf
                   stats masters  gpa programming admitted
            id
            19  Advanced    None  NaN    Advanced        0
            24  Advanced    None  NaN      Novice        1
            13  Advanced      no  4.0        None     None
            29    Novice     yes  4.0        None     None
            15  Advanced     yes  4.0        None     None
            >>>
            >>> # join = 'inner'
            >>> cdf = df1.concat(df2, join='inner')
            >>> cdf
                   stats
            id
            19  Advanced
            24  Advanced
            13  Advanced
            29    Novice
            15  Advanced
            >>>
            >>> # allow_duplicates = True (default)
            >>> cdf = df1.concat(df2)
            >>> cdf
                   stats masters  gpa programming admitted
            id
            19  Advanced    None  NaN    Advanced        0
            24  Advanced    None  NaN      Novice        1
            13  Advanced      no  4.0        None     None
            29    Novice     yes  4.0        None     None
            15  Advanced     yes  4.0        None     None
            >>> cdf = cdf.concat(df2)
            >>> cdf
                   stats masters  gpa programming admitted
            id
            19  Advanced    None  NaN    Advanced        0
            13  Advanced      no  4.0        None     None
            24  Advanced    None  NaN      Novice        1
            24  Advanced    None  NaN      Novice        1
            19  Advanced    None  NaN    Advanced        0
            29    Novice     yes  4.0        None     None
            15  Advanced     yes  4.0        None     None
            >>>
            >>> # allow_duplicates = False
            >>> cdf = cdf.concat(df2, allow_duplicates=False)
            >>> cdf
                   stats masters  gpa programming admitted
            id
            19  Advanced    None  NaN    Advanced        0
            29    Novice     yes  4.0        None     None
            24  Advanced    None  NaN      Novice        1
            15  Advanced     yes  4.0        None     None
            13  Advanced      no  4.0        None     None
            >>>
            >>> # sort = True
            >>> cdf = df1.concat(df2, sort=True)
            >>> cdf
               admitted  gpa masters programming     stats
            id
            19        0  NaN    None    Advanced  Advanced
            24        1  NaN    None      Novice  Advanced
            13     None  4.0      no        None  Advanced
            29     None  4.0     yes        None    Novice
            15     None  4.0     yes        None  Advanced

        """
        concat_join_permitted_values = ['INNER', 'OUTER']

        awu = AnalyticsWrapperUtils()
        awu_matrix = []
        awu_matrix.append(["other", other, False, (DataFrame)])
        awu_matrix.append(["join", join, False, (str)])
        awu_matrix.append(["allow_duplicates", allow_duplicates, False, (bool)])
        awu_matrix.append(["sort", sort, False, (bool)])

        # Validate argument types
        awu._validate_argument_types(awu_matrix)
        awu._validate_input_table_argument(other, 'other')

        # Validate empty arguments
        awu._validate_input_columns_not_empty(join, "join")

        # Validate permitted values
        awu._validate_permitted_values(join, concat_join_permitted_values, "join")

        # Generate the columns and their type to output, and check if the evaluation has to be lazy
        master_columns_dict, is_lazy = self.__check_concat_compatibility(other, join, sort)

        # If the result has no columns, i.e. no data
        if len(master_columns_dict) < 1:
            raise TeradataMlException(Messages.get_message(MessageCodes.EMPTY_DF_RETRIEVED),
                                      MessageCodes.EMPTY_DF_RETRIEVED)

        try:
            aed_utils = AedUtils()
            meta = sqlalchemy.MetaData()

            col_list = []
            # The iteration currently is for two objects, hence range(2)
            for i in range(2):
                col_list.append([])

            # Now create the list of columns for each DataFrame to concatenate
            type_compiler = td_type_compiler(td_dialect)
            for col_name, value in master_columns_dict.items():
                # The iteration currently is for two objects, hence range(2)
                for i in range(2):
                    # i = 0 : Check for current DataFrame (self)
                    # i = 1 : Check for the other DataFrame
                    if not value['col_present'][i]:
                        col_list[i].append('CAST(NULL as {}) as {}'.format(type_compiler.process(value['col_type']),
                                                                           UtilFuncs._teradata_quote_arg(col_name, "\"",
                                                                                                         False)))
                    else:
                        col_list[i].append(col_name)

            concat_nodeid = aed_utils._aed_setop(self._nodeid,
                                                 other._nodeid,
                                                 'unionall' if allow_duplicates else 'union',
                                                 df1_columns=','.join(col_list[0]),
                                                 df2_columns=','.join(col_list[1]))

            # Set the index_label to columns self._index_label if it is being projected,
            # else set it to columns in other._index_label if it is being projected.
            index_label = None
            index_to_use = None
            if self._index_label is not None and any(ind_col in master_columns_dict for ind_col in self._index_label):
                index_label = []
                index_to_use = self._index_label
            elif other._index_label is not None and any(ind_col in master_columns_dict for ind_col in other._index_label):
                index_label = []
                index_to_use = other._index_label

            if index_to_use is not None:
                for ind_col in index_to_use:
                    if ind_col in master_columns_dict:
                        index_label.append(ind_col)

            if is_lazy:
                # Constructing new Metadata (_metaexpr) without DB; using dummy select_nodeid
                cols = (Column(col_name, master_columns_dict[col_name]['col_type']) for col_name in master_columns_dict)
                t = Table(concat_nodeid, meta, *cols)
                new_metaexpr = _MetaExpression(t)

                return DataFrame._from_node(concat_nodeid, new_metaexpr, index_label)
            else:
                try:
                    # Execute node and get table_name to build DataFrame on
                    table_name = df_utils._execute_node_return_db_object_name(concat_nodeid)
                    return DataFrame(table_name, index_label=index_to_use)
                except TeradataMlException as err:
                    # We should be here only because of failure caused in creating DF
                    # due to incompatible types, but a TeradataMLException is raised when DF creation fails
                    raise TeradataMlException(Messages.get_message(MessageCodes.CONCAT_COL_TYPE_MISMATCH),
                                              MessageCodes.CONCAT_COL_TYPE_MISMATCH) from err

        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.CONCAT_FAILED),
                                      MessageCodes.CONCAT_FAILED) from err

    def __check_concat_compatibility(self, other, join, sort):
        """
        DESCRIPTION:
            Internal function to check if the DataFrames are compatible for concat or not.

        other:
            Required argument.
            Specifies the other teradataml DataFrame to concatenate the current DataFrame with.
            Type: teradataml DataFrame

        join:
            Required argument.
            Specifies the type of join to use in concat ('inner' or 'outer').
            Type: str

        sort:
            Required argument.
            Specifies a flag to determine whether the columns should be sorted while being projected.
            Type: bool

        RETURNS:
            A tuple of the following form:
            (master_column_dict, is_lazy)

            where master_column_dict is a dictionary with the column names to project as a result as the keys,
            and is of the following form:
            { '<col_name_1>' : { 'col_present' : [True, False], 'col_type': <type> }, '<col_name_2>' : {...}, ... }

            The value of the keys in the dictionary is again a dictionary with the following elements:
            1. 'col_present': A list of booleans, the nth value in it indicating the columns presence in the nth DF.
                              Presence specified by True, and absence by False,
            2. 'col_type':    The teradatasqlalchemy datatype of the column in the first DF that the column is present in,

            and 'is_lazy' is a boolean which indicates whether the result DataFrame creation should be a lazy operation
            or not, based on the column type compatibility.

        RAISES:
            None

        EXAMPLES:
            columns_dict, is_lazy = self.__check_concat_compatibility(other, join, sort)
        """
        dfs_to_operate_on = [self, other]

        # Initialize the return objects including a variable deciding whether the execution is lazy or not.
        # The execution will be non-lazy if the types of columns are not an exact match.
        # TODO: Add a concat type compatibility matrix for use to make this operation completely lazy
        #       https://jira.td.teradata.com/jira/browse/ELE-1913

        concat_col_dict = OrderedDict()
        is_lazy = True

        # Iterate on all DFs (currently 2) to be concatenated.
        for df in dfs_to_operate_on:
            # Process each column in the DF of the iteration.
            for c in df._metaexpr.t.c:
                col_name = c.name
                # Process the column name if it is not already processed.
                # Processing of concatenation is column name based so if the DF in the nth iteration had column 'xyz',
                # then the column with the same name in any DF in later iterations need not be processed.
                if col_name not in concat_col_dict:
                    # For every column, it's entry in the dictionary looks like:
                    # '<column_name>' : { 'col_present' : [True, False], 'col_type': <type> }
                    #   where :
                    #       '<column_name>' : is the name of the column being processed.
                    #
                    #       It's value is yet another dictionary with keys:
                    #       'col_present'   : Its value is a list of booleans, the nth value in it indicating the
                    #                         columns presence in the nth DF - presence specified by True,
                    #                         and absence by False.
                    #       'col_type'      : Its value is the teradatasqlalchemy type of the column in the first DF
                    #                         that the column is present in.

                    # Generate a list of booleans, each value of it indicating the columns presence in the DF in the
                    # dfs_to_operate_on list.
                    col_present_in_dfs = [df_utils._check_column_exists(col_name, inner_df.columns)
                                          for inner_df in dfs_to_operate_on]

                    if join.upper() == 'INNER':
                        # For inner join, column has to present in all DFs.
                        if all(col_present_in_dfs):
                            concat_col_dict[col_name] = {}

                            # Get the type of the column in all the DFs.
                            col_types_in_dfs = [inner_df._metaexpr.t.c[col_name].type for inner_df in
                                                dfs_to_operate_on]

                            # Populate the 'column_present' list using the col_present_in_dfs.
                            concat_col_dict[col_name]['col_present'] = col_present_in_dfs
                            # The type to be used for the column is the one of the first DF it is present in.
                            concat_col_dict[col_name]['col_type'] = col_types_in_dfs[0]

                            # If the type of the column in all DFs is not the same, then the operation is not lazy.
                            if not all(ctype == concat_col_dict[col_name]['col_type']
                                       for ctype in col_types_in_dfs):
                                is_lazy = False

                    elif join.upper() == 'OUTER':
                        # For outer join, column need not be present in all DFs.
                        concat_col_dict[col_name] = {}
                        # Get the type of the column in all the DFs. None for the DF it is not present in.
                        col_types_in_dfs = [None if not present else inner_df._metaexpr.t.c[col_name].type
                                            for (inner_df, present) in zip(dfs_to_operate_on, col_present_in_dfs)]

                        # Find the type of the column in the first DF it is present in.
                        non_none_type_to_add = next(ctype for ctype in col_types_in_dfs if ctype is not None)

                        # Populate the 'column_present' list using the col_present_in_dfs.
                        concat_col_dict[col_name]['col_present'] = col_present_in_dfs
                        # The type to be used for the column is the one of the first DF it is present in.
                        concat_col_dict[col_name]['col_type'] = non_none_type_to_add

                        # If the type of the column in all DFs is not the same, then the operation is not lazy.
                        if not all(True if ctype is None else ctype == non_none_type_to_add
                                   for ctype in col_types_in_dfs):
                            is_lazy = False

        # Sort if required
        if sort and join.upper() == 'OUTER':
            concat_col_dict = OrderedDict(sorted(concat_col_dict.items()))

        return concat_col_dict, is_lazy


class DataFrameGroupBy (DataFrame):
    """
    This class integrate GroupBy clause with AED.
    Updates AED node for DataFrame groupby object.

    """
    def __init__(self, nodeid, metaexpr, column_names_and_types, columns, groupbyexpr, column_list):
        super(DataFrameGroupBy, self).__init__()
        self._nodeid = self._aed_utils._aed_groupby(nodeid, groupbyexpr)
        self._metaexpr = metaexpr
        self._column_names_and_types = column_names_and_types
        self._columns = columns
        self.groupby_column_list = column_list


class MetaData():
    """
    This class contains the column names and types for a dataframe.
    This class is used for printing DataFrame.dtypes

    """

    def __init__(self, column_names_and_types):
        """
        Constructor for TerdataML MetaData.

        PARAMETERS:
            column_names_and_types - List containing column names and Python types.

        EXAMPLES:
            meta = MetaData([('col1', 'int'),('col2', 'str')])

        RAISES:

        """
        self._column_names_and_types = column_names_and_types

    def __repr__(self):
        """
        This is the __repr__ function for MetaData.
        Returns a string containing column names and Python types.

        PARAMETERS:

        EXAMPLES:
            meta = MetaData([('col1', 'int'),('col2', 'str')])
            print(meta)

        RAISES:

        """
        if self._column_names_and_types is not None:
            return df_utils._get_pprint_dtypes(self._column_names_and_types)
        else:
            return ""
