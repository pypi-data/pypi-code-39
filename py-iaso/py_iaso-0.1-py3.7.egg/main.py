from .monitor import Monitor
import sys
import os

sys.path.insert(0, os.getcwd())

def run():
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = None

    try:
        monitor = Monitor(config_file)
    except Exception as e:
        print(e)
        sys.exit(-1)

    try:
        monitor.run()
    except KeyboardInterrupt:
        print('Good bye!')