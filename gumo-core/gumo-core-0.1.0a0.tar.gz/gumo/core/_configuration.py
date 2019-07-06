import threading

from logging import getLogger
from typing import Optional
from injector import singleton

from gumo.core.injector import injector
from gumo.core.infrastructure.configuration import GumoConfiguration

logger = getLogger('gumo.core')

_configure_funcs = []
_configure_funcs_lock = threading.Lock()


def register_configure_func(func):
    global _configure_funcs
    with _configure_funcs_lock:
        _configure_funcs.append(func)


def configure(
        google_cloud_project: Optional[str] = None,
        google_cloud_location: Optional[str] = None,
        service_account_credential_path: Optional[str] = None,
):
    if google_cloud_location is not None:
        logger.warning(f'The argument "google_cloud_location" of gumo.core.configure() is deprecated.')
    if service_account_credential_path is not None:
        logger.warning(f'The argument "service_account_credential_path" of gumo.core.configure() is deprecated.')

    config = GumoConfiguration(
        google_cloud_project=google_cloud_project,
    )
    logger.debug(f'Gumo is configured, config={config}')
    injector.binder.bind(GumoConfiguration, to=config, scope=singleton)

    with _configure_funcs_lock:
        logger.debug(f'Invoke configure funcs: {len(_configure_funcs)} functions.')
        for i, func in enumerate(_configure_funcs):
            logger.debug(f'Invoke configure func[{i}]: {func}')
            func()
        logger.debug(f'Invoke configure funcs: {len(_configure_funcs)} functions finished.')

    return config
