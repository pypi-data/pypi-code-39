import os
from subprocess import check_output

from .. import print_log

def run_command(*args, **kwargs):
    if not len(args) and not len(kwargs):
        return False

    cur_dir = os.getcwd()
    if kwargs.get('directory', None):
        directory = kwargs['directory']
        try:
            os.chdir(directory)
        except OSError:
            print_log('Cannot chdir to {}'.format(directory))
            return False
    
    my_args = args
    if kwargs.get('command', None):
        my_args = kwargs['command']

    print(check_output(my_args).decode())
    os.chdir(cur_dir)