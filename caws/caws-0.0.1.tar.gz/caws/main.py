#!/usr/bin/env python

"""configure AWS responsibly using profile names."""

import argparse
from argparse import RawTextHelpFormatter as rawtxt
import sys
import signal
import os
from os.path import expanduser
import shutil
import json
import subprocess
from datetime import datetime
from pathlib import Path

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

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which
    return which(name) is not None

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
    PINK = '\033[35m'

def main():
    '''configure AWS responsibly using profile names and environment vars.'''
    parser = argparse.ArgumentParser(
        description="""configure AWS responsibly using profile names and environment vars.
`caws` will write to an rc file setting AWS_DEFAULT_PROFILE to the profile name.
if you do not have the rc file `caws` will create it for you.
"""+Bcolors.PINK+"""you'll need to add `source .cawsrc` to your .bashrc or .bash_profile"""+Bcolors.ENDC+"""
add new profiles using `$ aws configure --profile newname`""",
        prog='caws',
        formatter_class=rawtxt
    )

    #parser.print_help()
    parser.add_argument(
        "profile",
        help="""configure AWS responsibly using profile names.
example:
$ caws user1
where `user1` is the name of a profile in ~/.aws/credentials""",
        nargs='?',
        default='none'
    )
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.0.1')
    args = parser.parse_args()
    profile = args.profile
    if profile == "none":
        parser.print_help()
        exit()
    else:
        home = expanduser('~')        
        rcfile = os.path.join(home, ".cawsrc")
        if not os.path.isfile(rcfile):
            print(Bcolors.WARNING+"no rc file found, creating..."+Bcolors.ENDC)
            f = open(rcfile, "x")
            f.write("export AWS_DEFAULT_PROFILE=default")
            f.close()
            print(Bcolors.OKGREEN+"created: {}".format(rcfile)+Bcolors.ENDC)
        creds = os.path.join(home, ".aws", "credentials")
        awsconfig = os.path.join(home, ".aws", "config")
        if not os.path.isfile(creds) or not os.path.isfile(awsconfig):
            print(Bcolors.WARNING+"you must have aws cli installed and configured."+Bcolors.ENDC)
            exit()
        f = open(creds)
        line = f.readline()
        exists = False
        while line:
            if profile in line:
                exists = True
            line = f.readline()
        f.close()
        if not exists:
            print(Bcolors.WARNING+"no profile exists with the name {}".format(profile)+Bcolors.ENDC)
            exit()
        f = open(rcfile, "w")
        f.write("export AWS_DEFAULT_PROFILE={}".format(profile))
        f.close()
        os.system("source {}".format(rcfile))
        print(Bcolors.OKGREEN+"changed "+Bcolors.WARNING+"AWS_DEFAULT_PROFILE"+Bcolors.OKGREEN+" to "+Bcolors.PINK+"{}".format(profile)+Bcolors.ENDC)
        print("")
        print("   please run this command: "+Bcolors.WARNING+"source "+rcfile+Bcolors.ENDC)
        print("")
    exit()

if __name__ == "__main__":
    main()
