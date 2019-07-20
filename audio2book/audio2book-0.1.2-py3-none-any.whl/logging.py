import sys
from logbook import Logger, RotatingFileHandler


RotatingFileHandler('log').push_application()
log = Logger('Book')
