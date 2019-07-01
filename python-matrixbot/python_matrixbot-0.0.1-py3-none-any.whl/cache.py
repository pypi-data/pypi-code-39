import logging, hashlib, json, sqlite3, time
from os import path

logger = logging.getLogger(__name__)


class Cache:
    """
    A basic sqlite-backed caching mechanism, intended to avoid spamming external APIs
    (or whatever)

    Defaults to an ephemeral in-memory database, but a file can be specified for
    persistence across restarts.
    """

    def __init__(self, dbfile=":memory:"):
        self.cache = {}
        self.dbfile = dbfile

    def clean_cache(self):
        """
        Purges the cache of expired values
        """
        self.init_db()
        conn = sqlite3.connect(self.dbfile)
        query = "DELETE FROM cache WHERE expires < ?"
        conn.execute(query, (time.time(),))
        conn.commit()
        pass

    def table_exists(self, table):
        """
        Checks if a given table exists in the database

        parameters:     table (str) - the table name
        returns:        True if table exists, False otherwise
        return type:    bool
        """
        conn = sqlite3.connect(self.dbfile)
        return (
            False
            if conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,)
            ).fetchone()
            is None
            else True
        )

    def init_db(self):
        """
        Creates a new 'cache' table in the db if it does't already exist
        """
        if not self.table_exists("cache"):
            conn = sqlite3.connect(self.dbfile)
            conn.execute(
                "CREATE TABLE cache(key VARCHAR(32) NOT NULL PRIMARY KEY, "
                + "value VARCHAR(4096), expires FLOAT NOT NULL)"
            )
            conn.commit()

    def gen_pk(self, key):
        """
        Returns an md5 hash of the user provided key to use as the actual key
        """
        return hashlib.md5(key.encode("utf-8")).hexdigest()

    def query(self, key):
        """
        Queries the cache table for the given key
        """
        self.init_db()
        conn = sqlite3.connect(self.dbfile)
        conn.row_factory = sqlite3.Row
        query = "SELECT key, value FROM cache WHERE key=?"
        return conn.execute(query, (self.gen_pk(key),)).fetchone()

    def insert(self, key, value, expires):
        """
        Inserts a new item

        parameters:     key (str) - unique cache key
                        value (str) - data to be cached
                        expires (int) - seconds (from now) until data expires
        """
        self.init_db()
        try:
            conn = sqlite3.connect(self.dbfile)
            query = "INSERT INTO cache (key, value, expires) VALUES(?, ?, ?)"
            conn.execute(query, (self.gen_pk(key), value, expires))
            conn.commit()
        except sqlite3.IntegrityError as e:
            # don't try to add a key that already exists
            if re.match("UNIQUE constraint failed", e):
                pass
            else:
                raise

    def fetch(self, key, callback, timeout=300):
        """
        Set/refreshes the cached result and returns it

        parameters:     key (str) - unique cache key
                        callback (func) - callback to get fresh data
                        timeout (int) - seconds until data expires
        returns:        cached data for the matching key
        return type:    varies
        """
        # remove expired keys
        self.clean_cache()
        # if the key doesn't exist, create it
        result = self.query(key)
        if result is None:
            logger.debug(f"Cache MISS: {key}")
            data = callback()
            if data is None:
                return
            # store strings as-is
            elif isinstance(data, str):
                value = data
            # otherwise, json serialize the data
            else:
                value = json.dumps(data)
            self.insert(key, value, time.time() + timeout)
        else:
            logger.debug(f"Cache HIT: {key}")
        retval = self.query(key)["value"]
        # try to deserialize the data
        try:
            return json.loads(retval)
        # if that fails, pass it through as-is
        except json.decoder.JSONDecodeError:
            logger.debug(
                f"Failed to deserialize JSON for key {key}. Passing through unchanged."
            )
            return retval
