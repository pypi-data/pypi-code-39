"""An useless example of script, that just waits and nothing else."""

import time
NAME = "Waiter"

def run_on(context, *, waittime:float=1.):
    time.sleep(waittime)
