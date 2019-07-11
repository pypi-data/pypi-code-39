import time
try:
    import mysql.connector as mysql
except ImportError:
    print("Warn: unable to import mysql-connector; assuming uninstalled. remote_db will not work.")


from .ssh_tunnel import *

class RemoteDB(SSHLocalTunnel):
    """ Barebones example of MySQL w\ Python, TODO: - convert NewQL/XQL libs to this."""

    def __init__(self,
                 tunneled_db_host,
                 db_user,
                 db_pass,
                 database,
                 db_port=4444,
                 **tunnel_args):
        """
        Constructor; inherits from RemoteDB so must also include, at minimum, a target= kword argument.
        :param tunneled_db_host: localhost, 127.0.0.1, 0.0.0.0 if you wanna be weird.
        :param db_user: eg: timerd, root
        :param db_pass: eg: mysqlpass, super@secret19191
        :param database: database to use as the index for the connector; can be changed later with change db
        :param db_port: port that mysql is running on
        :param tunnel_args: REQUIRED: at least target=, which are then passed to init to construct the parent.
        """
        self.host = tunneled_db_host
        self.db_user = db_user
        self.db_pass = db_pass
        self.database = database
        self.db_port = db_port
        super().__init__(**tunnel_args) #open the tunnel
        while not self.fully_initialized:
            time.sleep(0.1)
        self.dbconn, self.curs = self._open_db_conn()     #boot the db connection

    def change_db(self, newdb):
        """ Change the database that we are workign with. Does not close conection."""
        self.dbconn.database = newdb
        self.database = newdb

    def _open_db_conn(self):
        """ Open conn, instantiate the cursor and then return the connection object"""
        cn = mysql.connect(host=self.host, port=self.db_port, user=self.db_user, password=self.db_pass, database=self.database, autocommit=True)
        curs = cn.cursor(buffered=True)
        return cn, curs

    def query(self, ql):
        """ Pass SQL queries to this."""
        self.curs.execute(ql)
        return "\n".join([str(x) for x in self.curs.fetchall()])


    def pull_table(self, table, key=None):
        """ Get a table, or a table by key."""
        if not key:
            return self.query("select * from {};".format(table))
        elif key:
            return self.query("select {} from {}".format(key, table))
        else:
            return False

    def close_db_conn(self):
        """ Close the DB connection, and kill the thread for good measure."""
        self.dbconn.close()
        self.kill()

