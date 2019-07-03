import argparse
import platform
import signal
import socket
import subprocess
import sys
import time

import logbook as logbook
import pkg_resources

from keychest_agent.core import Core
from keychest_agent.agent import Agent
from keychest_agent.config import KCConfig
from keychest_agent.log_dispatcher import LogDispatcher
from keychest_agent.logger import logger

app = None


def parse_args():
    """
    Argument parsing & startup
    :return:
    """
    # Parse our argument list
    parser = argparse.ArgumentParser(description='KeyChest Agent')

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

    signal.signal(signal.SIGINT, signal_handler)
    args = parse_args()

    if not args.not_force_run:
        Core.clear_pid()
    Core()  # init and create pid file

    if args.force_register and args.register_only:
        default_cfg = KCConfig.default_config()
        KCConfig.write_configuration(default_cfg)

    app = Agent(args)

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
        if platform.system() in ['Windows', 'nt']:
            logging_socket = True
            local_ip = socket.gethostbyname("localhost")
            app.log_dispatcher_thread = LogDispatcher(app.logger_stop_event, ip=local_ip,
                                                      port=KCConfig.config.internal_socket)
        else:
            app.log_dispatcher_thread = LogDispatcher(app.logger_stop_event)

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
    resource_path = 'data/git_version'
    data_dir = pkg_resources.resource_filename(resource_package, 'data')
    data_filename = pkg_resources.resource_filename(resource_package, resource_path)
    # noinspection PyBroadException
    try:
        import os
        git_version_b = subprocess.check_output(['git', 'describe', '--always'], stderr=subprocess.DEVNULL)  # returns bytes
        git_version = git_version_b.decode().strip()
        KCConfig.config.git_version = git_version

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        with open(data_filename, 'w') as git_file:
            git_file.write(git_version)
    except Exception as ex:  # if we can't run git, read version from a file (created during installation of the package
        KCConfig.config.git_version = pkg_resources.resource_string(resource_package, resource_path)

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
    if KCConfig.config.agent_email == "dummy@keychest.net":
        sys.stdout.write("\n\n\nRegistration failed:\n check the log messages above and if required, "
                         "send the logs to our support:\n\n  support@keychest.net\n\n")
    else:
        sys.stdout.write("\n\n\nThis agent ID is:\n %s\n\n\n" % KCConfig.config.agent_email)
    Core.clear_pid()


if __name__ == '__main__':
    main()
