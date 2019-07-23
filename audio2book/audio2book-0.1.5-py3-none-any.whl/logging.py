from pathlib import Path
from logbook import Logger, RotatingFileHandler


def log(path=None):
    loc = Path(path) if path else Path.home()
    RotatingFileHandler(str(loc / '.audio2book.log')).push_application()
    return Logger('Book')
