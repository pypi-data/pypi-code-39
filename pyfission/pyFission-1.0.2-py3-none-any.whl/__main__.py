import sys
import uuid
from argparse import ArgumentParser

from pyfission.configs import custom_config as config
from pyfission.sync import pyfission_orch

import faulthandler

faulthandler.enable()


def dryrun(guid, config, args):
    print('Dry-Run Successful')


def main(argv=None):
    guid = str(uuid.uuid1()).replace('-', '')

    parser = ArgumentParser(description='PYFISSION - A tool to sync data across data sources')
    parser.add_argument('--src', help='Source DB', required=True)
    parser.add_argument('--dest', help='Destination DBs', required=True)
    subparser = parser.add_subparsers()

    """Dry-Run"""
    dryrun_main = subparser.add_parser('dryrun', help='Dry-Run For submodules of fission')
    dryrun_main.set_defaults(func=dryrun)

    """Database Sync"""
    pyfission_main = subparser.add_parser('sync', help='Sync Databases')
    pyfission_main.add_argument('--src_table', help='Overrides table definition from pyfission configs')
    pyfission_main.add_argument('--src_schema', help='Overrides schema definition from pyfission configs')
    pyfission_main.add_argument('--src_db', help='Overrides database definition from pyfission configs')
    pyfission_main.add_argument('--dest_table', help='Overrides table definition from pyfission configs')
    pyfission_main.add_argument('--dest_schema', help='Overrides schema definition from pyfission configs')
    pyfission_main.add_argument('--dest_db', help='Overrides database definition from pyfission configs')
    pyfission_main.add_argument('--method', help='Method of Replication', choices=['full', 'incremental'],
                             default='full')
    pyfission_main.add_argument('--out_format', help='Format of output files', choices=['csv', 'json'], default='json')
    pyfission_main.set_defaults(func=pyfission_orch)

    argv = argv or sys.argv
    args = parser.parse_args(argv[1:])

    args.func(guid, config, args)


if __name__ == '__main__':
    sys.exit(main())
