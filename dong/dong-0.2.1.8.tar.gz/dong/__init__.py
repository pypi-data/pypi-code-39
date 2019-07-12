import os

#__version__ = "0.1"

PROG_NAME = "dong"

try:
    env = os.environ['DONG_DEBUG']
except KeyError:
    SERVER_IP = 'https://dongcloud.libgirl.com'
else:
    if env == 't':
        SERVER_IP = 'http://127.0.0.1:8000'
    else:
        SERVER_IP = env

SERVER_NAME = 'api.libgirl.com'
