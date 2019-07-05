import os
import sys
import pickle
import getpass
import cx_Oracle
import sqlalchemy
from sys import argv

try:
    from settings import *
except:
    from core_framework.settings import *


class DbAttrs:
    username = None
    password = None
    servername = None
    databasename = None
    serverip = None
    serverport = None
    sidname = None
    dsnname = None


class DbConfig:
    pass


class DatabaseConfiguration():
    def __init__(self):
        self.commands()

    def delete_db_data(self):
        check_path = os.path.exists(database_config)
        if check_path is True:
            os.remove(database_config)

    def db_con_list(self):
        check_path = os.path.exists(database_config)
        if check_path is True:
            with open(database_config, 'rb') as fr:
                data = pickle.load(fr)
                return data
        else:
            return f"File does not exist on path: {database_config}"

    def add_db_conn(self, db_type, username, password, databasename, servername=None, serverip=None, serverport=None,
                    sidname=None, tnsname=None, dsname=None, lib='default', conn_name=None):
        """
        Description:
            creates new document that will contain all data required for connection strings
            or append to same doc depends on argument append
        :param str db_type: database type ms, ora, pstg
        :param str tnsname: name of the server, used when library is cx_oracle and not default
        :param str dsnname: name of dsn that must me configured in windows it is under odbc data sources
        :param str conn_name: name for the connection if None it will be number
        """
        db_type = db_type.lower()
        arguments = list(locals().keys())

        # check does database type exists
        if db_type not in db_types.keys():
            raise AttributeError(f"db_type (Database type) not recognised supported db types are {db_types.keys()}")

        # check database name type
        if db_type in ['pstg', 'ms'] and type(databasename) is not str:
            raise AttributeError(f"Database can't be {type(databasename)} unless it is ora db_type")

        # check server name for Postgre
        if db_type == 'pstg':
            if servername is None:
                servername = 'localhost'

        # precheck for Oracle database
        if db_type == 'ora':
            if (serverip is None or serverport is None or sidname is None) and tnsname is None:
                raise AttributeError(f"Oracle connection string requires (serverip, serverport, sidname)")

            # if library is cx_oracle is defined and tnsname is not provided it will be made
            if lib.lower() == 'cx_oracle':
                dsn = cx_Oracle.makedsn(serverip, serverport, sid=sidname)
                tnsname = dsn

        # precheck for Micorsoft SQL Server database
        if db_type == 'ms':
            if lib == 'default':
                if dsname is None:
                    raise AttributeError(f"Microsoft SQL Server connection string requires dsname that can be found in ODBC Data sources. or switch lib to pymssql")
            if lib.lower() == 'pymssql':
                if serverip is None or serverport is None:
                    raise AttributeError(f"Oracle connection string requires (serverip, serverport)")

        check_path = os.path.exists(database_config)
        # create config dict
        for argument in arguments:
            setattr(DbConfig, argument, locals().get(argument))
        config = {k: v for k, v in DbConfig.__dict__.items() if k in arguments and k not in []}
        print(config)

        if check_path is False:
            if conn_name is None:
                config = {0: config}
            # else:
            #     check_name =
            with open(database_config, 'wb') as fw:
                pickle.dump(config, fw)

        else:
            with open(database_config, 'rb') as fr:
                data = pickle.load(fr)
                data.update({len(data): config})
            with open(database_config, 'wb') as fw:
                pickle.dump(data, fw)

    def commands(self):
        width = 50
        lib = 'default'
        lines = '-'*width
        space = " "*round(width/3.5)
        header = f'''+{lines}+\n{space}DATABASE CONFIGURATOR{space}\n+{lines}+\n\n'''
        sys.stdout.write(header)
        sys.stdout.write("SELECT OPTION:\n[1] Add db connection\n[2] List db connections\n[3] Edit db connection\n[4] Delete connection\n[5] Delete db config file\n")
        option = input()

        if int(option) == 1:
            lines = "-"*width
            sys.stdout.write(f"{lines}\nNew db connection form initiated\n{lines}")
            sys.stdout.write("\nDatabase connection type:\n[1] Postgre\n[2] Microsoft SQL Server\n[3] Oracle\n")
            option = input()
            sys.stdout.write("\r")
            if int(option) == 1:

                while True:
                    sys.stdout.write('> Do you wanna change library that is going to be used by sqlalchemy? [y/n]\n')
                    answer = input()
                    sys.stdout.write("\r")
                    if answer.lower() not in ['y', 'n', 'yes', 'no']:
                        sys.stdout.write("Answer can be y or n. Try again..\n")
                        continue
                    break

                while True:
                    if answer.lower() in ['y', 'yes']:
                        sys.stdout.write("Lib options:\n[1] psycopg2\n[2] pg8000\n[3] default\n")
                        lib = input()
                        sys.stdout.write("\r")
                        if lib.isnumeric() is True:
                            lib = int(lib)
                            libs = {1: 'psycopg2', 2: 'pg8000', 3: 'default'}
                            if lib not in [1,2,3]:
                                sys.stdout.write("That option doesnt exist. Try again..\n")
                                continue
                            lib = libs.get(lib)
                        else:
                            sys.stdout.write("\nThat option doesnt exist. Enter option number.  Try again..\n")
                            continue
                    break

                sys.stdout.write(f"{lines}\nPostgre connection setup\n{lines}")
                while True:
                    sys.stdout.write("\nusername:")
                    username = input()
                    sys.stdout.write("\r")
                    if username.strip() == '':
                        sys.stdout.write("Username cant be blank.  Try again.")
                        continue
                    break

                while True:
                    password = getpass.getpass('password:')
                    sys.stdout.write("\r")
                    if password.strip() == '':
                        sys.stdout.write("\n\rPassword cant be blank.  Try again.\n")
                        continue
                    break

                sys.stdout.write("\nservername:")
                servername = input()
                sys.stdout.write("\r")
                if servername.strip() == '':
                    sys.stdout.write('INFO: Server name is blank default servername set to localhost')
                    servername = 'localhost'

                while True:
                    sys.stdout.write("\ndatabasename:")
                    databasename = input()
                    sys.stdout.write("\r")
                    if databasename.strip() == '':
                        sys.stdout.write("Database name cant be blank.  Try again.")
                        continue
                    break

                while True:
                    sys.stdout.write(f'{lines}\nDATA COMFIRMATION:\n{lines}\nusername:{username}\npassword:{password}\n'
                                     f'servername:{servername}\ndatabasename:{databasename}')
                    sys.stdout.write("\n> Is data above correct? [y/n]")
                    answer = input()
                    sys.stdout.write("\r")
                    if answer.lower() not in ['y', 'n', 'yes', 'no']:
                        sys.stdout.write("Answer can be y or n. Try again..\n")
                        continue
                    break

                if answer.lower() in ['y', 'yes']:
                    sys.stdout.write(f'{lines}\nTESTING CONNECTION\n{lines}\n')

                    postgre = engine_connection_strings.get('pstg')
                    lib_selection = postgre.get(lib)
                    login_data = {'username': username, 'password': password,
                                  'servername': servername, 'databasename': databasename}
                    connection_string = lib_selection.format(**login_data)
                    print(connection_string)
                    try:
                        engine = create_engine(connection_string).connect()
                    except  sqlalchemy.exc.OperationalError:
                        sys.stdout.write("Cant connect with provided data.")


if __name__ == '__main__':
    if len(argv) > 1:
        DatabaseConfiguration()

