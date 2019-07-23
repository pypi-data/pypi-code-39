import datetime
import logging
import sys
import uuid

from pyfission.configs.config import dir_logs


def logger_config(guid=None, prefix='generic'):
    guid = str(uuid.uuid1()).replace('-', '') if not guid else guid
    logger = logging.getLogger(f'{guid}')
    logger.setLevel(logging.INFO)

    # # # define handlers # # #
    formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(pathname)s:%(lineno)d\n\t%(message)s\n',
                                  "%Y-%m-%d %H:%M:%S %Z")

    # File Handlers
    handler = logging.FileHandler(f'{dir_logs}/{prefix}__{guid}')
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)

    # Stream Handlers (i.e. console)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(handler)
    logger.addHandler(stream_handler)

    return logger


def func_logger(ignore_args=None, ignore_kwargs=None):
    """
    To be used as decorator for functions
    :param ignore_args: a list of position based args which needs to be ignored during logging
    :param ignore_kwargs: a list of keyword based args which needs to be ignored during logging
    :return: elapsed_time, inner function's return values
    """

    def func_logger_wrapper(func):
        def _func_logger_wrapper(*args, **kwargs):
            fname = func.__name__
            args2log = args
            kwargs2log = kwargs

            try:
                if 'guid' not in kwargs2log.keys():
                    guid = args2log[0].handlers[0].baseFilename.split('/')[-1]
                    log = logging.getLogger(guid)
                else:
                    log = logging.getLogger(kwargs2log['guid'])
            except:
                log = logging.getLogger(fname)

            if ignore_args is not None:
                args2log = [arg if index not in ignore_args else "*** HIDDEN ***"
                            for index, arg in enumerate(args2log)
                            ]

            if ignore_kwargs is not None:
                kwargs2log = {key: value if key not in ignore_kwargs else "*** HIDDEN ***"
                              for key, value in list(kwargs2log.items())
                              }

            log.info('Starting func:{}(args={}, kwargs{})'.format(fname,
                                                                  args2log,
                                                                  kwargs2log))

            start_time = datetime.datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.datetime.now()

            elapsed_time = end_time - start_time
            log.info(f'Function `{fname}` completed in {elapsed_time}')

            return elapsed_time, result

        return _func_logger_wrapper

    return func_logger_wrapper


def main():
    print('Testing logger_config')
    logger_config()


if __name__ == '__main__':
    sys.exit(main())
