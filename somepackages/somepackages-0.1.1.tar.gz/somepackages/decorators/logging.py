import logging
import traceback


def exception(safe=False, default=None):
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
            except:
                if not safe:
                    logging.error(traceback.format_exc(limit=-1))
                    exit(1)
                    return
                else:
                    logging.warning(traceback.format_exc(limit=-1))
                    result = default
            return result

        return wrapper

    return decorator



