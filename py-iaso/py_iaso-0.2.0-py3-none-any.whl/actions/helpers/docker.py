import os
from subprocess import check_output

from .. import print_log

def restart_docker_compose(directory=None):
    if directory:
        try:
            os.chdir(directory)
        except OSError:
            print_log('Cannot chdir to {}'.format(directory))
            return False

    check_output(['docker-compose', 'restart'])