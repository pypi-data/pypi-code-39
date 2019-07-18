# -*- coding: utf-8 -*-
"""Import a protobuf graph (.pb) into Tensorboard and get its address to open in Chrome

Example usage:
python import_pb.py -g ./freeze/frozen_graph.pb  -l ./tb_logs(optional) -f(optional)
argument --log_dir(-l) is optional, if no specific address is required, log dir will be on the same level as graph address
argument --force(-f) is optional, if force, we create a pb file no matter there was one or not
if not force, if there was a pb file, we just open the old one.

note:if use .tflex entension file, please use company-customized tensorflow package
"""

"""Oneline docstring"""

import os
import socket
import random
import argparse
import tensorflow as tf

from tflex.utils import import_graph


def get_parser():
    parser = argparse.ArgumentParser(
        description='Visualization of deep learning models(.pb and .tflex file are supported).')
    parser.add_argument(
        '--graph', '-g',
        type=str,
        default='',
        required=True,
        help="Import protobuf graphDef file (.pb or .tflex) to tensorboard.")
    parser.add_argument(
        '--logdir', '-l',
        type=str,
        default=None,
        help="Log directory specified by user to save tensorboard logs.")

    return parser


def main():
    parser = get_parser()
    flags = parser.parse_args()
    ip = get_host_addr()
    log_dir_path = is_default_log_path(flags.graph, flags.logdir)
    create_file(flags.graph, log_dir_path)
    view_file_by_tensorboard(log_dir_path, ip)


def get_host_addr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception as e:  # If there is no internet connected
        ip = 'localhost'
    return ip


def create_file(file_path, log_path):
    """Creating tensorboard log file."""
    if os.listdir(log_path):
        filesToRemove = [os.path.join(log_path, f) for f in os.listdir(log_path)]
        for f in filesToRemove:
            os.remove(f)
    graph, _, _ = import_graph(file_path)
    tf.summary.FileWriter(log_path, graph)


def is_default_log_path(file_path, log_path):
    """if specific log path is entered, create log dir on there,
    else, create log dir on the same level of the graph file"""
    if log_path is None:
        parentPath = os.path.dirname(os.path.abspath(file_path))  # parent path of graph file
        log_dir_path = parentPath + "/logDir"
    else:
        log_dir_path = os.path.abspath(log_path)
    if not os.path.exists(log_dir_path):
        os.mkdir(log_dir_path)
    return log_dir_path


def view_file_by_tensorboard(log_path, ip_address):
    os.system(
        'tensorboard --logdir=' + log_path + " --host=" + ip_address + " --port=" + str(random.randint(6006, 9999)))


if __name__ == '__main__':
    main()
