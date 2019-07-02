# -*- coding: utf-8 -*-
"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: rameshchandra.d@teradata.com
Secondary Owner:

teradataml context
----------
A teradataml context functions provide interface to Teradata Vantage. Provides functionality to get and set a global context which
can be used by other analytical functions to get the Teradata Vantage connection.

"""
from sqlalchemy import create_engine
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.sqlbundle import SQLBundle
from teradataml.common.constants import SQLConstants
from teradataml.common.garbagecollector import GarbageCollector
from teradataml.context.aed_context import AEDContext
from teradataml.common.constants import TeradataConstants
from teradataml.common.utils import UtilFuncs
import os
import warnings
import atexit

# Store an global Teradata Vantage Connection.
# Right now user can only provide an single Vantage connection at any point of time.
td_connection = None
td_sqlalchemy_engine = None
temporary_database_name = None
user_specified_connection = False

function_alias_mappings = {}

# Current directory is context folder.
teradataml_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_folder = os.path.join(teradataml_folder, "config")

def _get_current_databasename():
    """
    Returns the database name associated with the current context.

    PARAMETERS:
        None.

    RETURNS:
        Database name associated with the current context

    RAISES:
        TeradataMlException - If Vantage connection can't be established using the engine.

    EXAMPLES:
        _get_current_databasename()
    """
    if get_connection() is not None:
        try:
            sqlbundle = SQLBundle()
            select_user_query = sqlbundle._get_sql_query(SQLConstants.SQL_SELECT_DATABASE)
            result = get_connection().execute(select_user_query)
            for row in result:
                return row[0]
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, select_user_query),
                                      MessageCodes.TDMLDF_EXEC_SQL_FAILED) from err
    else:
        return None

def _get_database_username():
    """
    Function to get the database user name.

    PARAMETERS:
        None.

    RETURNS:
        Database user name.

    RAISES:
        TeradataMlException - If "select user" query fails.

    EXAMPLES:
        _get_database_username()
    """
    if get_connection() is not None:
        try:
            sqlbundle = SQLBundle()
            select_query = sqlbundle._get_sql_query(SQLConstants.SQL_SELECT_USER)
            result = get_connection().execute(select_query)
            for row in result:
                return row[0]
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, select_query),
                                      MessageCodes.TDMLDF_EXEC_SQL_FAILED) from err
    else:
        return None

def __cleanup_garbage_collection():
    """initiate the garbage collection."""
    GarbageCollector._cleanup_garbage_collector()

def create_context(host = None, username = None, password = None,  tdsqlengine = None,
                   temp_database_name = None, logmech = None):
    """
    DESCRIPTION:
        Creates a connection to the Teradata Vantage using the teradatasql + teradatasqlalchemy DBAPI and dialect combination.
        Users can pass all required parameters (host, username, password) for establishing a connection to Vantage,
        or pass a sqlalchemy engine to the tdsqlengine parameter to override the default DBAPI and dialect combination.

    PARAMETERS:
        host:
            Optional Argument.
            Specifies the fully qualified domain name or IP address of the Teradata System.
            Types: str
        
        username:
            Optional Argument.
            Specifies the username for logging onto the Teradata Vantage.
            Types: str
        
        password:
            Optional Argument.
            Specifies the password required for the username.
            Types: str
            
        tdsqlengine:
            Optional Argument.
            Specifies Teradata Vantage sqlalchemy engine object that should be used to establish a Teradata Vantage connection.
            Types: str
            
        temp_database_name:
            Optional Argument.
            Specifies the temporary database name where temporary tables, views will be created.
            Types: str
            
        logmech:
            Optional Argument.
            Specifies the type of logon mechanism to establish a connection to Teradata Vantage. 
            Permitted Values: 'TD2', 'TDNEGO', 'LDAP' & 'KRB5'.
            Types: str

    RETURNS:
        A Teradata sqlalchemy engine object.

    RAISES:
        TeradataMlException

    EXAMPLES:
        td_sqlalchemy_engine = create_context(host = 'tdhost.labs.teradata.com', username='tduser', password = 'tdpassword')
        td_sqlalchemy_engine = create_context(tdsqlengine = teradata_sql_alchemy_engine)
        td_sqlalchemy_engine = create_context(host = 'tdhost.labs.teradata.com', username='tduser', password = 'tdpassword', logmech='TD2')
        
    """
    # Check if teradata sqlalchemy engine is provided by the user
    global td_connection
    global td_sqlalchemy_engine
    global temporary_database_name
    global user_specified_connection
    logmech_valid_values = ['TD2','TDNEGO','LDAP','KRB5']
    logmech_value = ""
    if tdsqlengine:
        try:
            if td_connection is not None:
                warnings.warn(Messages.get_message(MessageCodes.OVERWRITE_CONTEXT))
                remove_context()
            td_connection = tdsqlengine.connect()
            td_sqlalchemy_engine = tdsqlengine
            user_specified_connection = True
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.CONNECTION_FAILURE), MessageCodes.CONNECTION_FAILURE) from err
    # Check if username & password & host are provided by the user
    elif host and username and password:
        try:
            if td_connection is not None:
                warnings.warn(Messages.get_message(MessageCodes.OVERWRITE_CONTEXT))
                remove_context()
            # Check if logmech is provided by the user
            if logmech is not None:
                # Validate logmech argument value to be a string
                if not isinstance(logmech, str):
                    raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "logmech", ["str"]), MessageCodes.UNSUPPORTED_DATATYPE)
                logmech_value = '/?LOGMECH=' + logmech.upper()
                # Importing AnalyticsWrapperUtils here due to circular dependency issue
                from teradataml.common.wrapper_utils import AnalyticsWrapperUtils
                awu = AnalyticsWrapperUtils()
                awu._validate_permitted_values(logmech.upper(), logmech_valid_values, "LOGMECH")

            td_sqlalchemy_engine  = create_engine('teradatasql://'+ username +':' + password + '@'+ host + logmech_value)
            td_connection = td_sqlalchemy_engine.connect()
            user_specified_connection= False
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.CONNECTION_FAILURE), MessageCodes.CONNECTION_FAILURE) from err

    # TODO: Comment the below line, uncomment the line
    #       `vantage_version = _get_current_vantage_version()` and
    #       implement the function _get_current_vantage_version
    vantage_version = "vantage1.0"
    # vantage_version = _get_current_vantage_version()

    # TODO: We may have to add support to multiple vantage version for loading aliases, if in case
    #       alias names for vantage1.0 functions differ from vantage1.1 alias names.

    # Load function aliases from config.
    _load_function_aliases(vantage_version)

    # Assign the tempdatabase name to global
    if temp_database_name is None:
        temporary_database_name = _get_current_databasename()
    else:
        temporary_database_name = temp_database_name

    # Connection is established initiate the garbage collection
    atexit.register(__cleanup_garbage_collection)
    __cleanup_garbage_collection()
    # Initialise Dag
    __initalise_dag()
    # Return the connection by default
    return td_sqlalchemy_engine

def get_context():
    """
    DESCRIPTION:
        Returns the Teradata Vantage connection associated with the current context.

    PARAMETERS:
        None

    RETURNS:
        A Teradata sqlalchemy engine object.

    RAISES:
        None.

    EXAMPLES:
        td_sqlalchemy_engine = get_context()
        
    """
    global td_sqlalchemy_engine
    return td_sqlalchemy_engine

def get_connection():
    """
    DESCRIPTION:
        Returns the Teradata Vantage connection associated with the current context.

    PARAMETERS:
        None

    RETURNS:
        A Teradata dbapi connection object.

    RAISES:
        None.

    EXAMPLES:
        tdconnection = get_connection()
        
    """
    global td_connection
    return td_connection

def set_context(tdsqlengine, temp_database_name = None):
    """
    DESCRIPTION:
        Specifies a Teradata Vantage sqlalchemy engine as current context.

    PARAMETERS:
        tdsqlengine:
            Required Argument.
            Specifies Teradata Vantage sqlalchemy engine object that should be used to establish a Teradata Vantage connection.
            Types: str
            
        temp_database_name:
            Optional Argument.
            Specifies the temporary database name where temporary tables, views will be created.
            Types: str

    RETURNS:
        A Teradata Vantage connection object.

    RAISES:
        TeradataMlException

    EXAMPLES:
        set_context(tdsqlengine = td_sqlalchemy_engine)
        
    """
    global td_connection
    global td_sqlalchemy_engine
    global temporary_database_name
    if td_connection  is not None:
        warnings.warn(Messages.get_message(MessageCodes.OVERWRITE_CONTEXT))
        remove_context()

    if tdsqlengine:
        try:
            td_connection = tdsqlengine.connect()
            td_sqlalchemy_engine = tdsqlengine
            # Assign the tempdatabase name to global
            if temp_database_name is None:
                temporary_database_name = _get_current_databasename()
            else:
                temporary_database_name = temp_database_name
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.CONNECTION_FAILURE), MessageCodes.CONNECTION_FAILURE) from err
    else:
        return None

    # TODO: Comment the below line, uncomment the line
    #       `vantage_version = _get_current_vantage_version()` and
    #       implement the function _get_current_vantage_version
    vantage_version = "vantage1.0"
    # vantage_version = _get_current_vantage_version()

    # TODO: We may have to add support to multiple vantage version for loading aliases, if in case
    #       alias names for vantage1.0 functions differ from vantage1.1 alias names.

    # Load function aliases from config.
    _load_function_aliases(vantage_version)

    # Initialise Dag
    __initalise_dag()

    return td_connection

def remove_context():
    """
    DESCRIPTION:
        Removes the current context associated with the Teradata Vantage connection.

    PARAMETERS:
        None.

    RETURNS:
        None.

    RAISES:
        None.

    EXAMPLES:
        remove_context()
        
    """
    global td_connection
    global td_sqlalchemy_engine
    global user_specified_connection
    if user_specified_connection is not True:
        try:
            #intiate the garbage collection
            __cleanup_garbage_collection()
            td_connection.close()
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.DISCONNECT_FAILURE), MessageCodes.DISCONNECT_FAILURE) from err
    td_connection = None
    td_sqlalchemy_engine = None
    # Closing Dag
    __close_dag()
    return True

def _get_context_temp_databasename():
    """
    Returns the temporary database name associated with the current context.

    PARAMETERS:
        None.

    RETURNS:
        Database name associated with the current context

    RAISES:
        None.

    EXAMPLES:
        _get_context_temp_databasename()
    """
    global temporary_database_name
    return temporary_database_name

def __initalise_dag():
    """
        Intialises the Dag

        PARAMETERS:
            None.

        RETURNS:
            None

        RAISES:
            None.

        EXAMPLES:
            __initalise_dag()
    """
    aed_context = AEDContext()
    # Closing the Dag if previous instance is still exists.
    __close_dag()
    # TODO: Need to add logLevel and log_file functionlaity once AED is implemented these functionalities
    aed_context._init_dag(_get_database_username(),_get_context_temp_databasename(),
                           log_level=4,log_file="")

def __close_dag():
    """
    Closes the Dag

    PARAMETERS:
        None.

    RETURNS:
        None

    RAISES:
        None.

    EXAMPLES:
        __close_dag()
    """
    try:
        AEDContext()._close_dag()
    # Ignore if any exception occurs.
    except TeradataMlException:
        pass


def _load_function_aliases(vantage_version = "vantage1.0"):
    """
    Function to load function aliases for analytical functions
    based on the vantage version from configuration file.

    PARAMETERS:
        vantage_version:
            Optional Argument.
            Defines the version of the current vantage.
            This argument is for future purpose.
            Permitted Values: "vantage1.0", "vantage1.1"

    RETURNS:
        None

    RAISES:
        TeradataMLException

    EXAMPLES:
        _load_function_aliases("vantage1.1")
    """

    global function_alias_mappings
    function_alias_mappings = {}

    supported_engines = TeradataConstants.SUPPORTED_ENGINES.value

    UtilFuncs._validate_vantage_version(vantage_version)

    for engine in supported_engines.keys():
        alias_config_file = os.path.join(config_folder, supported_engines[engine]["file"])
        engine_name = supported_engines[engine]['name']

        # TODO : Attach vantage version to config file if there are changes in function aliases.
        # TODO : Add the appropriate configuration files in config folder.
        # Get alias_config_file based on vantage version
        # alias_config_file = "{}_{}".format(alias_config_file,
        #                                    supported_vantage_versions[vantage_version])

        UtilFuncs._is_alias_config_file_exists(vantage_version, alias_config_file)

        function_alias_mappings[engine_name] = \
            UtilFuncs._get_function_mappings_from_config_file(alias_config_file)

def _get_function_mappings():
    """
    Function to return function aliases for analytical functions.

    PARAMETERS:
        None

    RETURNS:
        Dict of function aliases of the format
        {'mle' : {'func_name': "alias_name", ...},
        'sqle' : {'func_name': "alias_name", ...}
        ......
        }

    RAISES:
        None

    EXAMPLES:
        get_function_aliases()
    """
    global function_alias_mappings
    return function_alias_mappings
