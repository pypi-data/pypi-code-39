import os
import json
import pathlib
from loguru import logger
from functools import wraps

def write_runtime(runtime):
    try:
        lock = FileLock("%s/.lock" % os.getcwd(), timeout=5)
        with lock.acquire(timeout=2):
            with open("app.dump", "w") as f:
                return f.write(json.dumps(runtime))
    except:
        return False

def load_runtime():
    try:
        lock = FileLock("%s/.lock" % os.getcwd(), timeout=5)
        with lock.acquire(timeout=2):
            with open("app.dump", "r") as f:
                return json.loads(f.read())
    except:
        return False
