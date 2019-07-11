from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_restful import Api
from werkzeug.exceptions import NotFound

from .conf import log
from .conf.log import LOG_FILE_MAX_BYTES
from .conf.log import LOG_FILE_BACKUP_COUNT
from .conf.log import LOG_FORMATTER
from .controller.response import Response
from .log import logger
from .utils.package import Package
from .router import Router
from .utils.utype import *
from .view import ViewBase

__all__ = ('Pysubway', 'logger', 'ViewBase')


class Pysubway:

    def __init__(self, app_name: str, app: Flask = None, prefix: str = '',
                 default_mediatype='application/json', decorators=None,
                 catch_all_404s=False, serve_challenge_on_401=False,
                 url_part_order='bae', errors=None):
        self.app_name = app_name
        self.app = app or Flask(self.app_name)
        if len(prefix) > 0 and not prefix.startswith('/'):
            raise Exception('prefix must start with slash')
        self.api = Api(app, prefix=prefix,
                       default_mediatype=default_mediatype, decorators=decorators,
                       catch_all_404s=catch_all_404s, serve_challenge_on_401=serve_challenge_on_401,
                       url_part_order=url_part_order, errors=errors)

    def new(self, db, conf_path: str, router: Dict[str, Any], *args: Dict[str, Any]):
        CORS(self.app, supports_credentials=True)
        self.bind_conf(conf_path)
        self.bind_db(db)
        self.bind_log(self.app_name)
        self.bind_router(router, *args)
        return self.app

    def bind_router(self, router: Dict[str, Any], *args: Dict[str, Any]):
        Router.bind(self.api, router, *args)

    def bind_db(self, db):
        db.init_app(self.app)

    def bind_conf(self, conf_path: str):
        attrs = Package(conf_path).conf_attrs(upper=True)
        self.app.config.from_mapping(attrs)

    def bind_log(self, app_name: str, error_path: str = None, info_path: str = None,
                 file_max_bytes: int =LOG_FILE_MAX_BYTES,
                 file_backup_count: int = LOG_FILE_BACKUP_COUNT, formatter_info: str =LOG_FORMATTER,
                 formatter_error: str = LOG_FORMATTER):
        log.Log(self.app, app_name, error_path=error_path, info_path=info_path,
                file_max_bytes=file_max_bytes,
                file_backup_count=file_backup_count, formatter_info=formatter_info,
                formatter_error=formatter_error)


def handle_exception(e):
    raw = Response.system_error()
    if isinstance(e, NotFound):
        return Response.not_found()
    return jsonify(raw)
