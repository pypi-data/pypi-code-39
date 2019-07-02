#!/usr/bin/python
# ##################################################################
#
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# ##################################################################

import re
import datetime
import warnings
import pandas as pd

from sqlalchemy import MetaData, Table, Interval, Column
from sqlalchemy.exc import OperationalError as sqlachemyOperationalError
from teradatasqlalchemy import (INTEGER, BIGINT, BYTEINT, FLOAT)
from teradatasqlalchemy import (TIMESTAMP)
from teradatasqlalchemy import (VARCHAR)
from teradatasqlalchemy.dialect import TDCreateTablePost as post
from teradataml.context.context import *
from teradataml.dataframe import dataframe as tdmldf
from teradataml.dataframe.dataframe_utils import DataFrameUtils as df_utils
from teradataml.common.utils import UtilFuncs
from teradataml.options.configure import configure
from teradataml.common.constants import CopyToConstants
from teradatasql import OperationalError
from teradataml.common.wrapper_utils import AnalyticsWrapperUtils


def copy_to_sql(df, table_name, schema_name=None, if_exists='append',
                index=False, index_label=None, primary_index=None,
                temporary=False, types = None,
                primary_time_index_name = None, timecode_column=None, timebucket_duration = None,
                timezero_date = None, columns_list=[], sequence_column=None, seq_max=None, set_table=False):
    """
    Writes records stored in a Pandas DataFrame or a teradataml DataFrame to Teradata Vantage.

    PARAMETERS:

        df:
            Required Argument. 
            Specifies the Pandas or teradataml DataFrame object to be saved.
            Types: pandas.DataFrame or teradataml.dataframe.dataframe.DataFrame

        table_name:
            Required Argument.
            Specifies the name of the table to be created in Vantage.
            Types : String

        schema_name:
            Optional Argument. 
            Specifies the name of the SQL schema in Teradata Vantage to write to.
            Types: String
            Default: None (Uses default database schema).

            Note: schema_name will be ignored when temporary=True.

        if_exists:
            Optional Argument.
            Specifies the action to take when table already exists in Vantage.
            Types: String
            Possible values: {'fail', 'replace', 'append'}
                - fail: If table exists, do nothing.
                - replace: If table exists, drop it, recreate it, and insert data.
                - append: If table exists, insert data. Create if does not exist.
            Default : append

            Note: Replacing a table with the contents of a teradataml DataFrame based on
                  the same underlying table is not supported.

        index:
            Optional Argument.
            Specifies whether to save Pandas DataFrame index as a column or not.
            Types : Boolean (True or False)
            Default : False
            
            Note: Only use as True when attempting to save Pandas DataFrames (and not with teradataml DataFrames).

        index_label: 
            Optional Argument.
            Specifies the column label for Pandas DataFrame index column(s).
            Types : String
            Default : None
            
            Note: If index_label is not specified (defaulted to None or is empty) and `index` is True, then
                  the 'name' property of the DataFrames index is used as the label, and if that too is None or empty,
                  a default label 'index_label' is used.
                  Only use as True when attempting to save Pandas DataFrames (and not on teradataml DataFrames).

        primary_index:
            Optional Argument.
            Specifies which column(s) to use as primary index while creating Teradata table(s) in Vantage.
            When None, No Primary Index Teradata tables are created.
            Types : String or list of strings
            Default : None
            Example:
                primary_index = 'my_primary_index'
                primary_index = ['my_primary_index1', 'my_primary_index2', 'my_primary_index3']

        temporary:
            Optional Argument.
            Specifies whether to creates Vantage tables as permanent or volatile.
            Types : Boolean (True or False)
            Default : False
            
            Note: When True:
                  1. volatile Tables are created, and
                  2. schema_name is ignored.
                  When False, permanent tables are created.
            
        types 
            Optional Argument.
            Specifies required data-types for requested columns to be saved in Vantage.
            Types: Python dictionary ({column_name1: type_value1, ... column_nameN: type_valueN})
            Default: None
            
            Note: This argument accepts a dictionary of columns names and their required teradatasqlalchemy types
                  as key-value pairs; allowing to specify a subset of the columns of a specific type.
                  When only a subset of all columns are provided, the rest are defaulted to appropriate types.
                  When types argument is not provided, all column types are appropriately assigned and defaulted.

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
            corresponding to Python types datetime.datetime or datetime.date, or Pandas dtype datetime64[ns].
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
            Used when the DataFrame must be saved as a PTI table.
            Required if timebucket_duration is not specified.
            A list of one or more PTI table column names.
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
            Default Value: False
            Type: boolean

            Note: 1. Specifying set_table=True also requires specifying primary_index or timecode_column.
                  2. Creating SET table (set_table=True) may result in
                     a. an error if the source is a Pandas DataFrame having duplicate rows.
                     b. loss of duplicate rows if the source is a teradataml DataFrame.
                  3. This argument has no effect if the table already exists and if_exists='append'.


    RETURNS:
        None

    RAISES:
        TeradataMlException

    EXAMPLES:
        1. Saving a Pandas DataFrame:

            >>> from teradataml.dataframe.copy_to import copy_to_sql
            >>> from teradatasqlalchemy.types import *

            >>> df = {'emp_name': ['A1', 'A2', 'A3', 'A4'],
                'emp_sage': [100, 200, 300, 400],
                'emp_id': [133, 144, 155, 177],
                'marks': [99.99, 97.32, 94.67, 91.00]
                }

            >>> pandas_df = pd.DataFrame(df)

            a) Save a Pandas DataFrame using a dataframe & table name only:
            >>> copy_to_sql(df = pandas_df, table_name = 'my_table')

            b) Saving as a SET table
            >>> copy_to_sql(df = pandas_df, table_name = 'my_set_table', index=True,
                            primary_index='index_label', set_table=True)

            c) Save a Pandas DataFrame by specifying additional parameters:
            >>> copy_to_sql(df = pandas_df, table_name = 'my_table_2', schema_name = 'alice',
                            index = True, index_label = 'my_index_label', temporary = False,
                            primary_index = ['emp_id'], if_exists = 'append',
                            types = {'emp_name': VARCHAR, 'emp_sage':INTEGER,
                                     'emp_id': BIGINT, 'marks': DECIMAL})

            d) Saving with additional parameters as a SET table
            >>> copy_to_sql(df = pandas_df, table_name = 'my_table_3', schema_name = 'alice',
                            index = True, index_label = 'my_index_label', temporary = False,
                            primary_index = ['emp_id'], if_exists = 'append',
                            types = {'emp_name': VARCHAR, 'emp_sage':INTEGER,
                                     'emp_id': BIGINT, 'marks': DECIMAL},
                            set_table=True)

        2. Saving a teradataml DataFrame:

            >>> from teradataml.dataframe.dataframe import DataFrame
            >>> from teradataml.dataframe.copy_to import copy_to_sql
            >>> from teradatasqlalchemy.types import *
            >>> from teradataml.data.load_example_data import load_example_data
            
            >>> # Load the data to run the example.
            >>> load_example_data("glm", "admissions_train")
            
            >>> # Create teradataml DataFrame(s)
            >>> df = DataFrame('admissions_train')
            >>> df2 = df.select(['gpa', 'masters'])

            a) Save a teradataml DataFrame by using only a table name:
            >>> df2.to_sql('my_tdml_table')

            b) Save a teradataml DataFrame by using additional parameters:
            >>> df2.to_sql(table_name = 'my_tdml_table', if_exists='append',
                           primary_index = ['gpa'], temporary=False, schema_name='alice')

            c) Alternatively, save a teradataml DataFrame by using copy_to_sql:
            >>> copy_to_sql(df2, 'my_tdml_table_2')

            d) Save a teradataml DataFrame by using copy_to_sql with additional parameters:
            >>> copy_to_sql(df = df2, table_name = 'my_tdml_table_3', schema_name = 'alice',
                            temporary = False, primary_index = None, if_exists = 'append',
                            types = {'masters': VARCHAR, 'gpa':INTEGER})

            e) Saving as a SET table
            >>> copy_to_sql(df = df2, table_name = 'my_tdml_set_table', schema_name = 'alice',
                            temporary = False, primary_index = ['gpa'], if_exists = 'append',
                            types = {'masters': VARCHAR, 'gpa':INTEGER}, set_table = True)

        3. Saving a teradataml DataFrame as a PTI table:

            >>> from teradataml.dataframe.dataframe import DataFrame
            >>> from teradataml.dataframe.copy_to import copy_to_sql
            >>> from teradataml.data.load_example_data import load_example_data

            >>> load_example_data("sessionize", "sessionize_table")
            >>> df3 = DataFrame('sessionize_table')

            a) Using copy_to_sql
            >>> copy_to_sql(df3, "test_copyto_pti",
                            timecode_column='clicktime',
                            columns_list='event')

            b) Alternatively, using DataFrame.to_sql
            >>> df3.to_sql(table_name = "test_copyto_pti_1",
                          timecode_column='clicktime',
                          columns_list='event')

            c) Saving as a SET table
            >>> copy_to_sql(df3, "test_copyto_pti_2",
                            timecode_column='clicktime',
                            columns_list='event',
                            set_table=True)

    """
    # Deriving global connection using context.get_context()
    con = get_context()

    try:
        if con is None:
            raise TeradataMlException(Messages.get_message(MessageCodes.CONNECTION_FAILURE), MessageCodes.CONNECTION_FAILURE)

        # Check if the table to be created must be a Primary Time Index (PTI) table.
        # If a user specifies the timecode_column parameter, and attempt to create
        # a PTI will be made.
        is_pti = False
        if timecode_column is not None:
            is_pti = True
            if primary_index is not None:
                warnings.warn(Messages.get_message(MessageCodes.IGNORE_ARGS_WARN,
                                                   'primary_index',
                                                   'timecode_column',
                                                   'specified'))
        else:
            ignored = []
            if timezero_date is not None: ignored.append('timezero_date')
            if timebucket_duration is not None: ignored.append('timebucket_duration')
            if sequence_column is not None: ignored.append('sequence_column')
            if seq_max is not None: ignored.append('seq_max')
            if columns_list is not None and (
                    not isinstance(columns_list, list) or len(columns_list) > 0): ignored.append('columns_list')
            if primary_time_index_name is not None: ignored.append('primary_time_index_name')
            if len(ignored) > 0:
                warnings.warn(Messages.get_message(MessageCodes.IGNORE_ARGS_WARN,
                                                   ignored,
                                                   'timecode_column',
                                                   'missing'))

        # Unset schema_name when temporary is True since volatile tables are always in the user database
        if temporary is True:
            if schema_name is not None:
                warnings.warn(Messages.get_message(MessageCodes.IGNORE_ARGS_WARN,
                                                   'schema_name',
                                                   'temporary=True',
                                                   'specified'))
            schema_name = None

        # Validate DataFrame & related flags; Proceed only when True
        _validate_copy_parameters(df, table_name, index, index_label, primary_index, temporary, if_exists, schema_name,
                                  set_table, types)

        # If the table created must be a PTI table, then validate additional parameters
        # Note that if the required parameters for PTI are valid, then other parameters, though being validated,
        # will be ignored - for example, primary_index
        if is_pti:
            _validate_pti_copy_parameters(df, timecode_column, timebucket_duration,
                                  timezero_date, primary_time_index_name, columns_list,
                                  sequence_column, seq_max, types, index, index_label)

        # A table cannot be a SET table and have NO PRIMARY INDEX
        if set_table and primary_index is None and timecode_column is None:
            raise TeradataMlException(Messages.get_message(MessageCodes.SET_TABLE_NO_PI),
                                      MessageCodes.SET_TABLE_NO_PI)

        # df is a Pandas DataFrame object
        if isinstance(df, pd.DataFrame):
            table_exists = con.dialect.has_table(con, table_name, schema=schema_name)
            if not table_exists or (table_exists and if_exists.lower() == 'replace'):

                if table_exists:
                    UtilFuncs._drop_table(table_name)

                if not is_pti:
                    table = _create_table_object(df, table_name, con, primary_index, temporary, schema_name, set_table,
                                                 types, index, index_label)
                else:
                    table = _create_pti_table_object(df, con, table_name, schema_name, temporary,
                                                     primary_time_index_name, timecode_column, timezero_date,
                                                     timebucket_duration, sequence_column, seq_max,
                                                     columns_list, set_table, types, index, index_label)

                if table is not None:
                    table.create()
                else:
                    raise TeradataMlException(Messages.get_message(MessageCodes.TABLE_OBJECT_CREATION_FAILED),
                                              MessageCodes.TABLE_OBJECT_CREATION_FAILED)

                # Support for saving Pandas index/Volatile tables doesn't exist
                # - Manually inserting (batch) rows for now
                if index is True or temporary is True:
                    _insert_from_dataframe(df, con, schema_name, table_name, index, index_label, types,
                                           is_pti, timecode_column, sequence_column)
                # When index isn't saved & for permanent tables, to_sql insertion used (batch)
                else:
                    try:
                        _insert_data(df, table_name, con, index, index_label, schema_name, is_pti, timecode_column,
                                     sequence_column)
                    except sqlachemyOperationalError as err:
                        if "Duplicate row error" in str(err):
                            raise TeradataMlException(Messages.get_message(MessageCodes.SET_TABLE_DUPICATE_ROW,
                                                                           table_name),
                                                      MessageCodes.SET_TABLE_DUPICATE_ROW)
                        else:
                            raise TeradataMlException(Messages.get_message(MessageCodes.COPY_TO_SQL_FAIL),
                                                      MessageCodes.COPY_TO_SQL_FAIL) from err
            elif table_exists and if_exists.lower() == 'append':
                if set_table:
                    warnings.warn(Messages.get_message(MessageCodes.IGNORE_ARGS_WARN,
                                                       'set_table',
                                                       "if_exists='append'",
                                                       'specified'))

                meta = MetaData(con)
                table = Table(table_name, meta, schema=schema_name, autoload=True, autoload_with=con)

                if table is not None:
                    if types is None:
                        col_names, col_types = _extract_column_info(df)
                        df_col_object = (col_names, col_types)
                        cols_compatible = _check_columns_insertion_compatible(table.c, df_col_object, True,
                                                                              is_pti, timecode_column, sequence_column)

                        if cols_compatible:
                            try:
                                _insert_from_dataframe(df, con, schema_name, table_name, index, index_label, types,
                                                       is_pti, timecode_column, sequence_column)
                            except OperationalError:
                                raise TeradataMlException(Messages.get_message(MessageCodes.INSERTION_INCOMPATIBLE),
                                                          MessageCodes.INSERTION_INCOMPATIBLE)
                        else:
                            raise TeradataMlException(Messages.get_message(MessageCodes.INSERTION_INCOMPATIBLE),
                                                      MessageCodes.INSERTION_INCOMPATIBLE)

                    # When types are provided, no validation is performed, Vantage handles incompatibility (if any)
                    else:
                        _insert_from_dataframe(df, con, schema_name, table_name, index, index_label, types,
                                               is_pti, timecode_column, sequence_column)

            elif table_exists and if_exists.lower() == 'fail':
                raise TeradataMlException(Messages.get_message(MessageCodes.TABLE_ALREADY_EXISTS, table_name),
                                          MessageCodes.TABLE_ALREADY_EXISTS)
        # df is a teradataml DataFrame object (to_sql wrapper used)
        elif isinstance(df, tdmldf.DataFrame):
            # Let us also execute the node and set the table_name
            if df._table_name is None:
                df._table_name = df_utils._execute_node_return_db_object_name(df._nodeid, df._metaexpr)

            # Handle cases for table already exists & append/replace/fail
            table_exists = con.dialect.has_table(con, table_name, schema=schema_name)
            df_column_list = [col.name for col in df._metaexpr.c]

            if is_pti:
                # Reorder the column list to reposition the timecode and sequence columns
                df_column_list = _reorder_insert_list_for_pti(df_column_list, timecode_column, sequence_column)

            if not table_exists or (table_exists and if_exists.lower() == 'replace'):

                if table_exists:
                    UtilFuncs._drop_table(table_name)

                if not is_pti:
                    table = _create_table_object(df, table_name, con, primary_index, temporary, schema_name, set_table,
                                                 types)
                else:
                    table = _create_pti_table_object(df, con, table_name, schema_name, temporary, primary_time_index_name,
                                                     timecode_column, timezero_date, timebucket_duration,
                                                     sequence_column, seq_max, columns_list, set_table, types)

                if table is not None:
                    table.create()
                    df_utils._insert_all_from_table(table_name, df._table_name, df_column_list, schema_name)
                else:
                    raise TeradataMlException(Messages.get_message(MessageCodes.TABLE_OBJECT_CREATION_FAILED),
                                              MessageCodes.TABLE_OBJECT_CREATION_FAILED)

            elif table_exists and if_exists.lower() == 'append':
                if set_table:
                    warnings.warn(Messages.get_message(MessageCodes.IGNORE_ARGS_WARN,
                                                       'set_table',
                                                       "if_exists='append'",
                                                       'specified'))

                meta = MetaData(con)
                table = Table(table_name, meta, schema=schema_name, autoload=True, autoload_with=con)

                if table is not None:
                    if types is None:
                    
                        # Get the column details from the metadata to get past any datatype mapping issues (ELE-1711)
                        df_table = __get_sqlalchemy_table_from_tdmldf(df, meta)
                        cols_compatible = _check_columns_insertion_compatible(table.c, df_table.c, False, is_pti,
                                                                              timecode_column, sequence_column)

                        if cols_compatible:
                            try:
                                df_utils._insert_all_from_table(table_name, df._table_name, df_column_list, schema_name)
                            # When types are incompatible at run-time while inserting, raise exception
                            except OperationalError:
                                raise TeradataMlException(Messages.get_message(MessageCodes.INSERTION_INCOMPATIBLE),
                                                      MessageCodes.INSERTION_INCOMPATIBLE)
                        else:
                            raise TeradataMlException(Messages.get_message(MessageCodes.INSERTION_INCOMPATIBLE),
                                                      MessageCodes.INSERTION_INCOMPATIBLE)
                    
                    #When types are provided, no validation is performed, Vantage handles incompatibility (if any)
                    else:
                        df_utils._insert_all_from_table(table_name, df._table_name, df_column_list, schema_name)

            elif table_exists and if_exists.lower() == 'fail':
                    raise TeradataMlException(Messages.get_message(MessageCodes.TABLE_ALREADY_EXISTS, table_name),
                                              MessageCodes.TABLE_ALREADY_EXISTS)

    except TeradataMlException:
        raise
    except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.COPY_TO_SQL_FAIL), MessageCodes.COPY_TO_SQL_FAIL) from err


def __get_sqlalchemy_table_from_tdmldf(df, meta):
    """
    This is an internal function used to generate an SQLAlchemy Table
    object for the underlying table/view of a DataFrame.

    PARAMETERS:
        df:
            The teradataml DataFrame to generate the SQLAlchemy.Table object for.

        meta:
            The SQLAlchemy.Metadata object.

    RETURNS:
        SQLAlchemy.Table

    RAISES:
        None

    EXAMPLES:
        >>> con = get_context()
        >>> df = DataFrame('admissions_train')
        >>> meta = sqlalchemy.MetaData(con)
        >>> table = __get_sqlalchemy_table_from_tdmldf(df, meta)

    """
    con = get_context()
    db_schema = UtilFuncs._extract_db_name(df._table_name)
    db_table_name = UtilFuncs._extract_table_name(df._table_name)

    # Remove quotes because sqlalchemy.Table() does not like the quotes.
    if db_schema is not None:
        db_schema = db_schema[1:-1]
    db_table_name = db_table_name[1:-1]

    return Table(db_table_name, meta, schema=db_schema, autoload=True, autoload_with=con)


def _validate_copy_parameters(df, table_name, index, index_label, primary_index, temporary, if_exists, schema_name,
                              set_table, types):
    """
    This is an internal function used to validate the copy request.
    Dataframe, connection & related parameters are checked.
    Saving to Vantage is proceeded to only when validation returns True.

    PARAMETERS:
        df:
            The DataFrame (Pandas or teradataml) object to be saved.

        table_name:
            Name of SQL table.

        index:
            Flag specifying whether to write Pandas DataFrame index as a column or not.

        index_label:
            Column label for index column(s).

        primary_index:
            Creates Teradata Table(s) with Primary index column if specified.

        temporary:
            Flag specifying whether SQL table to be created is Volatile or not.

        if_exists:
            String specifying action when table already exists in SQL Schema.

        schema_name:
            Name of the Vantage database.

        set_table:
            A Flag specifying whether to create a SET table or a MULTISET table.
            When True, an attempt to create a SET table is made.
            When False, an attempt to create a MULTISET table is made.

        types:
            Dictionary specifying column-name to teradatasqlalchemy type-mapping.

    RETURNS:
        True, when all parameters are valid.

    RAISES:
        TeradataMlException, when parameter validation fails.

    EXAMPLES:
        _validate_copy_parameters(df = my_df, table_name = 'test_table', index = True, index_label = None,
                                  primary_index = None, temporary = True, if_exists = 'replace', types = None)
    """
    if df is None or not _check_dataframe(df):
        raise TeradataMlException(Messages.get_message(MessageCodes.IS_NOT_VALID_DF),
                                  MessageCodes.IS_NOT_VALID_DF)

    if isinstance(df, pd.DataFrame):
        df_columns = df.columns.get_values().tolist()
    else:
        df_columns = [col.name for col in df._metaexpr.c]

    if len(df.columns) > TeradataConstants.TABLE_COLUMN_LIMIT.value:
        raise TeradataMlException(Messages.get_message(MessageCodes.TD_MAX_COL_MESSAGE),
                                  MessageCodes.TD_MAX_COL_MESSAGE)

    awu = AnalyticsWrapperUtils()
    awu_matrix = []

    # The arguments added to awu_martix are:
    # arg_name, arg, is_optional, acceptable types
    # The value for is_optional is set to False when the argument
    # a) is a required argument
    # b) is not allowed to be None, even if it is optional
    awu_matrix.append(['table_name', table_name, False, (str)])
    awu_matrix.append(['schema_name', schema_name, True, (str)])
    awu_matrix.append(['index', index, False, (bool)])
    awu_matrix.append(['temporary', temporary, False, (bool)])
    awu_matrix.append(['types', types, True, (dict)])
    awu_matrix.append(['if_exists', if_exists, False, (str)])
    awu_matrix.append(['primary_index', primary_index, True, (str,list)])
    awu_matrix.append(['set_table', set_table, False, (bool)])

    if isinstance(df, pd.DataFrame):
        awu_matrix.append(['index_label', index_label, True, (str)])
        awu._validate_input_columns_not_empty(index_label, 'index_label')

    # Validate types
    awu._validate_argument_types(awu_matrix)

    # Validate arg emtpy
    awu._validate_input_columns_not_empty(table_name, 'table_name')
    awu._validate_input_columns_not_empty(schema_name, 'schema_name')
    awu._validate_input_columns_not_empty(if_exists, 'if_exists')
    awu._validate_input_columns_not_empty(primary_index, 'primary_index')

    # Validate permitted values
    awu._validate_permitted_values(if_exists, ['APPEND', 'REPLACE', 'FAIL'], 'if_exists')

    # Retrieving user, and user-created valid schemas using the helper func. _get_database_names()
    eng = get_context()
    current_user = eng.url.username
        
    allowed_schemas = df_utils._get_database_names(eng, schema_name)
    allowed_schemas.append(current_user)

    if schema_name is not None and schema_name.lower() not in allowed_schemas:
        raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_ARG_VALUE,
                                  str(schema_name), 'schema_name', 'A valid database/schema name.'),
                                  MessageCodes.INVALID_ARG_VALUE)

    if isinstance(df, pd.DataFrame):
        if index is True and index_label in df_columns:
            raise TeradataMlException(Messages.get_message(MessageCodes.INDEX_ALREADY_EXISTS), MessageCodes.INDEX_ALREADY_EXISTS)

        if index_label is not None and index is False:
            raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_INDEX_LABEL), MessageCodes.INVALID_INDEX_LABEL)

    elif isinstance(df, tdmldf.DataFrame):
        # teradataml DataFrame's do not support saving pandas index/index_label
        if index_label is not None:
            raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_ARG_VALUE,
                                      str(index_label), 'index_label', 'None'),
                                      MessageCodes.INVALID_ARG_VALUE)

        if index is not False:
            raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_ARG_VALUE,
                                      str(index), 'index', 'False'),
                                      MessageCodes.INVALID_ARG_VALUE)
        
    # When Pandas DF's used and Pandas Index is saved, add it to column list while validating types argument
    if index:
        index_name = index_label
        if index_label in ('', None):
            index_name = df.index.name if not df.index.name in ('', None) else 'index_label'

        df_columns.append(index_name)

    # Check for existence of Primarry Index Columns
    pindex = primary_index
    if primary_index is not None:
        if isinstance(primary_index, str):
            pindex = [primary_index]

        for column in pindex:
            if column not in df_columns:
                raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_PRIMARY_INDEX),
                                          MessageCodes.INVALID_PRIMARY_INDEX)

    # Verify types argument is a dictionary, non-empty, and contains appropriate columns
    if types is not None:
        # Verify types argument is non-empty when specified
        if not(types):
            raise TeradataMlException(Messages.get_message(MessageCodes.ARG_EMPTY, 'types'),
                                      MessageCodes.ARG_EMPTY)
            
        # Check if all column names provided in types are valid DataFrame columns
        if any(key not in df_columns for key in types):
            # Only iterate entire types dictionary if an invalid column value passed
            for key in types:
                if key not in df_columns:
                    raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_ARG_VALUE,
                                              str(key), 'types', ', '.join(df_columns)),
                                              MessageCodes.INVALID_ARG_VALUE)


def _validate_pti_copy_parameters(df, timecode_column, timebucket_duration,
                                  timezero_date, primary_time_index_name, columns_list,
                                  sequence_column, seq_max, types, index, index_label):
    """
    This is an internal function used to validate the PTI part of copy request.
    Dataframe, connection & related parameters are checked.
    Saving to Vantage is proceeded to only when validation returns True.

    PARAMETERS:
        df:
            The DataFrame (Pandas or teradataml) object to be saved.

        timecode_column:
            The column in the DataFrame that reflects the form of the timestamp
            data in the time series.
            Type: String

        timebucket_duration:
            A duration that serves to break up the time continuum in
            the time series data into discrete groups or buckets.
            Type: String

        timezero_date:
            Specifies the earliest time series data that the PTI table will accept.
            Type: String

        primary_time_index_name:
            A name for the Primary Time Index (PTI).
            Type: String

        columns_list:
            A list of one or more PTI table column names.
            Type: String or list of Strings

        sequence_column:
            Specifies a column of type Integer with sequences implying that the
            time series data readings are not unique.
            If not specified, the time series data are assumed to be unique in time.
            Type: String

        seq_max:
            Specifies the maximum number of sensor data rows that can have the
            same timestamp. Can be used when 'sequenced' is True.
            Accepted range:  1 - 2147483647.
            Type: int

        types:
            Dictionary specifying column-name to teradatasqlalchemy type-mapping.

        index:
            Flag specifying whether to write Pandas DataFrame index as a column or not.
            Type: bool

        index_label:
            Column label for index column(s).
            Type: String

    RETURNS:
        True, when all parameters are valid.

    RAISES:
        TeradataMlException, when parameter validation fails.

    EXAMPLES:
        _validate_pti_copy_parameters(df = my_df, timecode_column = 'ts', timbucket_duration = 'HOURS(2)')
    """
    if isinstance(df, pd.DataFrame):
        df_columns = df.columns.get_values().tolist()
        # When Pandas DF's used and Pandas Index is saved,
        # add it to column list while validating types argument
        if index:
            index_name = index_label
            if index_label in ('', None):
                index_name = df.index.name if not df.index.name in ('', None) else 'index_label'

            df_columns.append(index_name)
    else:
        df_columns = [col.name for col in df._metaexpr.c]

    awu = AnalyticsWrapperUtils()
    awu_matrix = []

    # The arguments added to awu_martix are:
    # arg_name, arg, is_optional, acceptable types
    # The value for is_optional is set to False when the argument
    # a) is a required argument
    # b) is not allowed to be None, even if it is optional
    awu_matrix.append(['timecode_column', timecode_column, False, (str)])
    awu_matrix.append(['columns_list', columns_list, timebucket_duration is not None, (str, list)])
    awu_matrix.append(['timezero_date', timezero_date, True, (str)])
    awu_matrix.append(['timebucket_duration', timebucket_duration, columns_list is not None, (str)])
    awu_matrix.append(['primary_time_index_name', primary_time_index_name, True, (str)])
    awu_matrix.append(['sequence_column', sequence_column, True, (str)])
    awu_matrix.append(['seq_max', seq_max, True, (int)])

    # Validate types
    awu._validate_argument_types(awu_matrix)

    # Validate arg emtpy
    awu._validate_input_columns_not_empty(timecode_column, 'timecode_column')
    awu._validate_input_columns_not_empty(columns_list, 'columns_list')
    awu._validate_input_columns_not_empty(timezero_date, 'timezero_date')
    awu._validate_input_columns_not_empty(timebucket_duration, 'timebucket_duration')
    awu._validate_input_columns_not_empty(sequence_column, 'sequence_column')

    # Validate all the required arguments and optional arguments when not none
    # First the timecode_column
    _validate_column_in_list_of_columns('df', df_columns, timecode_column, 'timecode_column')
    # Check the type of timecode_column
    _validate_column_type(df, timecode_column, 'timecode_column', CopyToConstants.valid_timecode_datatypes, types)

    # timezero date
    _validate_timezero_date(timezero_date)

    # timebucket duration
    _validate_timebucket_duration(timebucket_duration)

    # Validate sequence_column
    if sequence_column is not None:
        _validate_column_in_list_of_columns('df', df_columns, sequence_column, 'sequence_column')
        # Check the type of sequence_column
        _validate_column_type(df, sequence_column, 'sequence_column', CopyToConstants.valid_sequence_col_datatypes, types)

    # Validate seq_max
    if seq_max is not None and (seq_max < 1 or seq_max > 2147483647):
        raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_ARG_VALUE).format(seq_max, 'seq_max', '1 < integer < 2147483647'),
                                  MessageCodes.INVALID_ARG_VALUE)

    # Validate cols_list
    _validate_columns_list('df', df_columns, columns_list)
    if isinstance(columns_list, str):
        columns_list = [columns_list]

    # Either one or both of timebucket_duration and columns_list must be specified
    if timebucket_duration is None and (columns_list is None or len(columns_list) == 0):
        raise TeradataMlException(
            Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT, 'timebucket_duration', 'columns_list'),
            MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)


def _validate_columns_list(df, df_columns, columns_list):
    """
    Internal function to validate columns list specified when creating a
    Primary Time Index (PTI) table.

    PARAMETERS:
        df:
            Name of the DataFrame to which the column being validated
            does or should belong.

        df_columns:
            List of columns in the DataFrame.

        columns_list:
            The column or list of columns.
            Type: String or list of Strings

    RETURNS:
        True if the column or list of columns is valid.

    RAISES:
        Raise TeradataMlException on validation failure.
    """
    if columns_list is None:
        return True

    # Validate DF has columns
    if isinstance(columns_list, str):
        columns_list = [columns_list]

    for col in columns_list:
        _validate_column_in_list_of_columns(df, df_columns, col, 'columns_list')

    return True


def _validate_column_in_list_of_columns(df, df_columns, col, col_arg):
    """
    Internal function to validate the arguments used to specify
    a column name in DataFrame.

    PARAMETERS:
        df:
            Name of the DataFrame to which the column being validated
            does or should belong.

        df_column_list:
            List of columns in the DataFrame.

        col:
            Column to be validated.

        col_arg:
            Name of argument used to specify the column name.

    RETURNS:
         True, if column name is a valid.

    RAISES:
        TeradataMlException if invalid column name.
    """
    if col not in df_columns:
        raise TeradataMlException(
            Messages.get_message(MessageCodes.TDMLDF_COLUMN_IN_ARG_NOT_FOUND).format(col,
                                                                                     col_arg, df),
            MessageCodes.TDMLDF_COLUMN_IN_ARG_NOT_FOUND)

    return True


def _validate_column_type(df, col, col_arg, expected_types, types = None):
    """
    Internal function to validate the type of an input DataFrame column against
    a list of expected types.

    PARAMETERS
        df:
            Input DataFrame (Pandas or teradataml) which has the column to be tested
            for type.

        col:
            The column in the input DataFrame to be tested for type.

        col_arg:
            The name of the argument used to pass the column name.

        expected_types:
            Specifies a list of teradatasqlachemy datatypes that the column is
            expected to be of type.

        types:
            Dictionary specifying column-name to teradatasqlalchemy type-mapping.

    RETURNS:
        True, when the columns is of an expected type.

    RAISES:
        TeradataMlException, when the columns is not one of the expected types.

    EXAMPLES:
        _validate_column_type(df, timecode_column, 'timecode_column', CopyToConstants.valid_timecode_datatypes, types)
    """
    # Check if sequence_column is being translated to a valid_type
    if types is not None and col in types:
        if not any(isinstance(types[col], expected_type) for expected_type in expected_types):
            raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_COLUMN_TYPE).
                                      format(col_arg, types[col], ' or '.join(expected_type.__visit_name__
                                                                              for expected_type in expected_types)),
                                      MessageCodes.INVALID_COLUMN_TYPE)
    # Else we need to copy without any casting
    elif isinstance(df, pd.DataFrame):
        t = _get_sqlalchemy_mapping(str(df.dtypes[col]))
        if t not in expected_types:
            raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_COLUMN_TYPE).
                                      format(col_arg, t, ' or '.join(expected_type.__visit_name__
                                                                     for expected_type in expected_types)),
                                      MessageCodes.INVALID_COLUMN_TYPE)
    elif not any(isinstance(df[col].type, t) for t in expected_types):
        raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_COLUMN_TYPE).
                                  format(col_arg, df[col].type, ' or '.join(expected_type.__visit_name__
                                                                            for expected_type in expected_types)),
                                  MessageCodes.INVALID_COLUMN_TYPE)

    return True


def _create_table_object(df, table_name, con, primary_index, temporary, schema_name, set_table, types, index=None,
                         index_label=None):
    """
    This is an internal function used to construct a SQLAlchemy Table Object.
    This function checks appropriate flags and supports creation of Teradata
    specific Table constructs such as Volatile/Primary Index tables.


    PARAMETERS:
        df:
            The teradataml or Pandas DataFrame object to be saved.

        table_name:
            Name of SQL table.

        con:
            A SQLAlchemy connectable (engine/connection) object

        primary_index:
            Creates Teradata Table(s) with Primary index column if specified.

        temporary:
            Flag specifying whether SQL table to be created is Volatile or not.

        schema_name:
            Specifies the name of the SQL schema in the database to write to.

        set_table:
            A flag specifying whether to create a SET table or a MULTISET table.
            When True, an attempt to create a SET table is made.
            When False, an attempt to create a MULTISET table is made.

        types:
            Specifies a python dictionary with column-name(key) to column-type(value) mapping to create DataFrames.

        index:
            Flag specifying whether to write Pandas DataFrame index as a column or not.

        index_label:
            Column label for index column(s).

    RETURNS:
        SQLAlchemy Table

    RAISES:
        N/A

    EXAMPLES:
        _create_table_object(df = my_df, table_name = 'test_table', con = tdconnection, primary_index = None,
                             temporary = True, schema_name = schema, set_table=False, types = types, index = True, index_label = None)
    """
    # Dictionary to append special flags, can be extended to add Fallback, Journalling, Log etc.
    post_params = {}
    prefix = []
    pti = post(opts=post_params)

    if temporary is True:
        pti = pti.on_commit(option='preserve')
        prefix.append('VOLATILE')

    if not set_table:
        prefix.append('multiset')
    else:
        prefix.append('set')

    meta = MetaData()
    meta.bind = con

    if isinstance(df, pd.DataFrame):
        if types is None:
            col_names, col_types = _extract_column_info(df)
        else:
            col_names, col_types = _extract_column_info_from_types(df, types)

        if index:
            index_name = df.index.name

            # Use index label if specified, else use Pandas DF Index name,
            # else use default index_label ('index' is a keyword)
            if index_name in ('', None):
                index_name = index_label if index_label is not None else 'index_label'
                col_names.append(index_name)
                col_types.append(INTEGER)
            else:
                index_name = index_label if index_label is not None else index_name
                col_names.append(index_name)
                col_types.append(_get_sqlalchemy_mapping(df.index.dtype))

    else:
        df_table = __get_sqlalchemy_table_from_tdmldf(df, meta)
        col_names = [col.name for col in df._metaexpr.c]

        if types is None:
            # Get the column details from the metadata to get past any datatype mapping issues (ELE-1711)
            col_types = [df_table.c[i].type for i in col_names]
        else:
            # When user-type provided use, or default when partial types provided
            col_types = [types.get(col, df_table.c[col].type) for col in col_names]

    if primary_index is not None:
        if isinstance(primary_index, list):
            pti = pti.primary_index(unique=False, cols=primary_index)
        elif isinstance(primary_index, str):
            pti = pti.primary_index(unique=False, cols=[primary_index])
    else:
        pti = pti.no_primary_index()

    # Create default Table construct with parameter dictionary
    table = Table(table_name, meta,
                  *(Column(col_name, col_type)
                    for col_name, col_type in
                    zip(col_names, col_types)),
                  teradatasql_post_create=pti,
                  prefixes=prefix,
                  schema=schema_name
                  )

    return table


def _create_pti_table_object(df, con, table_name, schema_name, temporary, primary_time_index_name,
                             timecode_column, timezero_date, timebucket_duration,
                             sequence_column, seq_max, columns_list, set_table, types, index=None, index_label=None):
    """
    This is an internal function used to construct a SQLAlchemy Table Object.
    This function checks appropriate flags and supports creation of Teradata
    specific Table constructs such as Volatile and Primary Time Index tables.

    PARAMETERS:
        df:
            The teradataml or Pandas DataFrame object to be saved.

        con:
            A SQLAlchemy connectable (engine/connection) object

        table_name:
            Name of SQL table.

        schema_name:
            Specifies the name of the SQL schema in the database to write to.

        temporary:
            Flag specifying whether SQL table to be created is Volatile or not.

        primary_time_index_name:
            A name for the Primary Time Index (PTI).

        timecode_column:
            The column in the DataFrame that reflects the form of the timestamp
            data in the time series.

        timezero_date:
            Specifies the earliest time series data that the PTI table will accept.

        timebucket_duration:
            A duration that serves to break up the time continuum in
            the time series data into discrete groups or buckets.

        sequence_column:
            Specifies a column with sequences implying that time series data
            readings are not unique. If not specified, the time series data are
            assumed to be unique.

        seq_max:
            Specifies the maximum number of sensor data rows that can have the
            same timestamp. Can be used when 'sequenced' is True.

        columns_list:
            A list of one or more PTI table column names.

        set_table:
            A flag specifying whether to create a SET table or a MULTISET table.
            When True, an attempt to create a SET table is made.
            When False, an attempt to create a MULTISET table is made.

        types:
            Specifies a python dictionary with column-name(key) to column-type(value) mapping to create DataFrames.

        index:
            Flag specifying whether to write Pandas DataFrame index as a column or not.

        index_label:
            Column label for index column(s).

    RETURNS:
        SQLAlchemy Table

    RAISES:
        N/A

    EXAMPLES:
        _create_pti_table_object(df = my_df, table_name = 'test_table', con = tdconnection,
                         timecode_column = 'ts', columns_list = ['user_id', 'location'])

    """
    meta = MetaData(con)

    if isinstance(df, pd.DataFrame):
        if types is None:
            col_names, col_types = _extract_column_info(df)
        else:
            col_names, col_types = _extract_column_info_from_types(df, types)

        timecode_datatype = _get_sqlalchemy_mapping(str(df.dtypes[timecode_column]))()

        if index is True:
            # Pandas Index needs to be saved
            index_name = df.index.name

            # Use index label if specified, else use Pandas DF Index name, else use default index_label ('index' is a keyword)
            if index_name in ('', None):
                index_name = index_label if index_label is not None else 'index_label'
                col_names.append(index_name)
                col_types.append(INTEGER)
            else:
                index_name = index_label if index_label is not None else index_name
                col_names.append(index_name)
                col_types.append(_get_sqlalchemy_mapping(df.index.dtype))
    else:
        df_table = __get_sqlalchemy_table_from_tdmldf(df, meta)

        col_names = [col.name for col in df._metaexpr.c]

        timecode_datatype = df[timecode_column].type

        # Get the column details from the metadata to get past any datatype mapping issues (ELE-1711)
        if types is None:
            col_types = [df_table.c[i].type for i in col_names]
        # When user-type provided use, or default when partial types provided
        else:
            col_types = [types.get(col, df_table.c[col].type) for col in col_names]

    # Remove timecode and sequence column from col_name and col_types
    # since the required columns will be created automatically
    if timecode_column in col_names:
        ind = col_names.index(timecode_column)
        col_names.pop(ind)
        col_types.pop(ind)

    if sequence_column is not None and sequence_column in col_names:
        ind = col_names.index(sequence_column)
        col_names.pop(ind)
        col_types.pop(ind)

    # Dictionary to append special flags, can be extended to add Fallback, Journalling, Log etc.
    post_params = {}
    prefix = []
    pti = post(opts=post_params)

    # Create Table object with appropriate Primary Time Index/Prefix for volatile
    if temporary:
        pti = pti.on_commit(option='preserve')
        prefix.append('VOLATILE')

    if not set_table:
        prefix.append('multiset')
    else:
        prefix.append('set')

    pti = pti.primary_time_index(timecode_datatype,
                                 name=primary_time_index_name,
                                 timezero_date=timezero_date,
                                 timebucket_duration=timebucket_duration,
                                 sequenced=True if sequence_column is not None else False,
                                 seq_max=seq_max,
                                 cols=columns_list)

    table = Table(table_name, meta,
                  *(Column(col_name, col_type)
                    for col_name, col_type in
                    zip(col_names, col_types)),
                  teradatasql_post_create=pti,
                  prefixes=prefix,
                  schema=schema_name
                  )

    return table


def _rename_column(col_names, search_for, rename_to):
    """
    Internal function to rename a column in a list of columns of a Pandas DataFrame.

    PARAMETERS:
        col_names:
            Required Argument.
            The list of column names of the Pandas DataFrame.

        search_for:
            Required Argument.
            The column name that need to be changed/renamed.

        rename_to:
            Required Argument.
            The column name that the 'search_for' column needs to be replaced with.

    RETURNS:
        A list of renamed columns list.

    EXAMPLES:
        cols = _rename_column(cols, 'col_1', 'new_col_1')
    """
    ind = col_names.index(search_for)
    col_names.pop(ind)
    col_names.insert(ind, rename_to)

    return col_names


def _rename_to_pti_columns(col_names, timecode_column, sequence_column, timecode_column_index=None, sequence_column_index=None):
    """
    Internal function to generate a list of renamed columns of a Pandas DataFrame to match that of the PTI table column names
    in Vantage, or revert any such changes made.

    PARAMETERS:
        col_names:
            The list of column names of the Pandas DataFrame.

        timecode_column:
            The column name that reflects the timecode column in the PTI table.

        sequence_column:
            The column name that reflects the sequence column in the PTI table.

        timecode_column_index:
            The index of the timecode column. When Specified, it indicates that a reverse renaming operation is to be
            performed.

        sequence_column_index:
            The index of the timecode column. When Specified, it indicates that a reverse renaming operation is to be
            performed.

    RETURNS:
        A list of renamed PTI related columns.

    EXAMPLES:
        cols = _rename_to_pti_columns(cols, timecode_column, sequence_column, t_index=None, s_index)
        cols = _rename_to_pti_columns(cols, timecode_column, sequence_column)
    """
    # Rename the timecode_column to what it is in Vantage
    if timecode_column_index is not None:
        col_names = _rename_column(col_names, CopyToConstants.TD_TIMECODE, timecode_column)
    else:
        col_names = _rename_column(col_names, timecode_column, CopyToConstants.TD_TIMECODE)

    # Rename the sequence_column to what it is in Vantage
    if sequence_column is not None:
        if sequence_column_index is not None:
            col_names = _rename_column(col_names, CopyToConstants.TD_SEQNO, sequence_column)
        else:
            col_names = _rename_column(col_names, sequence_column, CopyToConstants.TD_SEQNO)

    return col_names


def _reorder_insert_list_for_pti(df_column_list, timecode_column, sequence_column, df_col_type_list = None):
    """
    Internal function to reorder the list of columns used to construct the 'INSERT INTO'
    statement as required when the target table is a PTI table.

    PARAMETERS:
        df_column_list:
            A list of column names for the columns in the DataFrame.

        timecode_column:
            The timecode_columns which should be moved to the first position.

        sequence_column:
            The timecode_columns which should be moved to the first position.

        df_col_type_list:
            Optionally reorder the list containing the types of the columns to match the
            reordering the of df_column_list.

    RETURNS:
        A reordered list of columns names for the columns in the DataFrame.
        If the optional types list is also specified, then a tuple of the list reordered columns names
        and the list of the column types.

    EXAMPLE:
        new_colname_list = _reorder_insert_list_for_pti(df_column_list, timecode_column, sequence_column)
        new_colname_list, new_type_list = _reorder_insert_list_for_pti(df_column_list, timecode_column,
                                                                       sequence_column, df_col_type_list)
    """
    # Reposition timecode (to the first) and sequence column (to the second)
    # in df_column_list
    timecode_column_index = df_column_list.index(timecode_column)
    df_column_list.insert(0, df_column_list.pop(timecode_column_index))
    if df_col_type_list is not None:
        df_col_type_list.insert(0, df_col_type_list.pop(timecode_column_index))

    if sequence_column is not None:
        sequence_column_index = df_column_list.index(sequence_column)
        df_column_list.insert(1, df_column_list.pop(sequence_column_index))
        if df_col_type_list is not None:
            df_col_type_list.insert(0, df_col_type_list.pop(sequence_column_index))

    if df_col_type_list is not None:
        return df_column_list, df_col_type_list
    else:
        return df_column_list


def _check_dataframe(df):
    """
    This is an internal function used for DF validation.
    Returns True when object passed is a Pandas or teradataml DataFrame.
    False otherwise.

    PARAMETERS:
        df : The Pandas DataFrame object to be saved.

    RETURNS:
        Boolean (True/False)

    RAISES:
        N/A

    EXAMPLES:
        _check_dataframe(df = my_df)

    """
    if isinstance(df, pd.DataFrame) and len(df.columns) > 0:
        return True
    elif isinstance(df, tdmldf.DataFrame) and len(df._metaexpr.c) > 0:
        return True
    else:
        return False


def _check_columns_insertion_compatible(table1_col_object, table2_col_object, is_pandas_df = False,
                                        is_pti = False, timecode_column=None, sequence_column = None):
    """
    This is an internal function used to extract column information for two SQLAlchemy ColumnExpression objects;
    and check if column names and types are matching to determine table insertion compatibility.

    PARAMETERS:
        table1_col_object:
            SQLAlchemy ColumnExpression Object for first table.
        
        table2_col_object:
            SQLAlchemy ColumnExpression Object for second table (for teradataml DataFrames).
        
        is_pandas_df:
            Flag specifying whether the table objects to check are pandas DataFrames or not
            Default: False    
            Note: When this flag is True, table_2_col_object is passed with a tuple object of 
            ([column_names], [column_types])

        is_pti:
            Boolean flag indicating if the target table is a PTI table.

        timecode_column:
            timecode_column required to order the select expression for the insert.
            It should be the first column in the select expression.

        sequence_column:
            sequence_column required to order the select expression for the insert.
            It should be the second column in the select expression.


    RETURNS:
        a) True, when insertion compatible (names & types match)
        b) False, otherwise

    RAISES:
        N/A

    EXAMPLES:
        _check_columns_insertion_compatible(table1.c, table2.c, True)
        _check_columns_insertion_compatible(table1.c, table2.c, True, True, 'ts', 'seq')

    """
    table1_col_names = [col.name for col in table1_col_object]
    
    # teradataml DataFrames check compatibility
    if not is_pandas_df:
        table2_col_names = [col.name for col in table2_col_object]

        if is_pti is True:
            # Reposition timecode (to the first) and sequence column (to the second)
            # with their names as generaated by the database, in col_name and col_types
            # since that is the default position of the columns
            if timecode_column in table2_col_names:
                ind = table2_col_names.index(timecode_column)
                table2_col_names.pop(ind)
                table2_col_names.insert(0, CopyToConstants.TD_TIMECODE)

            if sequence_column is not None and sequence_column in table2_col_names:
                ind = table2_col_names.index(sequence_column)
                table2_col_names.pop(ind)
                table2_col_names.insert(1, CopyToConstants.TD_SEQNO)

        if not all(col in table1_col_names for col in table2_col_names):
            return False
        
        for col_name in table1_col_names:
            # When the target table is a PTI table, ignore the TD_TIMEBUCKET column since
            # it is managed by the database and cannot be manipulated by SQL code
            table2_col_name = col_name
            if is_pti is True:
                if col_name == CopyToConstants.TD_TIMEBUCKET:
                    continue
                if col_name == CopyToConstants.TD_TIMECODE:
                    table2_col_name = timecode_column
                elif col_name == CopyToConstants.TD_SEQNO:
                    table2_col_name = sequence_column

            if type(table1_col_object[col_name].type) != type(table2_col_object[table2_col_name].type):
                return False

        return True

    # Pandas DataFrames check compatibility
    else:
        table2_col_names = table2_col_object[0]

        if is_pti is True:
            table2_col_names = _rename_to_pti_columns(table2_col_names, timecode_column, sequence_column)

        # When types mismatch, database is allowed to handle any resulting error.
        if not all(col in table1_col_names for col in table2_col_names):
            return False
        
        return True


def _extract_column_info(df):
    """
    This is an internal function used to extract column information for a DF, for Table creation manually.

    PARAMETERS:
        df : The Pandas DataFrame object to be saved.

    RETURNS:
        a) List of DataFrame Column names
        b) List of equivalent SQLAlchemy Column Types for Pandas Column Types

    RAISES:
        N/A

    EXAMPLES:
        _extract_column_info(df = my_df)

    """
    col_names = df.columns.values.tolist()
    col_types = [_get_sqlalchemy_mapping(str(df.dtypes[key])) for key in list(range(0, len(df.columns)))]
    return col_names, col_types


def _extract_column_info_from_types(df, types):
    """
    This is an internal function used to extract column information from a user provided type dictionary.
    Used internally in user API's such as copy_to_sql for Table creation manually.

    PARAMETERS:
        df: The Pandas DataFrame object to be saved.
        types : A python dictionary with column names and required types as key-value pairs.

    RETURNS:
        a) List of DataFrame Column names
        b) List of corresponding teradatasqlalchemy Column Types

    RAISES:
        N/A

    EXAMPLES:
        col_names, col_types = _extract_column_info_from_types(df = df, types = types)

    """
    col_names = df.columns.values.tolist()
    
    # When user provides partial type dictionary, default the rest.
    col_types = [types.get(col_name) if col_name in types else _get_sqlalchemy_mapping(str(df.dtypes[key])) 
                 for key, col_name in enumerate(list(df.columns))]

    return col_names, col_types


def _insert_data(df, table_name, con, index, index_label, schema_name, is_pti, timecode_column, sequence_column):
    """
    This is an internal function used to pandas.io.sql (to_sql) with 'Append' Mode.
    Used for Default Table creation & to separate Table DDL from Insertions.

    PARAMETERS:
        df:
            The Pandas DataFrame object to be saved.

        table_name:
            Name of SQL table.

        con:
            A SQLAlchemy connectable (engine/connection) object

        index:
            Flag specifying whether to write Pandas DataFrame index as a column or not.

        index_label:
            Column label for index column(s).
        
        schema_name:
            Name of the database schema to use to save the table.

        is_pti:
            Boolean flag indicating if the table should be a PTI table.

        timecode_column:
            timecode_column required to order the select expression for the insert.
            It should be the first column in the select expression.

        sequence_column:
            sequence_column required to order the select expression for the insert.
            It should be the second column in the select expression.

    RETURNS:
        N/A

    RAISES:
        N/A

    EXAMPLES:
        _insert_data(df = my_df, table_name = 'test_table', con = tdconnection,
                     index = True, index_label = None, schema = schema_name)
    """
    new_df = df

    try:

        if is_pti is True:
            cols = df.columns.tolist()
            cols = _reorder_insert_list_for_pti(cols, timecode_column, sequence_column)

            new_df = df[cols]
            cols = _rename_to_pti_columns(cols, timecode_column, sequence_column)
            new_df.columns = cols

        return new_df.to_sql(table_name, con, if_exists = 'append', index = False, index_label = index_label, schema = schema_name)
    except Exception:
        raise


def _insert_from_dataframe(df, con, schema_name, table_name, index, index_label, types,
                           is_pti=False, timecode_column=None, sequence_column=None):
    """
    This is an internal function used to to sequentially extract column info from DF,
    iterate rows, and insert rows manually.
    Used for Insertions to Temporary Tables & Tables with Pandas index.

    This uses DBAPI's executeMany() which is a batch insertion method.

    PARAMETERS:
        df:
            The Pandas DataFrame object to be saved.

        schema_name:
            Name of the schema.

        table_name:
            Name of the table.

        con:
            A SQLAlchemy connectable (engine/connection) object

        index:
            Flag specifying whether to write Pandas DataFrame index as a column or not.

        index_label:
            Column label for index column(s).
        
        types:
            A python dictionary with column names and required types as key-value pairs.

        is_pti:
            Boolean flag indicating if the table should be a PTI table.

        timecode_column:
            timecode_column required to order the select expression for the insert.
            It should be the first column in the select expression.

        sequence_column:
            sequence_column required to order the select expression for the insert.
            It should be the second column in the select expression.

    RETURNS:
        N/A

    RAISES:
        N/A

    EXAMPLES:
        _insert_from_dataframe(df = my_df, schema = None, table_name = 'test_table', con = tdconnection,
                               index = True, index_label = None)
    """
    new_df = df

    if types is None:
        col_names, col_types = _extract_column_info(new_df)
    else:
        col_names, col_types = _extract_column_info_from_types(new_df, types)

    # Quoted, schema-qualified table name
    table = '"{}"'.format(table_name)
    if schema_name is not None:
        table = '"{}".{}'.format(schema_name, table_name)

    try:

        if is_pti:
            # This if for non-index columns.
            col_names, col_types = _reorder_insert_list_for_pti(col_names,
                                                                timecode_column,
                                                                sequence_column,
                                                                df_col_type_list=col_types)

            new_df = df[col_names]
            cols = _rename_to_pti_columns(col_names, timecode_column, sequence_column)
            new_df.columns = cols
            col_names = cols

        insert_list = []

        ins = "INSERT INTO {} VALUES {}".format(
            table,
            '(' + ', '.join(['?' for i in range(len(col_names) + 1 if index is True else len(col_names))]) + ')')

        for ind, row in new_df.iterrows():
            ins_dict = ()
            for x in col_names:
                ins_dict = ins_dict + (row[x],)

            if index is True:
                ins_dict = ins_dict + (row.name,)

            insert_list.append(ins_dict)

        #Batch Insertion (using DBAPI's executeMany) used here to insert list of dictionaries
        con.execution_options(autocommit=True).execute(ins, *(r for r in insert_list))

    except Exception:
        raise


# TODO: Confirm whether required anymore/re-factor or remove if redundant.
def _insert_sequentially_from_dataframe(df, con, table, index, index_name):
    """
    This is an internal function used to to sequentially extract column info from DF,
    iterate rows, and insert rows manually - Sequentially.
    Used for Insertions to Temporary Tables & Tables with Pandas index
    Encountered to_sql insertion support issues.

    This is a SEQUENTIAL INSERT - In place only until GoSQL Driver supports
    Batch insertion - At which point the above _insert_from_dataframe (which
    Supports BATCH INSERTION) will be used.

    PARAMETERS:
        df : The Pandas DataFrame object to be saved.

        table: A SQLAlchemy Table construct/object.

        con : A SQLAlchemy connectable (engine/connection) object

        index : Flag specifying whether to write Pandas DataFrame index as a column or not.

        index_label : Column label for index column(s).

    RETURNS:
        N/A

    RAISES:
        N/A

    EXAMPLES:
        _insert_from_dataframe(df = my_df, schema= None, table_name = 'test_table', con = tdconnection,
                               index = True, index_label = None)
    """
    col_names, col_types = _extract_column_info(df)

    columns = []
    values = []

    for ind, row in df.iterrows():
        for x in col_names:
            columns.append(x)
            values.append(row[x])

        if index is True:
            if index_name in ('', None):
                index_name = 'index_label'
            columns.append(index_name)
            values.append(row.name)

        ins_dict = {}
        for col_no in range(len(columns)):
            ins_dict[columns[col_no]] = values[col_no]

        ins = table.insert().values(ins_dict)
        con.execution_options(autocommit=True).execute(ins)

        columns.clear()
        values.clear()


def _get_sqlalchemy_mapping(key):
    """
    This is an internal function used to returns a SQLAlchemy Type Mapping
    for a given Pandas DataFrame column Type.
    Used for Table Object creation internally based on DF column info.

    For an unknown key, String (Mapping to VARCHAR) is returned

    PARAMETERS:
        key : String representing Pandas type ('int64', 'object' etc.)

    RETURNS:
        SQLAlchemy Type (Integer, String, Float, DateTime etc.)

    RAISES:
        N/A

    EXAMPLES:
        _get_sqlalchemy_mapping(key = 'int64')
    """
    teradata_types_map = _get_all_sqlalchemy_mappings()

    if key in teradata_types_map.keys():
        return teradata_types_map.get(key)
    else:
        return VARCHAR(configure.default_varchar_size,charset='UNICODE')


def _get_all_sqlalchemy_mappings():
    """
    This is an internal function used to return a dictionary of all SQLAlchemy Type Mappings.
    It contains mappings from pandas data type to SQLAlchemyTypes

    PARAMETERS:

    RETURNS:
        dictionary { pandas_type : SQLAlchemy Type}

    RAISES:
        N/A

    EXAMPLES:
        _get_all_sqlalchemy_mappings()
    """
    teradata_types_map = {'int32':INTEGER, 'int64':BIGINT,
                          'object':VARCHAR(configure.default_varchar_size,charset='UNICODE'),
                          'O':VARCHAR(configure.default_varchar_size,charset='UNICODE'),
                          'float64':FLOAT, 'float32':FLOAT, 'bool':BYTEINT,
                          'datetime64':TIMESTAMP, 'datetime64[ns]':TIMESTAMP,
                          'timedelta64[ns]':VARCHAR(configure.default_varchar_size,charset='UNICODE'),
                          'timedelta[ns]':VARCHAR(configure.default_varchar_size,charset='UNICODE')}

    return teradata_types_map


def _validate_timezero_date(timezero_date):
    """
    Internal function to validate timezero_date specified when creating a
    Primary Time Index (PTI) table.

    PARAMETERS:
        timezero_date:
            The timezero_date passed to primary_time_index().

    RETURNS:
        True if the value is valid.

    RAISES:
        ValueError when the value is invalid.

    EXAMPLE:
        _validate_timezero_date("DATE '2011-01-01'")
        _validate_timezero_date('2011-01-01') # Invalid
    """
    # Return True is it is not specified or is None since it is optional
    if timezero_date is None:
        return True

    pattern = re.compile(CopyToConstants.pattern_timezero_date)
    match = pattern.match(timezero_date)

    err_msg = Messages.get_message(MessageCodes.INVALID_ARG_VALUE).format(timezero_date,
                                                                          'timezero_date',
                                                                          "str of format DATE 'YYYY-MM-DD'")

    try:
        datetime.datetime.strptime(match.group(1), '%Y-%m-%d')
    except (ValueError, AttributeError):
        raise TeradataMlException(err_msg,
                                  MessageCodes.INVALID_ARG_VALUE)

    # Looks like the value is valid
    return True


def _validate_timebucket_duration(timebucket_duration):
    """
    Internal function to validate timeduration_bucket specified when creating a
    Primary Time Index (PTI) table.

    PARAMETERS:
        timebucket_duration:
            The timebucket_duration passed to copy_to().

    RETURNS:
        True if the value is valid.

    RAISES:
        ValueError or TeradataMlException when the value is invalid.

    EXAMPLES:
        _validate_timebucket_duration('HOURS(2)')
        _validate_timebucket_duration('2hours')
        _validate_timebucket_duration('ayear') # Invalid
    """
    # Return True is it is not specified or is None since it is optional
    if timebucket_duration is None:
        return True

    # Message for error to be raise when n is invalid
    n_err_msg = "'n' must be a positive integer. Found: {}"

    # Check if notation if formal or shorthand (beginning with a digit)
    if timebucket_duration[0].isdigit():
        valid_timebucket_durations = CopyToConstants.valid_timebucket_durations_shorthand
        pattern_to_use = CopyToConstants.pattern_timebucket_duration_short
        normalized_timebucket_duration = timebucket_duration.lower()
    else:
        valid_timebucket_durations = CopyToConstants.valid_timebucket_durations_formal
        pattern_to_use = CopyToConstants.pattern_timebucket_duration_formal
        normalized_timebucket_duration = timebucket_duration.upper()

    for timebucket_duration_notation in valid_timebucket_durations:
        pattern = re.compile(pattern_to_use.format(timebucket_duration_notation))
        match = pattern.match(normalized_timebucket_duration)
        if match is not None:
            try:
                n = int(match.group(1))
                if n < 0:
                    raise ValueError(n_err_msg.format(n))

                # Looks like the value is valid
                return True
            except ValueError:
                raise ValueError(n_err_msg.format(match.group(1)))

    # Match not found
    raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_ARG_VALUE).format(timebucket_duration,
                                                                                          'timebucket_duration',
                                                                                          'a valid time unit of format time_unit(n) '
                                                                                          'or it\'s short hand equivalent notation'),
                              MessageCodes.INVALID_ARG_VALUE)
