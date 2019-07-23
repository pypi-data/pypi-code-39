#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import platform
import signal
import socket
import subprocess
import sys
import threading
import time

import logbook as logbook
import pkg_resources

from keychest_agent.core import Core
from keychest_agent.agent import Agent
from keychest_agent.config import KCConfig
from keychest_agent.log_dispatcher import LogDispatcher
from keychest_agent.logger import logger
from keychest_agent.version import Version

app = None


def parse_args():
    """
    Argument parsing & startup
    :return:
    """
    # Parse our argument list
    parser = argparse.ArgumentParser(description='KeyChest Agent, version %s' % Version.VERSION)

    # noinspection PyTypeChecker
    # parser.add_argument('--logging', dest='logging_level', default='notice', action='store_const', const=True,
    #                     help='possible logging levels are "debug", "info", "notice", "warning", "error", "critical"')

    parser.add_argument('--init', dest='init_config_only', default=False, action='store_const', const=True,
                        help="Creates a default configuration file if none found and stops")
    parser.add_argument('--register', dest='register_only', default=False, action="store_const", const=True,
                        help="Only register with KeyChest services and exit")
    parser.add_argument('--force', dest='force_register', default=False, action="store_const", const=True,
                        help="When used with --register, it will delete existing configuration file, no effect otherwise")
    parser.add_argument('--staging', dest='staging_env', default=False, action='store_const', const=True,
                        help="If set, the configuration file will be pointing to the KeyChest staging environment")
    parser.add_argument('--testing', dest='testing_env', default=False, action='store_const', const=True,
                        help="If set, the configuration file will be pointing to localhost for testing")
    parser.add_argument('--single', dest='not_force_run', default=False, action='store_const', const=True,
                        help="Default is to ignore existing PID file - this option will terminate if a PID file exists")
    parser.add_argument('--filelog', dest='do_file_logging', default=False, action='store_const', const=True,
                        help="Enables local logging to $HOME/.keychest/var/log")
    parser.add_argument('--locallog', dest='do_local_log', default=False, action='store_const', const=True,
                        help="Enables local logging to stdout")
    parser.add_argument('--run', dest='do_run_win', default=False, action='store_const', const=True,
                        help="Helper argument for Windows Service, no actual effect")

    return parser.parse_args()


# noinspection PyUnusedLocal
def signal_handler(sig, frame):
    global app

    Core.clear_pid()
    if app is not None:
        app.log_dispatcher_thread.stop()
    raise SystemExit('Terminating KeyChest agent')

def main():
    """
    Main keychest_agent starter
    :return:
    """
    global app

    if threading.current_thread() is threading.main_thread():
        signal.signal(signal.SIGINT, signal_handler)
    args = parse_args()

    if not args.not_force_run:
        Core.clear_pid()
    Core()  # init and create pid file

    if args.force_register and args.register_only:
        default_cfg = KCConfig.default_config()
        KCConfig.write_configuration(default_cfg)

    app = Agent(args)

    if args.register_only:
        KCConfig.config.do_register = True
    else:
        KCConfig.config.do_register = False
    app.old_stderr = sys.stderr
    KCConfig.config.do_local_log = args.do_local_log or args.do_file_logging
    if not KCConfig.config.do_local_log:
        f = open(os.devnull, 'w')
        sys.stderr = f

    if app.args.staging_env:
        default_cfg = KCConfig.default_config()
        KCConfig.config.logging_server \
            = default_cfg.logging_server.replace("keychest.net", "a3.keychest.net")
        if "a3.keychest.net" not in KCConfig.config.control_server:
            KCConfig.config.control_server \
                = default_cfg.control_server.replace("keychest.net", "a3.keychest.net")
        KCConfig.write_configuration(KCConfig.config)
    elif app.args.testing_env:
        default_cfg = KCConfig.default_config()
        KCConfig.config.logging_server \
            = default_cfg.logging_server.replace("https://keychest.net", "http://127.0.0.1")
        KCConfig.config.control_server \
            = default_cfg.control_server.replace("http://keychest.net", "http://127.0.0.1")
        KCConfig.write_configuration(KCConfig.config)

    # Init
    if app.args.init_config_only:
        Core.clear_pid()
        return

    # noinspection PyBroadException
    try:
        # subscriber = MultiProcessingSubscriber()
        # app.logging_queue = subscriber.queue
        logging_socket = False
        if hasattr(app.args, 'do_file_logging') and app.args.do_file_logging:
            file_output = True
        else:
            file_output = False

        if platform.system() in ['Windows', 'nt']:
            logging_socket = True
            local_ip = socket.gethostbyname("localhost")
            app.log_dispatcher_thread = LogDispatcher(app.logger_stop_event, ip=local_ip,
                                                      port=KCConfig.config.internal_socket, to_file=file_output)
        else:
            app.log_dispatcher_thread = LogDispatcher(app.logger_stop_event, to_file=file_output)

        app.log_dispatcher_thread.name = "Log dispatcher"
        app.log_dispatcher_thread.daemon = True
        app.log_dispatcher_thread.start()
        Agent.setup_logging(logbook.DEBUG, logging_socket)
        time.sleep(1)  # wait a bit for the logger to start listening on TCP
    except:
        Core.clear_pid()
        sys.exit(-1)

    # let's setup a config value for the current git version

    # counter = 0
    # while True:
    #     counter += 1
    #     time.sleep(1)
    #     logger.info("test", counter=counter)
    # noinspection PyBroadException

    resource_package = __name__
    data_filename = pkg_resources.resource_filename(resource_package, "version.py")
    # noinspection PyBroadException
    try:
        git_version_b = subprocess.check_output(['git', 'describe', '--always'], stderr=subprocess.DEVNULL)  # returns bytes
        git_version = git_version_b.decode().strip()
        KCConfig.config.git_version = git_version

        with open(data_filename, 'w') as git_file:
            git_file.write("\nclass Version(object):\n    VERSION = '" + git_version + "'\n")

    except Exception:  # if we can't run git, read version from a file (created during installation of the package
        # noinspection PyBroadException
        try:
            KCConfig.config.git_version = Version.VERSION
        except:
            KCConfig.config.git_version = "undetermined"

    logger.info("Logger configured for multiprocessing with stderr and filehandler")
    # app.logger = KCConfig.init_log()

    # filename = os.path.join(log_folder, 'server.log')
    # if filename:
    #     handlers.append(logbook.FileHandler(filename, mode='a', level=logbook.DEBUG, bubble=True))
    # target_handlers = logbook.NestedSetup(handlers)
    # sub = MultiProcessingSubscriber(app.logging_queue)
    # sub.dispatch_in_background(target_handlers)

    logger.info("KeyChest Agent starting", name=KCConfig.config.agent_name, query=str(app.args))
    if KCConfig.config.local_config:
        logger.info("The configuration is managed locally")
    else:
        logger.info("The configuration is managed from the KeyChest service")

    # the main processing loop
    terminate = False
    while not terminate:
        try:
            terminate = app.work_loop()
        except Exception as ex:
            logger.error("Agent main work_loop terminated", cause=str(ex))
            pass

    app.log_dispatcher_thread.stop()
    if KCConfig.config.do_register:
        sys.stderr = app.old_stderr
        if KCConfig.config.agent_email == "dummy@keychest.net":
            sys.stderr.write("\n\n\nRegistration failed:\n check the log messages above and if required, "
                             "send the logs to our support:\n\n  support@keychest.net\n\n")
        else:
            sys.stderr.write("\n\n\nThis agent ID is:\n %s\n\n\n" % KCConfig.config.agent_email)

    Core.clear_pid()


if __name__ == '__main__':
    main()
