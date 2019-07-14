import os
import signal


def _handle(sig, frame):
    print(end='\033[K\r', flush=True)
    os._exit(128 + signal.SIGINT)


signal.signal(signal.SIGINT, _handle)
