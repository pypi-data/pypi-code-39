import logging

logger = logging.getLogger('logger')
logger.propagate = False
logger.setLevel('INFO')
logger.addHandler(logging.StreamHandler())  # Logs go to stderr
logger.handlers[-1].setFormatter(logging.Formatter('%(message)s'))
logger.handlers[-1].setLevel('INFO')


# TODO test it
def get_logger(name):
    child_logger = logger.manager.getLogger(name)
    child_logger.setLevel('INFO')
    return child_logger

