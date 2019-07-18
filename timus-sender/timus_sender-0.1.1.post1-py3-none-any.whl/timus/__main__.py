#!/usr/bin/env python3

import argparse
import re
from pathlib import Path
import pkg_resources
from encodings import utf_8

import requests


BASE_URL = 'https://timus.online/'

LANGS = {
    'fpc': 31,
    'vc': 39,
    'vcpp': 40,
    'gcc': 45,
    'g++': 46,
    'clang': 47,
    'java': 32,
    'csharp': 41,
    'py2': 34,
    'py3': 48,
    'go': 14,
    'ruby': 18,
    'haskell': 19,
    'scala': 33,
    'rust': 55,
    'kotlin': 49,
}

DEFAULT_COMPILERS = {
    '.pas': 'fpc',
    '.c': 'gcc',
    '.cpp': 'g++',
    '.java': 'java',
    '.py': 'py3',
    '.cs': 'csharp',
    '.rb': 'ruby'
}

UTF_8 = utf_8.getregentry().name

def _load_version():
    version = pkg_resources.resource_string('timus', 'timus-sender.version')
    version = version.decode(UTF_8).strip()
    return version

parser = argparse.ArgumentParser(description='Submit solution to acm.timus.ru')
parser.add_argument('--judge-id', '-j', nargs='?', help='Judge ID')
parser.add_argument('--compiler', '-c', nargs='?', help='Langage/compiler')
parser.add_argument('--problem', '-p', nargs='?', help='Problem ID')
parser.add_argument('file', nargs=1, help='Source code file')
parser.add_argument('--version', action='version', version=_load_version())


def main():
    args = parser.parse_args()

    args.file = args.file[0]

    if not args.judge_id:
        judge_id_file = Path.home() / '.judge_id'
        if judge_id_file.exists():
            with open(judge_id_file) as f:
                args.judge_id = f.read().strip()
        else:
            print('Error: No .judge_id file in home directory')
            exit(1)

    if not args.problem:
        folder_name = Path(args.file).resolve().parent.name
        match = re.search(r'^(.+-)?(?P<number>\d+)(-.+)?$', folder_name)
        if match and match.group('number'):
            args.problem = match.group('number')
        else:
            print('Error: Cannot parse problem number from path')
            exit(1)

    if not args.compiler:
        ext = Path(args.file).suffix
        if ext in DEFAULT_COMPILERS:
            args.compiler = DEFAULT_COMPILERS[ext]
        else:
            print(f'Error: Cannot define compiler for extension {ext}')
            exit(1)


    data = {
        'Action': (None, 'submit'),
        'SpaceID': (None, '1'),
        'JudgeID': (None, args.judge_id),
        'Language': (None, LANGS[args.compiler]),
        'ProblemNum': (None, args.problem),
        'Source': (None, ''),
        'SourceFile': (
            args.file,
            open(args.file, 'rb'),
        )
    }

    r = requests.post(BASE_URL + 'submit.aspx?space=1', files=data)
    if r.status_code != 200:
        print(f'Warn: statuc sode is {r.status_code}')
        exit(1)
    else:
        num = args.problem
        author = args.judge_id[:-2]
        print(BASE_URL + f'status.aspx?space=1&num={num}&author={author}')
        exit(0)


if __name__ == '__main__':
    main()
