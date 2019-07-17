import os
import json
import pathlib
from loguru import logger
from functools import wraps

from filelock import Timeout, FileLock

"""
name: Executor_Name
type: Executor_Type
status: running
submodule:
    - data driver:
        pid: 123123
        status: running
    - event driver:
        pid: 123123
        status: running
    - time drivier:
        pid: 123123
        status: running
    - healthcheck api:
        pid: 123123
        status: running

source type:
    - inner

registry:
    success: true
    topic: topic_id

topic_info:
    - topic_id-0:
        segments:
            - [0,99]
            - [102, 560]
        progress: 1-523
    - topic_id-3:
        segments:
            - [56,654]
            - [1542, 5623]
        progress: 0-543
"""


class RuntimeDump(object):
    """
    The class RuntimeDump is designed for sharing the status info between
    process, which enables user could run commands(`start`, `restart`...).

    Example:
        rd = RuntimeDump(data=temp)

        logger.info(rd.get("task_id"))

        rd.set("task_id", "asdasda")

        rd.set("branch_id", "12312312")

        rd.set("task_id", "22222222222222")

        logger.info(rd.get("task_id"))

        temp = {
            "task_id": "2",
            "branch_id": "1"
        }

        rd.reinitialize(temp)

        logger.info(rd.get("task_id"))

    :param data: the data for initializing when creating a new dump file, if not        specific, the value will be `{}`
    :param save_path: the file path of dump file and lock file, if not specific,
        the value will be `os.getcwd()`
    :param dump_name: the name of dump file

    """

    def __init__(self, data={}, save_path=os.getcwd(), dump_name="app.dump", mode=True):
        save_path = save_path[-1] if save_path[-1] == "/" else save_path
        self.dump_path = "%s/%s" % (save_path, dump_name)
        self.lock = FileLock("%s/.lock" % save_path, timeout=5)

        if (not pathlib.Path(self.dump_path).exists()) and mode:
            self.reinitialize(data)

    def reinitialize(self, data):
        """
        Reinitialize the dump file

        :param data:  the data for reinitializing when resetting
        """
        try:
            with self.lock.acquire(timeout=2):
                with open(self.dump_path, "w+") as f:
                    return f.write(json.dumps(data))
        except:
            return False

    def get(self, key=None, default_value=None, return_all=False):
        """
        Get the value by root key

        :param key: root key
        :param default_value: if fail to get the value, return
            the `default_value`, if not specific, the value will 
            be `None`
        :param return_all: return all data
        """
        try:
            with self.lock.acquire(timeout=2):
                with open(self.dump_path, "r") as f:
                    temp = f.read()
                    if (not temp):
                        raise AttributeError("empty file")
                    data = json.loads(temp)
                    if not key:
                        if return_all:
                            return data
                    return data[key]
        except:
            return default_value

    def set(self, key, value=None):
        """
        Set the value by root key

        :param key: root key
        :param value: if not specific, the value will 
            be `None`
        """
        try:
            with self.lock.acquire(timeout=2):
                with open(self.dump_path, "r+") as f:
                    temp = f.read()
                    if (temp):
                        data = json.loads(temp)
                    else:
                        data = dict()
                    f.seek(0)
                    f.truncate()
                    data[key] = value
                    return f.write(json.dumps(data))
        except:
            return False


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