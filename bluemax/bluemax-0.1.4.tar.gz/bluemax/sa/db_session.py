"""
    Helpers for SqlAlchemy connections
"""
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bluemax.settings import get_settings

LOGGER = logging.getLogger(__name__)


class ConnectionCache:
    """ Cache of Engine and Session for db_urls """

    connections = {}

    def __init__(self, name, url):
        self.name = name
        self.url = url
        LOGGER.info("connecting to db: %s", url)
        self.session, self.engine = self.connect(url)
        self.connections[self.name] = self

    @classmethod
    def get(cls, name):
        """ return cached connection """
        return cls.connections.get(name)

    @classmethod
    def connect(cls, db_url, echo=False):
        """ Connect to db and provide engine and Session """
        engine_ = create_engine(db_url, echo=echo)
        session_ = sessionmaker(bind=engine_)
        return session_, engine_

    @classmethod
    def setup_db(cls, base_name="db_url", db_url=None):
        """ Create a connection and cache it """
        logging.info("setUp(%r)", base_name)
        session_ = cls.get(base_name)
        if session_ is None:
            url = db_url if db_url else get_settings(base_name)
            session_ = cls(base_name, url)
        return session_.engine, session_.session


@contextmanager
def session(session_cls):
    """Provide a transactional scope around a series of operations."""
    session_obj = session_cls()
    try:
        yield session_obj
        session_obj.commit()
    except Exception:
        session_obj.rollback()
        raise
    finally:
        session_obj.close()


def session_scope(base_name="default", db_url=None):
    """Provide a transactional scope around a series of operations."""
    if ConnectionCache.get(base_name) is None:
        ConnectionCache.setup_db(base_name, db_url)
    return session(ConnectionCache.get(base_name).session)
