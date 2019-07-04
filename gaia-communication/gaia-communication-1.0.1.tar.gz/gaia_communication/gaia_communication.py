def interruption_to_esp():
    # !/usr/bin/env/python
    # -*- coding: utf-8 -*-
    import serial
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

    from gps import *
    import time

    gpsd = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
    # '\t' = TAB to try and output the data in columns.
    print 'latitude\tlongitude\tspeed'

    try:

        while True:
            report = gpsd.next()
            if report['class'] == 'TPV':

                print getattr(report, 'lat', 0.0), "\t",
                print getattr(report, 'lon', 0.0), "\t",
                # print  getattr(report,'epv','nan'),"\t",
                # print  getattr(report,'ept','nan'),"\t",
                print getattr(report, 'speed', 'nan'), "\t"
                time.sleep(1)

    except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c
        print "Done.\nExiting."
        return
