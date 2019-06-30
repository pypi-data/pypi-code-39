#!/usr/bin/python
#coding:utf-8
#
# PROGRAM/MODULE: Firebird Upkeep utility
# FILE:           /fbupkeep/runner.py
# DESCRIPTION:    Script executor
# CREATED:        24.6.2019
#
# The contents of this file are subject to the MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Copyright (c) 2019 IBPhoenix (www.ibphoenix.com)
# All Rights Reserved.
#
# Contributor(s): Pavel Císař (original code)
#                 ______________________________________.

"""Firebird Upkeep utility

- Create gbak backup via service. Filename in specified format.
- Optional testing restore.
- Removal of backup files older than specified period (in days).
- Optional recompute of index statistics.
- Optional rebuild of user indices.
- Optional sweep (or automatic if OAT-OIT moves over specified threshold)
- Optional gathering of database statistics.
- Tasks for execution defined via configuration file.
- Use of logging
- Report about outcome of script execution sent via e-mail.
"""

import sys
import os
import argparse
import logging
import configparser
from logging.config import fileConfig
from fbupkeep.base import __version__, StopError, TaskExecutor

CONFIG_HEADER = """; ===========================
; FBUPKEEP configuration file
; ===========================
;
; A configuration file consists of sections, each led by a [section] header, followed by
; key/value entries separated by = or : string. Section names are case sensitive but keys
; are not. Leading and trailing whitespace is removed from keys and values. Values can be
; omitted, in which case the key/value delimiter may also be left out. Values can also
; span multiple lines, as long as they are indented deeper than the first line of the value.
;
; Configuration files may include comments, prefixed by # and ; characters. Comments may
; appear on their own on an otherwise empty line, possibly indented.
;
; Values can contain ${section:option} format strings which refer to other values.
; If the section: part is omitted, interpolation defaults to the current section (and possibly
; the default values from the special DEFAULT section). Interpolation can span multiple levels.
;
; FBUPKEEP uses named jobs. Each job must have it's own [upkeep_<jobname>] section with
; configuration for task executor and used tasks.
;
; Individual tasks may use additional sections with their own conventions.
;
; Logging is configured in separate sections at the end of this file.
; For details see https://docs.python.org/3/howto/logging.html#configuring-logging and
; https://docs.python.org/3/library/logging.config.html#logging-config-fileformat
;

[DEFAULT]

; ==========================
; Section for default values
; ==========================
;
; On execution FBUPKEEP automatically adds next options to the default section:
; job_name = [job_name option value]
; here = [current working directory]
; host = [--host option value, default: localhost]
; user = [--user option value, default: 'ISC_USER' or 'sysdba']
; password = [--password option value, default: 'ISC_PASSWORD' or 'masterkey']
; output_dir = [--output-dir option value, default: ${here}/${job_name}]
; filename = ${job_name}-%Y%m%d
;
; You can freely use these options for interpolation in your configuration.
;
; If you define any from these options in default section, its value would be ignored
; (replaced by command-line option value).

"""

CONFIG_FOOTER = """
; =====================
; Logging configuration
; =====================
;
; For details see https://docs.python.org/3/howto/logging.html#configuring-logging and
; https://docs.python.org/3/library/logging.config.html#logging-config-fileformat

[loggers]
keys=root

[handlers]
keys=root_handler

[formatters]
keys=root_formatter

[logger_root]
level=NOTSET
handlers=root_handler

[handler_root_handler]
; This sends logging output to file in current working directory
class=FileHandler
args=('fbupkeep.log', 'a')
;
; This sends logging output to STDERR
;class=StreamHandler
;args=(sys.stderr,)
;
formatter=root_formatter

[formatter_root_formatter]
format=%(asctime)s %(levelname)s: %(message)s
"""

class UpperAction(argparse.Action):
    "Action for ArgumentParser that converts argument to upper case."
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.upper())

def main():
    "Main function for `fbupkeep` script."
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="Tool for Firebird database backup and maintenance.")
    #
    parser.add_argument('--version', action='version', version='%(prog)s '+__version__)
    parser.add_argument('--create-config', type=argparse.FileType('w'), metavar='FILENAME',
                        help="Create configuration file for job and exit")
    #
    group = parser.add_argument_group("positional arguments")
    group.add_argument('job_name', type=str,
                       help="Job name")
    #
    group = parser.add_argument_group("Firebird server/database connection arguments")
    group.add_argument('--host', help="Server host")
    group.add_argument('-u', '--user', help="User name")
    group.add_argument('-p', '--password', help="User password")
    #
    group = parser.add_argument_group("run arguments")
    group.add_argument('-c', '--config', type=str, help="Configuration file")
    group.add_argument('-o', '--output-dir', metavar='DIR',
                       help="Force directory for log files and other output")
    group.add_argument('--dry-run', action='store_true',
                       help="Prepare execution but do not run tasks")
    #
    group = parser.add_argument_group("output arguments")
    group.add_argument('-v', '--verbose', action='store_true', help="Verbose output")
    group.add_argument('-q', '--quiet', action='store_true', help="No screen output")
    group.add_argument('-l', '--log-level', action=UpperAction,
                       choices=[x.lower() for x in logging._nameToLevel
                                if isinstance(x, str)],
                       help="Logging level")
    group.add_argument('--log-only', action='store_true',
                       help="Suppress all screen output including error messages")
    #
    parser.set_defaults(host='localhost',
                        user=os.environ.get('ISC_USER', 'sysdba'),
                        password=os.environ.get('ISC_PASSWORD', 'masterkey'),
                        log_level='WARNING',
                        config='fbupkeep.cfg',
                        create_config=None,
                        output_dir='${here}/${job_name}')
    #
    args = parser.parse_args()
    #
    defaults = dict(((key, value) for key, value in vars(args).items()
                     if key in ['host', 'user', 'password', 'output_dir']))
    defaults['here'] = os.getcwd()
    defaults['job_name'] = args.job_name
    defaults['filename'] = '${job_name}-%Y%m%d'
    conf = configparser.SafeConfigParser(defaults,
                                         interpolation=configparser.ExtendedInterpolation())
    check_config = False
    if not args.config:
        config_filename = os.path.join(os.getcwd(), 'fbupkeep.cfg')
    else:
        config_filename = args.config
        check_config = True
    conf.read(config_filename)
    #section = 'upkeep_%s' % args.job_name
    #if not conf.has_section(section):
        #parser.error("Configuration file does not have [%s] section." % section)
    #
    if conf.has_section('loggers'):
        fileConfig(config_filename)
    else:
        logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s")
    #
    logging.getLogger().setLevel(args.log_level)
    logging.logThreads = 0
    logging.logMultiprocessing = 0
    logging.logProcesses = 0
    #
    if check_config and not os.path.exists(args.config):
        logging.warning("Config file %s not found.", config_filename)
    try:
        executor = TaskExecutor()
        executor.load_tasks()
        if args.create_config is None:
            executor.run(conf, args)
        else:
            try:
                args.create_config.write(CONFIG_HEADER)
                args.create_config.write("[upkeep_%s]\n\n" % args.job_name)
                section_header = "Configuration for '%s' job" % args.job_name
                args.create_config.write("; %s\n" % ('=' * len(section_header)))
                args.create_config.write("; %s\n" % section_header)
                args.create_config.write("; %s\n\n" % ('=' * len(section_header)))
                executor.write_default_config(args.create_config)
                args.create_config.write(CONFIG_FOOTER)
            finally:
                args.create_config.close()
    except StopError as exc:
        logging.error(str(exc))
        print(str(exc), file=sys.stderr)
        logging.shutdown()
        sys.exit(1)
    except Exception as exc:
        logging.exception('Unexpected error: %s', exc)
        print('Unexpected error: %s' % exc, file=sys.stderr)
        logging.shutdown()
        sys.exit(1)
    #
    logging.shutdown()

if __name__ == '__main__':
    main()
