import subprocess
import psutil
from cnvrg.helpers.logger_helper import log_message
import shlex
import sys
import re

ON_POSIX = 'posix' in sys.builtin_module_names


def __send_cmd(cmd):
    cmd = re.sub(r"(python3?)",r"\1 -u", cmd)
    if not isinstance(cmd, list):
        cmd = shlex.split(cmd)
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, close_fds=False, bufsize=1)

def run_sync(cmd, print_output=False):
    proc = __send_cmd(cmd)
    output = []
    for log in proc.stdout:
        log = log.decode("utf-8")
        output.append(log)
        if print_output:
            log_message(log)
    return output

def run_async(cmd):
    return __send_cmd(cmd)

def analyze_pid(proc):
    p = psutil.Process(proc.pid)
    with p.oneshot():
        return {"cpu": p.cpu_times(), "cpu_precent": p.cpu_percent(), "memory_info": p.memory_percent(), "threads": p.num_threads()}