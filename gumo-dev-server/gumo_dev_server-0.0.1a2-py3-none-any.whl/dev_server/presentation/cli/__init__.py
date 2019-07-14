import os
import sys
import subprocess
import logging
import threading
import time

import flask

from typing import Optional
from typing import Union


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

DEFAULT_ADMIN_PORT = '5001'


class RoutineWorkerStop(RuntimeError):
    pass


class RoutineWorker:
    def __init__(self, interval_seconds: int = 1):
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self.loop)
        self._interval_seconds = interval_seconds
        self._started = False

        self._worker_name = f'RoutineWorker({self.__class__.__name__})'

    def start(self, daemon: bool = False, interval_seconds: Optional[int] = None):
        if self._started:
            logger.debug(f'{self._worker_name} is already started.')
            return

        if interval_seconds:
            self._interval_seconds = interval_seconds

        self._stop_event.clear()
        self._thread.setDaemon(daemon)
        self._thread.start()
        logger.debug(f'{self._worker_name} is starting with interval = {self._interval_seconds}sec.')

    def stop(self, wait=True):
        self._stop_event.set()
        if wait:
            self._thread.join()

    def loop(self):
        try:
            while True:
                self.run()

                for i in range(self._interval_seconds):
                    time.sleep(1)
                    self.check_stop()
        except RoutineWorkerStop:
            logger.debug(f'{self._worker_name} is stopped by signals.')

    def check_stop(self):
        if self._stop_event.is_set():
            raise RoutineWorkerStop('Received stop event.')

    def run(self):
        raise NotImplementedError()


class NoopTask(RoutineWorker):
    def run(self):
        time.sleep(5)


class AdminWebServer(RoutineWorker):
    def run(self):
        _build_admin_server().run(
            host=os.environ['SERVER_HOST'],
            port=os.environ.get('ADMIN_PORT', DEFAULT_ADMIN_PORT)
        )


class TaskEmulatorWorker(RoutineWorker):
    def run(self):
        from gumo.task_emulator import BackgroundWorker

        BackgroundWorker.get_instance().start()


class AppServer(RoutineWorker):
    def run(self):
        app_yaml = sys.argv[1]

        entry_point = os.path.join(
            os.path.dirname(app_yaml),
            'main.py'
        )

        subprocess.run(
            args=['python', entry_point],
            stdout=sys.stdout,
            stderr=sys.stderr,
        )


class Worker:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        if cls._instance is not None:
            return cls._instance

        with cls._lock:
            if cls._instance is not None:
                return cls._instance

            cls._instance = cls()
            return cls._instance

    def __init__(self):
        self._noop_worker = NoopTask()
        self._app_server = AppServer()
        self._admin_web_server = AdminWebServer()
        self._task_emulator_worker = TaskEmulatorWorker()

        self._started = False

    def start(self):
        if self._started:
            logger.debug(f'{self} is already started.')
            return

        self._started = True
        self._noop_worker.start(daemon=False, interval_seconds=100)
        self._app_server.start(daemon=True, interval_seconds=3)
        self._admin_web_server.start(daemon=True, interval_seconds=3)
        self._task_emulator_worker.start(daemon=True, interval_seconds=3)

    def stop(self):
        if not self._started:
            return

        self._app_server.stop(wait=False)
        self._admin_web_server.stop(wait=False)
        self._task_emulator_worker.stop(wait=False)

        self._app_server.stop(wait=True)
        self._admin_web_server.stop(wait=True)
        self._task_emulator_worker.stop(wait=True)

        self._noop_worker.stop(wait=True)

        self._started = False


def _load_environment(app_yaml: str):
    from gumo.core.infrastructure import MockAppEngineEnvironment

    if not os.path.exists(app_yaml):
        print(f'File: {app_yaml} does not found.')
        exit(1)

    MockAppEngineEnvironment.load_app_yaml(app_yaml_path=app_yaml)


def _auto_fill_environ():
    if 'GOOGLE_CLOUD_PROJECT' not in os.environ:
        logger.warning(f'os.environ["GOOGLE_CLOUD_PROJECT"] does not configured.')
        logger.warning(f'os.environ["GOOGLE_CLOUD_PROJECT"] = "default" (by auto-fill)')
        os.environ['GOOGLE_CLOUD_PROJECT'] = 'default'

    if 'DATASTORE_EMULATOR_HOST' not in os.environ:
        raise RuntimeError(f'os.environ["DATASTORE_EMULATOR_HOST"] does not configured.')

    if os.environ.get('CLOUD_TASKS_EMULATOR_ENABLED') is None:
        logger.warning(f'os.environ["CLOUD_TASKS_EMULATOR_ENABLED"] does not configured.')
        logger.warning(f'os.environ["CLOUD_TASKS_EMULATOR_ENABLED"] = "true" (by auto-fill)')
        os.environ['CLOUD_TASKS_EMULATOR_ENABLED'] = 'true'

    if os.environ.get('SERVER_HOST') is None:
        logging.warning(f'os.environ["SERVER_HOST"] does not configured.')
        logging.warning(f'os.environ["SERVER_HOST"] = "0.0.0.0" (by auto-fill)')
        os.environ['SERVER_HOST'] = '0.0.0.0'

    if os.environ.get('SERVER_PORT') is None:
        logging.warning(f'os.environ["SERVER_PORT"] does not configured.')
        logging.warning(f'os.environ["SERVER_PORT"] = "5000" (by auto-fill)')
        os.environ['SERVER_PORT'] = '5000'


admin_blueprint = flask.Blueprint('gumo-dev-server', __name__, template_folder='template')


@admin_blueprint.route('/')
def root():
    return flask.render_template(
        'admin_dashboard.html'
    )


def _build_admin_server() -> flask.Flask:
    app = flask.Flask('admin_server')

    from gumo.task_emulator import task_emulator_flask_blueprints
    from datastore_viewer import DatastoreViewer

    for blueprint in task_emulator_flask_blueprints():
        app.register_blueprint(blueprint=blueprint)

    for blueprint in DatastoreViewer().flask_blueprints():
        app.register_blueprint(blueprint=blueprint)

    app.register_blueprint(blueprint=admin_blueprint)

    return app


def _configure_for_task_emulator(server_host: str, server_port: Union[str, int]):
    from gumo.core import configure as core_configure
    from gumo.datastore import configure as datastore_configure
    from gumo.task import configure as task_configure
    from gumo.task_emulator import configure as task_emulator_configure

    core_configure()
    datastore_configure()
    task_configure()
    task_emulator_configure(
        server_host=server_host,
        server_port=server_port,
    )


def gumo_dev_server():
    if len(sys.argv) == 1:
        print("Usage: gumo-dev-server <path-to-app.yaml>")
        exit(1)

    app_yaml = sys.argv[1]
    _load_environment(app_yaml=app_yaml)
    _auto_fill_environ()
    _configure_for_task_emulator(
        server_host=os.environ['SERVER_HOST'],
        server_port=os.environ.get('SERVER_PORT', DEFAULT_ADMIN_PORT)
    )

    Worker.get_instance().start()


if __name__ == '__main__':
    cli = os.path.dirname(__file__)
    presentation = os.path.dirname(cli)
    dev_server = os.path.dirname(presentation)
    gumo = os.path.dirname(dev_server)
    sys.path.insert(0, os.path.dirname(gumo))
    gumo_dev_server()
