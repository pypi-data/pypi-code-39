from robot.libraries.BuiltIn import BuiltIn
from urllib import parse


class MongoConnectionManager(object):
    """
    Connection Manager handles the connection & disconnection to the database.
    """

    def __init__(self):
        """
        Initializes _dbconnection to None.
        """
        self._dbconnection = None
        self._builtin = BuiltIn()


    def connect_to_mongodb(self, dbHost='localhost', dbPort=27017, dbMaxPoolSize=10, dbNetworkTimeout=None,
                           dbDocClass=dict, dbTZAware=False):
        """
        Loads pymongo and connects to the MongoDB host using parameters submitted.
        
        Example usage:
        | # To connect to foo.bar.org's MongoDB service on port 27017 |
        | Connect To MongoDB | foo.bar.org | ${27017} |
        | # Or for an authenticated connection, note addtion of "mongodb://" to host uri |
        | Connect To MongoDB | mongodb://admin:admin@foo.bar.org/dbName | ${27017} |
        
        """
        dbapiModuleName = 'pymongo'
        db_api_2 = __import__(dbapiModuleName)
        
        dbPort = int(dbPort)
        #print "host is               [ %s ]" % dbHost
        #print "port is               [ %s ]" % dbPort
        #print "pool_size is          [ %s ]" % dbPoolSize
        #print "timeout is            [ %s ]" % dbTimeout
        #print "slave_okay is         [ %s ]" % dbSlaveOkay
        #print "document_class is     [ %s ]" % dbDocClass
        #print "tz_aware is           [ %s ]" % dbTZAware
        print("| Connect To MondoDB | dbHost | dbPort | dbMaxPoolSize | dbNetworktimeout | dbDocClass | dbTZAware |")
        print("| Connect To MondoDB | %s | %s | %s | %s | %s | %s |" % (dbHost, dbPort, dbMaxPoolSize, dbNetworkTimeout,
                                                                        dbDocClass, dbTZAware))

        self._dbconnection = db_api_2.MongoClient(host=dbHost, port=dbPort, socketTimeoutMS=dbNetworkTimeout,
                                         document_class=dbDocClass, tz_aware=dbTZAware,
                                         maxPoolSize=dbMaxPoolSize)
    def connect_to_mongodb_with_auth(self, username, password, dbName, dbHost='localhost', dbPort=27017, dbMaxPoolSize=10, dbNetworkTimeout=None,
                           dbDocClass=dict, dbTZAware=False):
        """
        Loads pymongo and connects to the MongoDB host using parameters submitted.
        
        Example usage:
        | # To connect to foo.bar.org's MongoDB service on port 27017 with an authenticated connection, note addtion of "mongodb://" to host uri |
        | Connect To MongoDB | mongodb://admin:admin@host/dbName | ${27017} |
        
        """
        dbapiModuleName = 'pymongo'
        db_api_2 = __import__(dbapiModuleName)
        
        dbPort = int(dbPort)
        # 连接MongoDB的时候设置用户名和密码，则必须根据RFC 3986转义用户名和密码
        username = parse.quote_plus(username)
        password = parse.quote_plus(password)
        connURL = 'mongodb://{}:{}@{}:{}/{}'.format(username,password,dbHost,dbPort,dbName)
        #print("host is               [ %s ]") % dbHost
        #print("port is               [ %s ]") % dbPort
        #print("pool_size is          [ %s ]") % dbPoolSize
        #print("timeout is            [ %s ]") % dbTimeout
        #print("slave_okay is         [ %s ]") % dbSlaveOkay
        #print("document_class is     [ %s ]") % dbDocClass
        #print("tz_aware is           [ %s ]") % dbTZAware
        print("| Connect To MondoDB | connURL | dbPort | dbMaxPoolSize | dbNetworktimeout | dbDocClass | dbTZAware |")
        print("| Connect To MondoDB | %s | %s | %s | %s | %s | %s |" % (connURL, dbPort, dbMaxPoolSize, dbNetworkTimeout,
                                                                        dbDocClass, dbTZAware))

        self._dbconnection = db_api_2.MongoClient(host=connURL, socketTimeoutMS=dbNetworkTimeout,
                                         document_class=dbDocClass, tz_aware=dbTZAware,
                                         maxPoolSize=dbMaxPoolSize)
        
    def disconnect_from_mongodb(self):
        """
        Disconnects from the MongoDB server.
        
        For example:
        | Disconnect From MongoDB | # disconnects from current connection to the MongoDB server | 
        """
        print("| Disconnect From MongoDB |")
        self._dbconnection.close()
