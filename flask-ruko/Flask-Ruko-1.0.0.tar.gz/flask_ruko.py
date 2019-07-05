from flask import current_app, has_request_context, g
from werkzeug.exceptions import NotFound

from ruko import RukoClient, RDict
from ruko.context import RContext


class RukoDB(RDict):
    def __init__(self, app=None, host=None, port=None, key_error=NotFound):
        super().__init__([], RContext(None, None, obj=g), key_error)
        self.context.create_conn = self._create_conn
        self._app = app
        if app:
            self.init_app(app, host, port)

    def init_app(self, app, host=None, port=None):
        app.config.setdefault('RUKO_HOST', host or '127.0.0.1')
        app.config.setdefault('RUKO_PORT', port or 8080)
        app.teardown_appcontext(self._teardown)

    def _create_conn(self):
        app = current_app if has_request_context() else self._app
        return RukoClient(app.config['RUKO_HOST'], int(app.config['RUKO_PORT']))

    def _teardown(self, exception):
        self.context.close()
