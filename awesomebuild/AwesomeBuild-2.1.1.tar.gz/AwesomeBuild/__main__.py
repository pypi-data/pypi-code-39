#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import argparse
import json
import os

from .importer import importrules
from .RulesTree import RulesTree
from .StatusFile import StatusFile


def main():
    parser = argparse.ArgumentParser(
        description='Awesome build manager to replace Makefiles. It allows very fast building!')
    parser.add_argument('--config', default='awesomebuild.json',
                        help='default: awesomebuild.json')
    parser.add_argument('--status', default='awesomestatus.json',
                        help='Relative to project folder, default: awesomestatus.json')
    parser.add_argument(
        'targets', nargs='*',
        help='defaults to the main rule defined in the config file'
    )
    args = parser.parse_args()

    configpath = os.path.abspath(
        (os.path.abspath(os.getcwd()) + '/'
         if args.config[0] != '/' else '') + args.config)

    if not os.path.isfile(configpath):
        raise FileNotFoundError('Config path invalid!')

    configdir = os.path.dirname(configpath)

    with open(configpath) as json_file:
        data = json.load(json_file)

    if 'rules' not in data:
        data['rules'] = {}

    data = importrules(data, configdir)

    targets = args.targets if len(args.targets) != 0 else [data['main']]

    statusfile = StatusFile(
        os.path.abspath(
            os.path.join(configdir, args.status)
        ),
        data
    )

    rules = RulesTree(data, configdir, statusfile)

    for t in targets:
        rules[t].run()

    statusfile.save()


if __name__ == '__main__':
    main()
