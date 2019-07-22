"""
Workspace connection for SQL Alchemy

ws_sqlalchemy is a dsws conn type library that follows PEP-249.
It contains a single class, Sqlalchemy.
It is intended to be an alternate connection type for
systems if there is user preference.
"""

import pandas          as pd
from sqlalchemy import create_engine
from dsws.util     import pretty
from dsws.util     import sp
from dsws.util     import standard_conn_qry
from dsws.util     import no_return
from os import environ as env
from ast           import literal_eval

class Sqlalchemy:

    def __init__(self,kwargs,command=None):
        """
        Workspace class from the sqlalchemy library

        As convntion for DSWS, the following class methods are
        provided:
         - conn: returns a sqlalchemy connection class
         - qry: precesses a query, return type is dependent upon r_type requested:
            - df/raw: pandas dataframe
            - disp: pretty html form of pandas dataframe
        
        Configuring a Sqlalchemy class is typically done through dsws.duct, but can also be
        evaluated as:
        ```python
        from dsws.ws_sqlalchemy import Sqlalchemy
        kwargs = {'name_or_url': 'mysql+pymysql://user:password@dbname.db.ratiocinate.com:3306/dbname'}
        sa = Sqlalchemy(kwargs)
        ```
        """
        self.conf=kwargs
        if command is not None:
            self.command=command
    
    def conn(self):
        """
        Creates a sqlalchemy connection from a sqlalchemy engine
        """
        engine = create_engine(**self.conf)
        return engine.connect()    

    def qry(self,qry,r_type="df",limit=30):
        r_type = 'df' if r_type=='raw' else r_type
        qry=standard_conn_qry(qry)
        if r_type=="cmd":
            return(qry)
        conn   = self.conn()
        for q in qry[:-1]:
            conn.execute(q)
        if r_type=="disp" and "LIMIT" not in qry[-1].split()[-2].upper() and "SELECT" in qry[-1].split()[1].upper():
            qry[-1] = qry[-1] + " LIMIT " + str(limit)
        if r_type in ("df","disp"):
            rslt = pd.read_sql(sql=qry[-1],con=conn)
            if r_type=="disp":
                pretty(rslt,col="#ff9280")
                rslt=None
        else:
            rslt=None
        conn.close()    
        return(rslt)
