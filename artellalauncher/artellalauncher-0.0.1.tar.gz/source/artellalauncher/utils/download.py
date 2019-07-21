#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains implementation to handle downloads in Artella Launcher
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import os
import urllib2

from tpQtLib.Qt.QtCore import *


def chunk_report(bytes_so_far, total_size, console, updater=None):
    """
    Function that updates progress bar with current chunk
    :param bytes_so_far: int
    :param total_size: int
    :param console: ArtellaConsole
    :param updater: ArtellaUpdater
    :return:
    """

    percent = float(bytes_so_far) / total_size
    percent = round(percent*100, 2)
    if updater:
        updater.progress_bar.setValue(percent)
        QCoreApplication.instance().processEvents()
    console.write("Downloaded %d of %d bytes (%0.2f%%)\r" % (bytes_so_far, total_size, percent))
    # if bytes_so_far >= total_size:
    #     console.write('\n')


def chunk_read(response, destination, console, chunk_size=8192, report_hook=None, updater=None):
    """
    Function that reads a chunk of a dowlnoad operation
    :param response: str
    :param destination: str
    :param console: ArtellaLauncher
    :param chunk_size: int
    :param report_hook: fn
    :param updater: ArtellaUpdater
    :return: int
    """

    with open(destination, 'ab') as dst_file:
        total_size = response.info().getheader('Content-Length').strip()
        total_size = int(total_size)
        bytes_so_far = 0
        while 1:
            chunk = response.read(chunk_size)
            dst_file.write(chunk)
            bytes_so_far += len(chunk)
            if not chunk:
                break
            if report_hook:
                report_hook(bytes_so_far=bytes_so_far, console=console, total_size=total_size, updater=updater)
    dst_file.close()
    return bytes_so_far


def download_file(filename, destination, console=None, updater=None):
    """
    Downloads given file into given target path
    :param filename: str
    :param destination: str
    :param console: ArtellaConsole
    :param updater: ArtellaUpdater
    :return: bool
    """

    console.write('Downloading file {0} to temporary folder -> {1}'.format(os.path.basename(filename), destination))
    try:
        dst_folder = os.path.dirname(destination)
        if not os.path.exists(dst_folder):
            console.write('Creating downloaded folders ...')
            os.makedirs(dst_folder)

        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
        req = urllib2.Request(filename, headers=hdr)
        data = urllib2.urlopen(req)
        chunk_read(response=data, destination=destination, console=console, report_hook=chunk_report, updater=updater)
    except Exception as e:
        raise e

    if os.path.exists(destination):
        console.write('Files downloaded succesfully!')
        return True
    else:
        console.write_error('Error when downloading files. Maybe server is down! Try it later')
        return False
