import os


def env(key, default=None, cast_func=str, prefix=''):
    key = '%s%s' % (prefix, key)
    value = os.getenv(key)
    if value is None:
        print("[WARNING] EnvVar (%s) missing; Default: %s" % (key, default))
        return default
    return cast_func(value)


def cast_bool(value):
    if value == '1':
        return True
    return False
