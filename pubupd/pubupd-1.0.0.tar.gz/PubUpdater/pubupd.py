#!/usr/bin/env python3

#import yaml
from packaging import version
import json
import requests
from colorama import Fore, Back, Style
import ruamel.yaml
import sys
import argparse
import os


def main():
    def is_dir(dirname):
        """Checks if a path is an actual directory"""
        fname = os.path.abspath(dirname) + '/pubspec.yaml'
        if not os.path.isdir(dirname):
            msg = "{0} is not a directory".format(dirname)
            raise argparse.ArgumentTypeError(msg)
        elif not os.path.isfile(fname):
            msg = "{0} does not contain pubspec.yaml".format(dirname)
            raise argparse.ArgumentTypeError(msg)
        else:
            return dirname

    def get_args():
        """Get CLI arguments and options"""
        parser = argparse.ArgumentParser(description="""do something""")

        parser.add_argument('dir', help="The folder of alignments", nargs=1,
                            type=is_dir)
        return parser

    def get_latest_version(package):

        api_url = 'https://pub.dev/api/packages/' + package
        response = requests.get(api_url)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))['latest']['version']
        else:
            return None

    parser = get_args()
    project = os.path.abspath(parser.parse_args().dir[0])
    fname = project + '/pubspec.yaml'
    stream = open(fname, 'r')
    yaml = ruamel.yaml.YAML()  # defaults to round-trip if no parameters given
    data = yaml.load(stream)
    dep = data['dependencies']
    for package in dep:
        if type(dep[package]) is dict:
            continue
        if type(dep[package]) is not str:
            continue
        cv = version.parse(dep[package].replace('^', ''))
        lv = version.parse(get_latest_version(package))
        outdated = lv > cv
        if outdated:
            data['dependencies'][package] = '^' + str(lv)
            print(
                f'{Fore.BLUE}[{package}]{Style.RESET_ALL} {Fore.RED}{str(cv)}{Style.RESET_ALL} -> {Fore.GREEN}{str(lv)}{Style.RESET_ALL} (Update available)')
        else:
            print(
                f'{Fore.BLUE}[{package}]{Style.RESET_ALL} {Fore.GREEN}{str(cv)}{Style.RESET_ALL} (latest)')
    new_file = open(project + "/pubspec_new.yaml", 'w')
    yaml.dump(data, new_file)
