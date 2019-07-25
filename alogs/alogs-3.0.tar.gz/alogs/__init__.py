#!/usr/bin/env python3

# stdlib
import logging
import logging.config

__name__ = 'alogs'
__version__ = '3.0'
__author__ = 'Marcellus Amadeus'
__email__ = 'marcellus@nexusedge.co'
__url__ = 'https://bitbucket.org/nexusedge/alogs'

logging_settings = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": ('%(levelname)s %(asctime)s '
                       '%(processName)s:%(process)d '
                       '%(module)s:%(funcName)s() '
                       '%(filename)s:%(lineno)d '
                       '[%(name)s] = %(message)s'),
            "datefmt": "%d/%b/%Y:%H:%M:%S %z"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
    },

    "loggers": {
        "module": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": "no"
        }
    },

    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}

logging_file_handler = {
    "info_file_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "level": "INFO",
        "formatter": "simple",
        "filename": "info.log",
        "maxBytes": 10485760,
        "backupCount": 10,
        "encoding": "utf8"
    }
}


def get_logger(module_name: str = None, log_file: str = None, disable_existing_loggers: bool = False) -> logging.Logger:
    """Create a Logger object with given module name.

    :param module_name: Logger name
    :param log_file: log file name
    :param disable_existing_loggers: whether to disable existing logs or not
    :return: Logger object
    """

    log_settings = logging_settings.copy()
    log_settings['disable_existing_loggers'] = disable_existing_loggers

    if log_file is not None:
        file_settings = logging_file_handler.copy()
        file_settings['info_file_handler']['filename'] = log_file

        log_settings["handlers"].update(logging_file_handler)
        log_settings["loggers"]["module"]["handlers"].append('info_file_handler')
        log_settings["root"]["handlers"].append('info_file_handler')

    logging.config.dictConfig(log_settings)

    logger = logging.getLogger(module_name or __name__)
    return logger

