import os
import subprocess
from subprocess import Popen


def run_cmd(cmd: list, default=None):
    p = Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ)
    out, err = p.communicate()
    if p.returncode:
        return default
    return out.decode("utf8").strip()
