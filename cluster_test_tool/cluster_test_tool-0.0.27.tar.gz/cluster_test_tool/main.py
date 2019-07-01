from __future__ import print_function
import os
import sys
import re
import argparse
import functools
import getpass
import time
import threading
import logging
from argparse import RawTextHelpFormatter
from datetime import datetime

from . import check
from . import config
from . import pam
from . import utils


class Context(object):
    def __setattr__(self, name, value):
        super(Context, self).__setattr__(name, value)


def login(func):
    @functools.wraps(func)
    def login_func(*args, **kwargs):
        if config.LOGIN:
            print("###############")
        else:
            username = config.LOGIN_USER if config.LOGIN_USER else input("User name: ")
            if username == "" or username != "hacluster":
                utils.msg_error("User name is error!")
                sys.exit(1)
            password = config.LOGIN_PASSWORD if config.LOGIN_PASSWORD else getpass.getpass()

            pam_instance = pam.pam()
            pam_instance.authenticate(username, password)
            if pam_instance.code != 0:
                utils.msg_error(pam_instance.reason)
                sys.exit(pam_instance.code)
            print("###############")
            config.LOGIN = True

        func(*args, **kwargs)

    return login_func


def kill_testcase(context):
    '''
    --kill-sbd:           restarted or fenced
    --kill-sbd -l         fenced
    --kill-corosync       restarted or fenced
    --kill-corosync -l    fenced
    --kill-pacemakerd     restarted
    --kill-pacemakerd -l  blocked by bsc#1111692
    '''
    def check_restarted(context, task):
        count = 0
        while count < 10:
            rc, pid = utils.get_process_status(context.current_kill)
            if rc:
                task.info("Process {}({}) is restarted!".format(context.current_kill, pid))
                return
            time.sleep(0.5)
            count += 1
        task.error("Process {} is not restarted!".format(context.current_kill))

    def kill(context, task):
        if "Fenced" in context.expected and not utils.fence_enabled():
            task.error("stonith is not enabled!")
            sys.exit(1)

        while True:
            if not is_process_running(context, task):
                continue

            task.info("Trying to run \"{}\"".format(context.cmd))
            utils.run_cmd(context.cmd)

            if not context.loop:
                break
            # endless loop will lead to fence

        thread_check = threading.Thread(target=utils.anyone_kill, args=(utils.me(), task))
        thread_check.start()
        check_restarted(context, task)


    expected = {
        'sbd':        ('''a) sbd process restarted
                   b) Or, this node fenced.''', 'This node fenced'),
        'corosync':   ('''a) corosync process restarted
                   b) Or, this node fenced.''', 'This node fenced'),
        'pacemakerd': ('pacemakerd process restarted', None),
    }

    note = '''\nNOTE: The final report will explain the cluster behavior according to each test case.
      Some behavior might be not so obvious, and could be a bit complex indeed.'''

    for case in ('sbd', 'corosync', 'pacemakerd'):
        if getattr(context, case):
            if case == 'pacemakerd' and context.loop:
                return #blocked by bsc#1111692

            context.current_kill = case
            context.expected = expected[case][1] if context.loop else expected[case][0]
            context.cmd = r'killall -9 {}'.format(case)
            context.note = note

            task = utils.TaskKill("Force kill {}".format(context.current_kill),
                                  name=context.current_kill,
                                  expected=context.expected,
                                  looping=context.loop)

            if not check.check_cluster_service(quiet=True):
                task.error("cluster not running!")
                return
            if not is_process_running(context, task):
                return

            task.print_header()
            if not utils.ask("Run?"):
                task.info("Testcase cancelled")
                return
            task.enable_report()

            kill(context, task)


def split_brain(context):
    if not context.sp_iptables:
        return

    if not utils.which("iptables"):
        return

    if not check.check_cluster_service(quiet=True):
        utils.msg_error("cluster not running!")
        return

    fence_enabled, fence_action, fence_timeout = utils.get_fence_info()
    # check whether stonith is enabled
    if not fence_enabled:
        utils.msg_error("stonith is not enabled!")
        sys.exit(1)
    # get stonith action
    if not fence_action:
        sys.exit(1)

    if not fence_timeout:
        fence_timeout = config.FENCE_TIMEOUT
    task = utils.TaskSplitBrain("Block corosync ports",
                                fence_action=fence_action,
                                fence_timeout=fence_timeout)
    task.print_header()
    if not utils.ask("Run?"):
        task.info("Testcase cancelled")
        return

    ports = utils.corosync_port()
    if not ports:
        task.error("Can not get corosync's port")
        return
    task.info("Trying to temporarily block ports {}".format(ports))
    for p in ports:
        utils.run_cmd(config.BLOCK_PORT.format(p))
    task.info("Waiting {}s for self {}...".format(fence_timeout, fence_action))
    time.sleep(int(fence_timeout))
    task.error("Am I Still live?:(")
    sys.exit(1)


def fence_node(context):
    if not context.fence_node:
        return

    # check required commands exists
    required_commands = ['crm_node', 'stonith_admin', 'crm_attribute']
    for cmd in required_commands:
        if not utils.which(cmd):
            sys.exit(1)

    node = context.fence_node
    # check crm_node command
    if not utils.check_node_status(node, 'member'):
        utils.msg_error("Node \"{}\" not in cluster!".format(node))
        sys.exit(1)

    fence_enabled, fence_action, fence_timeout = utils.get_fence_info()
    # check whether stonith is enabled
    if not fence_enabled:
        utils.msg_error("stonith is not enabled!")
        sys.exit(1)
    # get stonith action
    if not fence_action:
        sys.exit(1)
    if not fence_timeout:
        fence_timeout = config.FENCE_TIMEOUT

    task = utils.TaskFence("Fence node {}".format(node),
                           fence_action=fence_action,
                           fence_timeout=fence_timeout)
    task.print_header()
    if not utils.ask("Run?"):
        task.info("Testcase cancelled")
        return

    task.info("Trying to fence node \"{}\"".format(node))

    thread_check = threading.Thread(target=utils.anyone_kill, args=(node, task, fence_timeout))
    utils.run_cmd(config.FENCE_NODE.format(node), wait=False)
    if node == utils.me():
        # fence self
        task.info("Waiting {}s for self {}...".format(fence_timeout, fence_action))
        thread_check.start()

        time.sleep(int(fence_timeout))
        task.error("Am I Still live?:(")
        sys.exit(1)
    else:
        # fence other node
        task.info("Waiting {}s for node \"{}\" {}...".format(fence_timeout, node, fence_action))
        thread_check.start()

        count = 0
        while count < int(fence_timeout):
            if utils.check_node_status(node, 'lost'):
                task.info("Node \"{}\" has been fenced successfully".format(node))
                return
            time.sleep(1)
            count += 1
        task.error("Node \"{}\" Still alive?:(".format(node))
        sys.exit(1)


def is_process_running(context, task):
    rc, pid = utils.get_process_status(context.current_kill)
    if not rc:
        return False
    task.info("Process {}({}) is running...".format(context.current_kill, pid))
    return True


class MyFormatter(RawTextHelpFormatter):
    def __init__(self,prog):
        super(MyFormatter,self).__init__(prog, max_help_position=50)


def parse_argument(context):
    parser = argparse.ArgumentParser(prog=context.name,
                                     description='Cluster Testing Tool Set',
                                     add_help=False,
                                     formatter_class=MyFormatter,
                                     epilog='''
Log: {}
Json results: {}
For each --kill-* testcase, report directory: {}'''.format(context.logfile,
                                                           context.jsonfile,
                                                           context.report_path))

    parser.add_argument('-e', '--env-check', dest='env_check', action='store_true',
                        help='Check environment')
    parser.add_argument('-c', '--cluster-check', dest='cluster_check', action='store_true',
                        help='Check cluster state')

    group_mutual = parser.add_mutually_exclusive_group()
    group_mutual.add_argument('--kill-sbd', dest='sbd', action='store_true',
                              help='Kill sbd daemon')
    group_mutual.add_argument('--kill-corosync', dest='corosync', action='store_true',
                              help='Kill corosync daemon')
    group_mutual.add_argument('--kill-pacemakerd', dest='pacemakerd', action='store_true',
                              help='Kill pacemakerd daemon')
    group_mutual.add_argument('--fence-node', dest='fence_node', metavar='NODE',
                              help='Fence specific node')
    group_mutual.add_argument('--split-brain-iptables', dest='sp_iptables', action='store_true',
                              help='Make split brain by blocking corosync ports')
    parser.add_argument('-l', '--kill-loop', dest='loop', action='store_true',
                        help='Kill process in loop')

    other_options = parser.add_argument_group('other options')
    other_options.add_argument('-d', '--debug', dest='debug', action='store_true',
                               help='Print verbose debugging information')
    other_options.add_argument('-y', '--yes', dest='yes', action='store_true',
                               help='Answer "yes" if asked to run the test')
    '''
    other_options.add_argument('-u', dest='user', metavar='USER',
                               help='User for login')
    other_options.add_argument('-p', dest='password', metavar='PASSWORD',
                               help='Password for login')
    '''
    other_options.add_argument('-h', '--help', dest='help', action='store_true',
                               help='show this help message and exit')

    args = parser.parse_args()
    if args.help:
        parser.print_help()
        sys.exit(0)
    for arg in vars(args):
        setattr(context, arg, getattr(args, arg))


def run(context):
    context.py2 = sys.version_info[0] == 2
    context.tasks = []
    var_dir = "/var/lib/{}".format(context.name)
    if not os.path.exists(var_dir):
        os.mkdir(var_dir)
    context.report_path = var_dir
    context.jsonfile = "{}/{}.json".format(var_dir, context.name)
    context.logfile = "/var/log/{}.log".format(context.name, context.name)
    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S',
                        filename=context.logfile,
                        level=logging.DEBUG)
    parse_argument(context)

    try:
        check.check(context)
        print()
        kill_testcase(context)
        fence_node(context)
        split_brain(context)

    except KeyboardInterrupt:
        utils.json_dumps()
        print("\nCtrl-C, leaving")
        sys.exit(1)


ctx = Context()
