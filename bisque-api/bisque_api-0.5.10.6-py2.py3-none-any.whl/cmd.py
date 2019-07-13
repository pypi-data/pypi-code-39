#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()

import os
import sys
import signal
import re
import fnmatch
import argparse
import logging
import random
import string
import urllib3
import configparser
import time


DEFAULT_CONFIG='~/bisque/config' if os.name == 'nt' else "~/.bisque/config"

def bisque_argument_parser(*args, **kw):
    parser = argparse.ArgumentParser(*args, **kw)
    parser.add_argument('-c', '--config', help='bisque config', default=DEFAULT_CONFIG)
    parser.add_argument('--profile', help="Profile to use in bisque config", default='default')
    parser.add_argument('-n', '--dry-run', action="store_true", help='report actions w/o changes', default=False)
    parser.add_argument('-d', '--debug', action="store_true", help='print debugging info', default=False)
    parser.add_argument('-q', '--quiet', action="store_true", help='print actions ', default=False)
    parser.add_argument('-a', '--credentials', help= "A bisque login.. admin ", default=None)
    parser.add_argument('--bisque-host', help = "Default bisque server to connect to ")
    # Local arguments
    return parser

def bisque_session(parser=None, argument_list=None):
    """Get a bisque session for command line tools using arguments and ~/.bisque/config files

    Usage:
    parser = bisque_argument_parser ("MyCommand")
    parser.add_argument ('newarg', help='any specific argument')
    args = parser.parse_args()
    session = bisque_session(args)

    ~/.bisque/config:
    [default]
    host=
    user=
    password=

    [testing]
    host=
    user=
    password=
    """
    user = None
    password = None
    root = None
    if parser is None:
        parser = bisque_argument_parser()
    args = parser.parse_args (args = argument_list)

    if args.bisque_host:
        root = args.bisque_host
    if args.credentials:
        user,password = args.credentials.split(':')
    elif os.path.exists (os.path.expanduser(args.config)):
        parser = configparser.ConfigParser ()
        parser.read (os.path.expanduser(args.config))
        if root is None:
            root = parser.get (args.profile, 'host')
        user = parser.get (args.profile, 'user')
        password = parser.get (args.profile, 'password')
    if not (root and user and password):
        config = configparser.RawConfigParser()
        print ("Please configure how to connect to bisque")
        root = input("BisQue URL e.g. https://data.viqi.org/: ")
        user = input("username: ")
        password = input("password: ")
        config_file = os.path.expanduser (args.config)
        os.makedirs(os.path.dirname(config_file))
        with open (config_file, 'wb') as conf:
            config.add_section (args.profile)
            config.set(args.profile, 'host', root)
            config.set(args.profile, 'user', user)
            config.set(args.profile, 'password', password)
            config.write (conf)
            print ("configuration has been saved to", args.config)

    if root and user and password:
        import urllib3
        from .comm import BQSession
        session =   BQSession()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        session.c.verify = False
        session = session.init_local(bisque_root=root,  user = user, pwd=password, create_mex=False)
        if not args.quiet:
            print  ("Session for  ", root, " for user ", user, " created")
        return session, args
    print ("Could not create bisque session with root={} user={} pass={}".format(root, user, password))
    return None
