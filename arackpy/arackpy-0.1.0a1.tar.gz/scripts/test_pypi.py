"""Publish to pypi.org using twine.

This script should be run from within the virtual environment.
"""

from __future__ import print_function

import subprocess
import shutil

import os

from arackpy import ROOT_DIR


def publish():
    """Publish to pypy.org"""

    cmds = ["python setup.py sdist bdist_wheel",
            "twine upload dist/*"]

    os.chdir(ROOT_DIR)

    if os.path.exists("dist"):
        shutil.rmtree("dist")

    try:
        for cmd in cmds:
            subprocess.call(cmd.split())
    except:
        print("Publish failed!")


if __name__ == "__main__":
    publish()
