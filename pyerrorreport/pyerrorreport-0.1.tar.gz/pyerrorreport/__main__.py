from argparse import ArgumentParser
import json

from . import *

parser = ArgumentParser(description='Server-side of error_report library.')
parser.add_argument('--hostname', type=str, default="localhost",
                    help='hostname to open the port on')
parser.add_argument('--port', type=int, default=1234,
                    help='port number to open (default = 1234)')
parser.add_argument('-k','--keys', nargs='*',
                    help='Keys into the report dictionaries; corresponding '
                         'values will be used as directory names to organize '
                         'reports.')
parser.add_argument('-s', '--save_config', action="store_true",
                    help="Save options provided on command line to "
                         "~/.pyerrorreport/config.json, becoming the new "
                         "default.")

args = parser.parse_args()
configdict = args.__dict__.copy()

del configdict['save_config']

if args.save_config:
    from . import _default_config_path
    _default_config_path.parent.mkdir(parents = True, exist_ok = True)
    _default_config_path.write_text( json.dumps(configdict) )

print(f"Starting server on {configdict['hostname']}:{configdict['port']}")
start_server(**configdict)