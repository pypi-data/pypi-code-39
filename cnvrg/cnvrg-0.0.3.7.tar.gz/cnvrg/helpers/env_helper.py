import os

EXPERIMENT = "Experiment"


POOL_SIZE = os.environ.get("CNVRG_THREAD_SIZE") or 100
CURRENT_JOB_ID = os.environ.get("CNVRG_JOB_ID")
CURRENT_JOB_TYPE = os.environ.get("CNVRG_JOB_TYPE")
MAX_LOGS_PER_SEND = int(os.environ.get("CNVRG_MAX_LOGS_PER_SEND") or 500)

def in_experiment():
    return CURRENT_JOB_TYPE == EXPERIMENT