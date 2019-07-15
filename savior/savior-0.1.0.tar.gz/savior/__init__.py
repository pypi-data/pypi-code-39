"""
Databases and transactions should be created in a `with` statement
so that their context managers can safely release resources.
Keys and values are MessagePack-encoded bytes, returned as Python objects.
Keys are a tuple of UUID, timestamp, and attribute.
Copy the data if you want to keep it after the transaction.
Timestamps are in UTC format.

This is a thin wrapper around LMDB that extends those classes.
"""

import datetime
from uuid import uuid4

import lmdb
from msgpack import packb, unpackb


# Maximum number of tables that can exist (default 1 million).
MAX_TABLES = 1_000_000
# Maximum size of database in bytes (default 1 terabyte). 
MAX_SIZE = 1_000_000_000_000

def uuid():
    """Generate a random unique ID."""
    return str(uuid4())

class SaviorException(Exception):
    """`SaviorException` represents any exception raised by this library."""
    pass

class Database():
    """
    Open the database at the given path with the given table names.
    The `tables` attribute on the returned object 
    is a dictionary of the tables within.
    """
    def __init__(self, path, tables=None):
        self.path = path
        self.table_names = tables
        self.tables = {}

    def __enter__(self):
        self.env = lmdb.open(self.path, max_dbs=MAX_TABLES, map_size=MAX_SIZE)
        # open the tables within the database
        with self.env.begin(write=True) as txn:
            if self.table_names:
                for name in self.table_names:
                    table = self.env.open_db(packb(name), txn=txn)
                    self.tables[name] = table
            else:
                with txn.cursor() as cursor:
                    for name in cursor.iternext(values=False):
                        self.tables[unpackb(name, raw=False)] = lmdb.open_db(name)

        return self

    def __exit__(self, type, value, traceback):
        self.env.close()
        # don't suppress any errors
        return False

    def transact(self, write=False):
        """Open a context managed transaction."""
        return Transaction(self, write=write)

def open(path, tables=None):
    return Database(path, tables=tables)

class Transaction:
    def __init__(self, db, write=False):
        self.db = db
        self.write = write

    def __enter__(self):                                          
        self.txn = self.db.env.begin(write=self.write)
        return self
                            
    def __exit__(self, type, value, traceback):
        # Commit the transaction if there is no exception.
        if type == None:                           
            self.txn.commit()                                     
        else:                
            self.txn.abort()                                     
        # Don't suppress any exceptions.
        return False        

    def append_entry(self, table, uuid, attribute, value):
        """Low-level interface to append a single new entry."""
        now = datetime.datetime.utcnow().isoformat()
        key = (uuid, now, attribute)
        self.txn.put(packb(key), packb(value), db=self.db.tables[table])

    def create(self, table, attrs):
        """Create a new entity with the given attribtues and return its ID."""
        id = uuid()
        for attr, value in attrs.items():
            self.append_entry(table, id, attr, value)
        return id
    
    def fetch(self, table, uuid):
        """Get an entity with the given UUID in the given table."""
        entity = {}
        with self.txn.cursor(db=self.db.tables[table]) as cursor:
            key = (uuid, '', '')
            cursor.set_range(packb(key))
            # keys are sorted in ascending time order
            for key, value in cursor.iternext():
                next_id, time, attr = unpackb(key, use_list=False, raw=False)
                if next_id != uuid:
                    break
                entity[attr] = unpackb(value, raw=False)
        return entity
    
    def update(self, table, uuid, attrs):
        """Update an entity with the given UUID and attributes."""
        for attr, value in attrs.items():
            self.append_entry(table, uuid, attr, value)
    
    def query(self, table, attrs):
        """
        Get all entities that have matching attribute-value entries.
        `attributes` is a dictionary of attributes that must match.
        Returns a dictionary of UUIDs to attribute-value dictionaries. 
        """
        entities = {}
        entity = {}
        current_id = None
        with self.txn.cursor(db=self.db.tables[table]) as cursor:
            # fetch each entity, and if attributes match, add it
            for key, value in cursor.iternext():
                uuid, time, attr = unpackb(key, use_list=False, raw=False)
                if current_id == None:
                    current_id = uuid
                if current_id != uuid:
                    # check that attributes are subset of entity
                    if attrs.items() <= entity.items():
                        entities[current_id] = entity
                    # reset local variables
                    current_id = uuid
                    entity = {}
                entity[attr] = unpackb(value, raw=False)
            # add final entity if it matches
            if attrs.items() <= entity.items():
                entities[current_id] = entity
        return entities

