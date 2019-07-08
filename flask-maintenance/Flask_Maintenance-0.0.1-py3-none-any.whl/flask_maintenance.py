import os
from flask import _app_ctx_stack, abort, current_app

__all__ = ['Maintenance']


class Maintenance:
    """
    Add Maintenance mode feature to your flask application.
    """

    def __init__(self, app=None, location='env'):
        """
        :param app:
            Flask application object.
        """

        self.app = app

        if app is not None:
            self.init_app(app, location)

    def init_app(self, app, location='env'):
        """
        Initalizes the application with the extension.

        :param app:
            Flask application object.
        """

        if location not in ['env', 'ins']:
            raise ValueError('should be env or ins')

        app.config['MAINTENANCE_MODE_LOCATION'] = location

        app.before_request_funcs.setdefault(None, []).append(self._handler)

    def _handler(self):
        """
        Maintenance mode handler.
        """
        actx = _app_ctx_stack.top

        if actx:
            location = current_app.config['MAINTENANCE_MODE_LOCATION']

            if location == 'env':
                mode_enabled = os.getenv('ENABLE_MAINTENANCE_MODE', 'False')
            else:
                ins_path = os.path.join(current_app.instance_path,
                                        'maintenance')
                mode_enabled = str(os.path.isfile(ins_path))

            if mode_enabled == 'True':
                abort(503)
