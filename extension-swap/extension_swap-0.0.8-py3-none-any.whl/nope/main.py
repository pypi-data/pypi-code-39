#!/usr/bin/env python

"""change file extension to nope"""

import argparse
from argparse import RawTextHelpFormatter as rawtxt
import sys
import signal
import os
import json
import subprocess
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
    PINK = '\033[38;5;212m'
    PALEYELLOW = '\033[38;5;228m'
    PALEBLUE = '\033[38;5;111m'

def main():
    '''change file extension to nope.'''

    version = pkg_resources.require("extension-swap")[0].version

    parser = argparse.ArgumentParser(
        description='change file extension to nope.',
        prog='nope',
        formatter_class=rawtxt
    )

    #parser.print_help()
    parser.add_argument(
        "file",
        help="""change file extension to nope.
"""+Bcolors.PALEYELLOW+"""$ nope file.tf"""+Bcolors.ENDC+"""
where file.tf is the file you wanna change.
for multiple files use the `-m` flag
"""+Bcolors.PALEYELLOW+"""$ nope -m file.tf another_file.tf"""+Bcolors.ENDC,
        nargs='?',
        default='none'
    )
    parser.add_argument('-x', '--extension', help="optional. use custom extension", default="tf")
    parser.add_argument('-m', '--multiple', nargs='+', help="""nope multiple files.
example: """+Bcolors.PALEBLUE+"""$ nope -m file1.tf file2.tf file3.tf"""+Bcolors.ENDC, type=str)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+version)
    args = parser.parse_args()
    the_file = args.file
    extension = args.extension
    multiple = args.multiple
    if the_file == "none":
        if not multiple:
            print()
            print(Bcolors.WARNING+"please provide a filename"+Bcolors.ENDC)
            print()
            parser.print_help()
            exit()
        else:
            the_file = multiple
    else:
        the_file = [the_file]

    for f in the_file:
        if os.path.exists(f):
            file_arr = f.split('.')
            if len(file_arr) < 2:
                print(Bcolors.ORANGE+f+Bcolors.WARNING+" does not have an extension"+Bcolors.ENDC)
            else:
                file_without_ext = ('.').join(file_arr[:-1])
                if file_arr[-1] == "nope":
                    new_name = file_without_ext+"."+extension
                else:
                    if extension != "tf":
                        new_name = file_without_ext+"."+extension
                    else:
                        new_name = file_without_ext+".nope"
                os.rename(f, new_name)
                print(Bcolors.ENDC+"noped: "+Bcolors.OKGREEN+new_name+Bcolors.ENDC)
        else: 
            print(Bcolors.WARNING+"file does not exist "+Bcolors.ORANGE+f+Bcolors.ENDC)

if __name__ == "__main__":
    main()
