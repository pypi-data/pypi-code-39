"""
    Helpers for SqlAlchemy connections
"""
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bluemax.settings import get_settings

LOGGER = logging.getLogger(__name__)


_SESSION_EXTENSIONS_ = []
_SESSION_KWARGS_ = {"autoflush": False}
_pool_recycle_ = 60


class ConnectionCache:
    """ Cache of Engine and Session for db_urls """

    connections = {}

    def __init__(self, name, url, **kwargs):
        self.name = name
        self.url = url
        LOGGER.debug("connecting to db: %s", url)
        self.session, self.engine = self.connect(url, **kwargs)
        self.connections[self.name] = self

    @classmethod
    def get(cls, name):
        """ return cached connection """
        return cls.connections.get(name)

    @classmethod
    def connect(cls, db_url, echo=False, pool_recycle=None, **kwargs):
        """ Connect to db and provide engine and Session """

        params = dict(echo=echo)
        if 'mysql' in db_url:
            params['encoding'] = 'utf-8'
            params[
                'pool_recycle'] = pool_recycle if pool_recycle else _pool_recycle_
            params['isolation_level'] = 'READ COMMITTED'
        params.update(kwargs)

        engine_ = create_engine(db_url, **params)
        session_ = sessionmaker(bind=engine_)
        return session_, engine_

    @classmethod
    def setup_db(cls, base_name="db_url", db_url=None, **kwargs):
        """ Create a connection and cache it """
        logging.debug("setUp(%r)", base_name)
        session_ = cls.get(base_name)
        if session_ is None:
            url = db_url if db_url else get_settings(base_name)
            session_ = cls(base_name, url, **kwargs)
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
