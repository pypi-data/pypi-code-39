#!/usr/bin/env python3

from fakeua.fakeua import update_useragent_db
from fakeua.fakeua import get_useragent_list
from fakeua.fakeua import get_random_ua

from fakeua.fakeua import DEFAULT_BROWSER
from fakeua.fakeua import DEFAULT_VERSION_FILTER
from fakeua.fakeua import DEFAULT_JSON_FP

from pathlib import Path

from argparse import ArgumentParser

import sys


def main():
    parser = ArgumentParser()
    # Argparse logic.
    parser.add_argument(
            "-u", "--update",
            help="Update useragent DB.",
            action="store_true",
            dest="update"
        )
    parser.add_argument(
            "-p", "--path",
            type=str,
            help="Json filepath where data_browsers dict is saved,"
            f"by default is {DEFAULT_JSON_FP}.",
            dest="path",
            default=DEFAULT_JSON_FP.as_posix()
        )
    parser.add_argument(
            "-b", "--browser",
            type=str,
            help="Specify a web browser",
            dest="browser",
            default=DEFAULT_BROWSER
        )
    parser.add_argument(
            "-f", "--filter",
            type=str,
            help="Specify a browser version filter",
            dest="filter",
            default=DEFAULT_VERSION_FILTER
        )
    parser.add_argument(
            "-r", "--list",
            help="Get UA list.",
            action="store_true",
            dest="list"
        )
    parser.add_argument(
            "-c", "--random",
            help="Choice a random element from UA list.",
            action="store_true",
            dest="random"
        )
    args = parser.parse_args()

    if args.update:
        if args.path:
            update_useragent_db(path=Path(args.path))
        else:
            update_useragent_db()
        print("Browsers database updated.")
        sys.exit(0)

    if args.list:
        filtered_ua_list = get_useragent_list(
            browser=args.browser,
            version_filter=args.filter,
            path=Path(args.path)
            )
        if args.random:
            random_ua = get_random_ua(
                browser=args.browser,
                version_filter=args.filter,
                path=Path(args.path)
                )
            print(random_ua)
        else:
            for ua in filtered_ua_list:
                print(ua)
