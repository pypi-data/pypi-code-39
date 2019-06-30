from couchdb import Server as CouchdbServer
from pyramid.config import Configurator

from .constants import (
    COUCHDB_DB,
    COUCHDB_URI,
)
from .design import sync_design


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('tables', '/tables')
    config.add_route('get_number', '/{number_id:\d+}')
    config.add_route('register', '/webapp_register')
    config.add_route('login', '/webapp_login')
    config.add_route('add_post', '/webapp_add_post')
    config.add_route('search', '/webapp_search')
    config.scan()

    #  database settings
    server = CouchdbServer(COUCHDB_URI)
    config.registry.couchdb_server = server
    if COUCHDB_DB not in server:
        server.create(COUCHDB_DB)
    config.registry.db = server[COUCHDB_DB]
    sync_design(config.registry.db)  # creates views in couchdb


    return config.make_wsgi_app()
