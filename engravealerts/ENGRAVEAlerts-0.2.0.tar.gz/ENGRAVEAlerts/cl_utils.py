#!/usr/local/bin/python
# encoding: utf-8
"""
Documentation for ENGRAVEAlerts can be found here: http://ENGRAVEAlerts.readthedocs.org/en/stable

Usage:
    ealert init
    ealert sms <mobilenumbers> <message> [-s <pathToSettingsFile>]
    ealert call <mobilenumbers> <message> [-s <pathToSettingsFile>]
    ealert listen [-t] [-s <pathToSettingsFile>]

Options:
    init                  setup the ENGRAVEAlerts settings file for the first time
    sms                   send sms
    listen                listen for and alert on new events

    <mobilenumbers>       quoted mobile numbers space or comma separated
    <message>             quoted message (160 limit)

    -t, --test            run in test mode
    -h, --help            show this help message
    -v, --version         show version
    -s, --settings        the settings file
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
import readline
import glob
import pickle
from docopt import docopt
from fundamentals import tools, times
from subprocess import Popen, PIPE, STDOUT
# from ..__init__ import *
from ENGRAVEAlerts.sms import sms as esms
from ENGRAVEAlerts.voicecall import voicecall


def tab_complete(text, state):
    return (glob.glob(text + '*') + [None])[state]


def main(arguments=None):
    """
    *The main function used when ``cl_utils.py`` is run as a single script from the cl, or when installed as a cl command*
    """
    # SETUP THE COMMAND-LINE UTIL SETTINGS
    su = tools(
        arguments=arguments,
        docString=__doc__,
        logLevel="DEBUG",
        options_first=False,
        projectName="ENGRAVEAlerts",
        defaultSettingsFile=True
    )
    arguments, settings, log, dbConn = su.setup()

    # UNPACK REMAINING CL ARGUMENTS USING `EXEC` TO SETUP THE VARIABLE NAMES
    # AUTOMATICALLY
    for arg, val in arguments.iteritems():
        if arg[0] == "-":
            varname = arg.replace("-", "") + "Flag"
        else:
            varname = arg.replace("<", "").replace(">", "")
        if varname == "import":
            varname = "iimport"
        if isinstance(val, str) or isinstance(val, unicode):
            exec(varname + " = '%s'" % (val,))
        else:
            exec(varname + " = %s" % (val,))
        if arg == "--dbConn":
            dbConn = val
        log.debug('%s = %s' % (varname, val,))

    ## START LOGGING ##
    startTime = times.get_now_sql_datetime()
    log.info(
        '--- STARTING TO RUN THE cl_utils.py AT %s' %
        (startTime,))

    if init:
        from os.path import expanduser
        home = expanduser("~")
        filepath = home + "/.config/ENGRAVEAlerts/ENGRAVEAlerts.yaml"
        try:
            cmd = """open %(filepath)s""" % locals()
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            pass
        try:
            cmd = """start %(filepath)s""" % locals()
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except:
            pass
        return

    # SEND AN SMS TO THE NUMBERS REQUESTED
    if sms:
        alerts = esms(
            log=log,
            settings=settings
        )
        alerts.set_mobile_numbers(mobilenumbers)
        alerts.send_message(message)

    # CALL THE NUMBERS REQUESTED
    if call:
        from ENGRAVEAlerts import voicecall
        alerts = voicecall(
            log=log,
            settings=settings
        )
        alerts.set_mobile_numbers(mobilenumbers)
        alerts.make_voicecall(message)

    # LISTEN TO THE GCN NOTICES FOR LV AND SEND AN SMS IF TRIGGERED
    if listen:
        from ENGRAVEAlerts import gcnListener
        alerts = gcnListener(
            log=log,
            settings=settings,
            test=testFlag
        )
        alerts.listen()

    # CALL FUNCTIONS/OBJECTS

    if "dbConn" in locals() and dbConn:
        dbConn.commit()
        dbConn.close()
    ## FINISH LOGGING ##
    endTime = times.get_now_sql_datetime()
    runningTime = times.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE cl_utils.py AT %s (RUNTIME: %s) --' %
             (endTime, runningTime, ))

    return


if __name__ == '__main__':
    main()
