import pandas as pd
import sqlite3
from functools import wraps
import uuid


def random_suffix(s):
    return '{}_{}'.format(s, uuid.uuid4().hex[:5])


class SQL:
    """An database interface that integrated Dataframe and SQL.

    Parameters
    ==========
    database : str
        path to the database.
    """

    def __init__(self, database):
        self._conn = sqlite3.connect(
            database, detect_types=sqlite3.PARSE_DECLTYPES)
        self._conn.row_factory = sqlite3.Row

    @wraps(pd.DataFrame.to_sql)
    def to_sql(self, df, **kwargs):
        kwargs['con'] = self._conn
        df.to_sql(**kwargs)

    def merge(self, df, table, how='left', left_on=None, right_on=None, on=None, right_cols=None):
        """ Merge a SQL table to dataframe.

        Parameters
        ==========
        df : dataframe
        table : str, SQL table name
        how : str, ['inner', 'left', 'leftonly']
            inner - return rows that appear in both df and SQL table
            left  - keep all rows in df, attach matched columns from SQL table
            leftonly - return rows that appear in df but not SQl table
        left_on - str, list
            key column(s) of df. Order matters. Cannot be specified with 'on' parameter. 
        right_on - str, list
            key column(s) of SQL table. Order matters. Cannot be specified with 'on' parameter. 
        on - str, list
            key column(s) of df & SQL table. Cannot be specified with 'left_on' or 'right_on'.
        right_cols - list
            columns from the SQL table to merge to df.
        """
        assert table in self.tables(), 'Table {} does not exist.'.format(table)
        assert (left_on is None and right_on is None and on is not None) or \
            (left_on is not None and right_on is not None and on is None), 'Use parameter on, or left_on and right_on.'

        if on is not None:
            left_on = right_on = on

        left_on = [left_on] if isinstance(left_on, str) else left_on
        right_on = [right_on] if isinstance(right_on, str) else right_on

        for col in left_on:
            assert col in df.columns.tolist(), 'Column {} not in dataframe.'.format(col)
        for col in right_on:
            assert col in self.columns(
                table), 'Column {} not in table {}'.format(col, table)

        if right_cols is not None:
            for col in right_cols:
                assert col in self.columns(
                    table), 'Column {} not in table {}'.format(col, table)
        else:
            right_cols = self.columns(table)

        tmptable = random_suffix('__tmp_merge')
        self.to_sql(df, name=tmptable)

        # build query
        query_template = """
            select a.*
            from {dftable} as a
            {jointype} join {sqltable} as b
            on {criteria}
            {whereclause}
        """
        crit = ' '.join(['a.{}=b.{}'.format(dfcol, tblcol)
                         for dfcol, tblcol in zip(left_on, right_on)])
        sqltbl_anykey = 'b.{}'.format(right_on[0])

        if how == 'left':
            jointype = 'left'
            whereclause = ''
        elif how == 'leftonly':
            jointype = 'left'
            whereclause = "where {sqltable_anykey} is NULL".format(
                sqltable_anykey=sqltbl_anykey)
        elif how == 'inner':
            jointype = 'inner'
            whereclause = ''

        query = query_template.format(
            dftable=tmptable,
            jointype=jointype,
            sqltable=table,
            criteria=crit,
            whereclause=whereclause,
        )

        resultdf = self.read_query(query)

        self.drop(tmptable)
        return resultdf

    def drop(self, table):
        """Drop a table from database"""
        if table not in self.tables():
            raise ValueError('Table {} does not exist.'.format(table))
        else:
            self.execute('DROP TABLE {}'.format(table))

    def read_query(self, sql, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None):
        """Ported API from pd.read_sql_query."""
        return pd.read_sql_query(sql=sql,
                                 con=self._conn,
                                 index_col=index_col,
                                 coerce_float=coerce_float,
                                 params=params,
                                 parse_dates=parse_dates,
                                 chunksize=chunksize)

    def execute(self, sql, parameters=None):
        "Ported from sqlite3.Connection.execute()."
        return self._conn.execute(sql)

    def commit(self):
        "Commit changes."
        self._conn.commit()

    def executemany(self, sql, parameters, commit=True):
        """Ported from sqlite3.Connection.executemany().

        Parameters
        ==========
        commit : bool, default True
            Commit changes after executing the command.
        """
        status = self._conn.executemany(sql, parameters)
        if commit:
            self.commit()
        return status

    def close(self):
        self._conn.close()

    def tables(self):
        "Return a list of table names in the database."
        return self.read_query("""SELECT tbl_name FROM sqlite_master
                                WHERE type=='table'""")['tbl_name'].tolist()

    def columns(self, tbl_name):
        "Return a list of column names in a table."
        assert ' ' not in tbl_name, "Invalid table name '{}'".format(tbl_name)
        cursor = self._conn.execute(
            "select * from {} limit 1".format(tbl_name))
        names = list(map(lambda x: x[0], cursor.description))
        return names

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
