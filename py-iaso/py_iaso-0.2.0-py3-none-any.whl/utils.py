import time

def print_log(*args):
    print(time.strftime('%d %b %Y | %H:%M:%S'), '|', *args)

def raise_missing_key(key):
    raise KeyError('Cannot find {} in config'.format(key))

def raise_invalid_key(key):
    raise KeyError('Invalid {} in config'.format(key))