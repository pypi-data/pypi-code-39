import logging
from inspect import getmembers

from okeydokey import notifier


class NotificationManager:
    backend_module = None
    backend_name: str = None
    _valid_backends = None

    def list_backends(self):
        if not self._valid_backends:
            _backends = {}
            for entity in getmembers(notifier):
                if not entity[0].startswith("_") and not entity[0].endswith("_") and not entity[0].endswith('notifier'):
                    _backends[entity[0]] = entity[1]
            self._valid_backends = _backends
        return self._valid_backends

    def select_backend(self, backend_name: str):
        if backend_name in self.list_backends():
            self.backend_name, self.backend_module = backend_name, getattr(
                self.list_backends()[backend_name],
                backend_name
            )
            self.backend_module = self.backend_module()
            del self._valid_backends
            return backend_name
        logging.critical(f'Selected backend "{backend_name}" is not available')
        return False

    def notify(self, message):
        try:
            self.backend_module.notify(message)
        except ValueError as e:
            logging.critical(f"Error using notification backend '{self.backend_name}': {e}")


class Notifier:
    _name = 'Notifier Basic'
    _destination = list()
    configuration = None
    configuration_validated = False

    def __init__(self):
        logging.info(f'Initiated Notifier: {self._name}')

    def configure(self, **kwargs):
        logging.info('Configuring Notifier')
        self.configuration = kwargs.get('configuration')

    def notify(self, message):
        logging.critical('No notification was sent. Use a Notifier backend for this instead of the main class.')

    def validate_configuration(self):
        raise NotImplementedError(
            'Wrong notifier backend selected or it has no validate_configuration method implemented'
        )
