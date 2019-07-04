from gps import *
import time
import serial


def interruption_to_esp():
    # !/usr/bin/env/python

    # -*- coding: utf-8 -*-
    port = "/dev/ttyUSB0"
    rate = 9600
    s1 = serial.Serial(port, rate)

# TODO: recieve location function
    while True:
        if s1.inWaiting() > 0:
            # if inputValue in comp_list: RECIEVE_LOCATION = LOCATION
            s1.write('0')
            return


def gps_data():
    # ! /usr/bin/python

    gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
    # '\t' = TAB to try and output the data in columns.

    lat = 0
    lon = 0

    while(lat == 0 and lon == 0):
        report = gpsd.next()
        if report['class'] == 'TPV':

            lat = getattr(report, 'lat', 0.0)
            lon = getattr(report, 'lon', 0.0)
            # print(getattr(report,'epv','nan'),"\t")
            # print(getattr(report,'ept','nan'),"\t",)
            speed = getattr(report, 'speed', 'nan')

    return (lat, lon, speed)
