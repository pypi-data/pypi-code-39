#!/usr/bin/env python

"""deploy lambda then terraform"""

import argparse
from argparse import RawTextHelpFormatter as rawtxt
import sys
import signal
import json
import subprocess
import os
import stat
import pkg_resources

def signal_handler(sig, frame):
    """handle control c"""
    print('\nuser cancelled')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def query_yes_no(question, default="yes"):
    '''confirm or decline'''
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("\nPlease respond with 'yes' or 'no' (or 'y' or 'n').\n")

class Bcolors:
    """console colors"""
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    GREY = '\033[90m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ORANGE = '\033[38;5;208m'

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which
    return which(name) is not None

def get_script_path(script_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    script_path = os.path.join(dir_path, "scripts/%s" % script_name)
    return script_path

def main():
    '''deploy lambda then terraform.'''
    version = pkg_resources.require("spin-and-heave")[0].version
    parser = argparse.ArgumentParser(
        description='run build script to zip lambda package then run terraform apply',
        prog='spin-and-heave',
        formatter_class=rawtxt
    )

    #parser.print_help()
    parser.add_argument(
        "source",
        help="""the directory with your lambda code in it
$ spin-and-heave lambda
where `lambda` is the dir including the lambda code and requirements/modules""",
        nargs='?',
        default='none'
    ) 
    parser.add_argument('-r', '--runtime', help="optional. define a runtime", default="python3.6")
    parser.add_argument('-js', '--node', action='store_true', help='deploy node.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+version)
    args = parser.parse_args()
    node = args.node
    if node:
        runtime = "nodejs10.x"
    else:
        runtime = args.runtime
        if "nodejs" in runtime:
            node = True
    source = args.source
    if source == "none":
        print(Bcolors.WARNING+"please include a source directory"+Bcolors.ENDC)
        parser.print_help()
        exit()
    cwd = os.getcwd()
    swd = os.path.join(cwd, source)
    buildit = get_script_path("build.sh")
    os.system("{} {} {} {}".format(buildit, swd, runtime, cwd))

if __name__ == "__main__":
    main()
