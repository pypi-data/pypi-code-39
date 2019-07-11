import csv
import os
import pathlib
import typing

PACKAGE_DIR=os.path.abspath(os.path.dirname(__file__))

with pathlib.Path(PACKAGE_DIR, 'pokerware-formal.txt').open(newline='') as f:
    reader = csv.reader(f, delimiter='\t')
    FORMAL_LOOKUP = {code: word for code, word in reader}

with pathlib.Path(PACKAGE_DIR, 'pokerware-slang.txt').open(newline='') as f:
    reader = csv.reader(f, delimiter='\t')
    SLANG_LOOKUP = {code: word for code, word in reader}

def formal(codes: typing.List[str]) -> typing.List[str]:
    return [FORMAL_LOOKUP[code] for code in codes]

def slang(codes: typing.List[str]) -> typing.List[str]:
    return [SLANG_LOOKUP[code] for code in codes]

def custom(codes: typing.List[str], path: str) -> typing.List[str]:
    with open(path, 'r', newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        lookup = {code: word for code, word in reader}

    return [lookup[code] for code in codes]
