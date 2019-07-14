#!/usr/bin/env python
"""strip comments and blank lines from env file"""
# -*- coding: utf-8 -*-
import json
import sys
import click
import env2json

MODULE_NAME = "env_strip"
PROG_NAME = 'python -m %s' % MODULE_NAME
USAGE = 'python -m %s path' % MODULE_NAME


@click.command()
@click.argument('path', required=True)
def _cli(path):
    data = {}
    lines = open(path).read().splitlines()
    for line_no,line in enumerate(lines,0):
        try:
            data.update(env2json.parse(line))
        except ValueError:
            raise ValueError(".env:%s\n%s" % (line_no,line))
    if data:
        for k,v in data.items():
            print("%s=%s" % (k,v))

if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
