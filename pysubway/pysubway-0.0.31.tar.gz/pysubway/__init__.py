import logging

import flask
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound

from .response import Response
from .conf import log
from .conf.log import LOG_FILE_BACKUP_COUNT
from .conf.log import LOG_FILE_MAX_BYTES
from .conf.log import LOG_FORMATTER
from .log import logger
from .router import Router
from .utils.file import File
from .utils.package import Package
from .utils.utype import *
from .view import ViewRestful

__all__ = ('Pysubway', 'logger', 'ViewRestful')


class Pysubway:

    @staticmethod
    def new_app_specified_template(dirname: str) -> Flask:
        """

        :param dirname: example File.this_dir(__file__)}/templates
        :return:
        """
        return Flask(__name__, template_folder=dirname)

    @staticmethod
    def set_template_folder(full_path_dirname: str = '') -> str:
        """
        declare template_folder
        :param full_path_dirname:
        :return:
        """
        if full_path_dirname:
            return full_path_dirname
        dirname: str = full_path_dirname or File.this_dir(__file__)
        return File.join_path(dirname, 'templates')

    def __init__(self, app_name: str,
                 app: Optional[Flask] = None,
                 prefix: str = '',
                 default_mediatype: str = 'application/json',
                 decorators: List = None,
                 catch_all_404s: bool = False, serve_challenge_on_401: bool = False,
                 url_part_order: str = 'bae', errors: Optional[Dict] = None):
        self.app_name: str = app_name
        self.app: Flask = app or Flask(self.app_name)
        if len(prefix) > 0 and not prefix.startswith('/'):
            raise Exception('prefix must start with slash')
        self.api = Api(app, prefix=prefix,
                       default_mediatype=default_mediatype, decorators=decorators,
                       catch_all_404s=catch_all_404s, serve_challenge_on_401=serve_challenge_on_401,
                       url_part_order=url_part_order, errors=errors)

    def new(self, db: SQLAlchemy, conf_path: str, router: Dict[str, Any], *args: Dict[str, Any]) -> Flask:
        CORS(self.app, supports_credentials=True)
        self.bind_conf(conf_path)
        self.bind_db(db)
        self.bind_log(self.app_name)
        self.bind_router(router, *args)
        return self.app

    def bind_router(self, router: Dict[str, Any], *args: Dict[str, Any]) -> None:
        Router.bind(self.api, router, *args)

    def bind_db(self, db: SQLAlchemy) -> None:
        db.init_app(self.app)

    def bind_conf(self, conf_path: str) -> None:
        attrs = Package(conf_path).conf_attrs(upper=True)
        self.app.config.from_mapping(attrs)

    def bind_log(self, app_name: str, error_path: str = None, info_path: str = None,
                 file_max_bytes: int = LOG_FILE_MAX_BYTES,
                 file_backup_count: int = LOG_FILE_BACKUP_COUNT, formatter_info: logging.Formatter = LOG_FORMATTER,
                 formatter_error: logging.Formatter = LOG_FORMATTER) -> None:
        log.Log(self.app, app_name, error_path=error_path, info_path=info_path,
                file_max_bytes=file_max_bytes,
                file_backup_count=file_backup_count, formatter_info=formatter_info,
                formatter_error=formatter_error)


def handle_exception(e: Exception) -> flask.Response:
    raw = Response.system_error()
    if isinstance(e, NotFound):
        return jsonify(Response.not_found())
    return jsonify(raw)
