"""Run tests on the local pydoc server"""

from __future__ import print_function

import os
import signal
import subprocess
import unittest

import time

from arackpy.spider import Spider


PORT = 8080
SERVER = None


def setUpModule():
    global SERVER

    # initialize server
    cmd = "python -m pydoc -p %s" % PORT
    SERVER = subprocess.Popen(cmd.split())

    # wait for server to start
    time.sleep(1)


def tearDownModule():
    print("pydoc server at http://localhost:%s stopped" % PORT)
    SERVER.terminate()


class TestSpider(Spider):

    debug = False

    wait_time_range = (1, 2)

    start_urls = ["http://localhost:%s" % PORT]

    def stop_crawl(self):
        """Keyboard interrupt"""
        if hasattr(signal, 'CTRL_C_EVENT'):
            # windows. Need CTRL_C_EVENT to raise the signal in the
            # whole process group
            os.kill(os.getpid(), signal.CTRL_C_EVENT)
        else:
            # unix.
            pgid = os.getpgid(os.getpid())
            if pgid == 1:
                os.kill(os.getpid(), signal.SIGINT)
            else:
                os.killpg(os.getpgid(os.getpid()), signal.SIGINT)


class TestCaseSpider(unittest.TestCase):
    """Start the pydoc server for testing the crawler"""

    pass
