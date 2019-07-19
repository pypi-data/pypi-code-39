#!/usr/local/bin/python
# encoding: utf-8
"""
*Listen to GCN LV Alerts*

:Author:
    David Young

:Date Created:
    March  3, 2019
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
import gcn
from ENGRAVEAlerts import sms
import lxml.etree
from datetime import datetime
import requests
import operator
# THE LVC-GCN HANDLER
try:
    # for Python 2.x
    from StringIO import StringIO
except ImportError:
    # for Python 3.x
    from io import StringIO
import unicodecsv as csv
import bitly_api


class gcnListener():
    """
    *The worker class for the gcnListener module*

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``test`` -- use test settings for development purposes

    **Usage:**

        To setup your logger, settings and database connections, please use the ``fundamentals`` package (`see tutorial here <http://fundamentals.readthedocs.io/en/latest/#tutorial>`_).

        To initiate a gcnListener object, use the following:

        .. code-block:: python

            from ENGRAVEAlerts import gcnListener
            alerts = gcnListener(
                log=log,
                settings=settings
            )
    """

    def __init__(
            self,
            log,
            settings=False,
            test=False
    ):
        # OBJECT VARIABLES
        self.log = log
        log.debug("instansiating a new 'gcnListener' object")
        self.settings = settings
        self.eventCache = []
        self.contacts = []
        self.test = test

        # INITIAL ACTIONS - CACHE THE CONTACTS FROM GOOGLE SHEET (SHEET ID IN
        # SETTING FILE)
        self.cache_alert_contacts()

        return None

    def listen(
            self,
            testEventPacket=False):
        """*listen to the GCN notice stream and trigger SMS alerts if new GW event discovered*

        **Key Arguments:**
            - ``testEventPacket`` -- use a local VOEvent Packet to test the process_gcn function

        **Return:**
            - None

        **Usage:**

            .. code-block:: python

                from ENGRAVEAlerts import gcnListener
                alerts = gcnListener(
                    log=log,
                    settings=settings
                )
                alerts.listen()
        """
        self.log.debug('starting the ``listen`` method')

        # FILTER THE GCNs TO ONLY LVC ORIGIN
        @gcn.handlers.include_notice_types(
            gcn.notice_types.LVC_PRELIMINARY,
            gcn.notice_types.LVC_INITIAL)
        def process_gcn(payload, root):

            smsContent = ""

            # DECIDE HOW TO RESPOND FOR REAL/TEST EVENTS
            if root.attrib['role'] == 'observation':
                pass
            if root.attrib['role'] == 'test':
                # IF THIS IS NOT A TEST THEN IGNORE THE GCN TEST STREAM
                if not self.test:
                    return
                smsContent = "TEST ALERT: "

            # READ ALL OF THE VOEVENT PARAMETERS FROM THE "WHAT" SECTION.
            params = {elem.attrib['name']:
                      elem.attrib['value']
                      for elem in root.iterfind('.//Param')}

            try:
                # TRY AND PARSE ORDERED CLASSIFICATIONS
                classList = ["BNS", "NSBH", "BBH", "MassGap", "Terrestrial"]
                classifications = {}

                for c in classList:
                    classifications[c] = float(params[c])

                sorted_classifications = sorted(
                    classifications.items(), key=operator.itemgetter(1), reverse=True)

                classifictions = "\n\nClassification of signal in desc. order of prob is "
                for i, v in enumerate(sorted_classifications):
                    k = v[0]
                    v = float(v[1]) * 100
                    if float(v) < 1:
                        v = "<1"
                    else:
                        v = int(round(v))
                    if i == 4:
                        classifictions += " or "
                    elif i > 0:
                        classifictions += ", "
                    classifictions += "%s (%s%%)" % (k, v)
            except:
                pass

            try:
                # CONVERT FAR TO YEARS
                FAR = float(params["FAR"])
                FAR = 1. / (FAR * 60 * 60 * 24 * 365)

                if FAR < 10:
                    FAR = "%(FAR)1.2f" % locals()
                elif FAR < 100:
                    FAR = "%(FAR)1.1f" % locals()
                else:
                    FAR = int(round(FAR))
                params["FAR"] = FAR
            except:
                pass

            # PARSE THE EVENT TIME
            eventTime = "?"
            for elem in root.iterfind('.//ISOTime'):
                eventTime = elem.text
                try:
                    eventTime = datetime.strptime(
                        eventTime, '%Y-%m-%dT%H:%M:%S.%f')
                    eventTime = eventTime.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    print "Could not convert time stamp"
                    pass
                eventTime = eventTime + " UT"
            params["eventTime"] = eventTime

            # BUILD ALERT CONTENT
            smsContent += "%(AlertType)s notice for %(GraceID)s, a %(Group)s event detected at %(eventTime)s.\n\nFAR=1 every %(FAR)s yrs." % params

            if params["Group"] == "CBC":
                smsContent += classifictions

            # SLACK URL
            # smsContent += "https://bit.ly/2VZdoWL  "

            API_USER = self.settings["bitly"]["user"]
            API_KEY = self.settings["bitly"]["api_key"]
            try:
                b = bitly_api.Connection(API_USER, API_KEY)
                # SHORTEN GRACEDB URL
                longurl = params["EventPage"]
                params["EventPage"] = b.shorten(uri=longurl)["url"]
            except:
                pass

            try:
                smsContent += " %(EventPage)s" % params
            except:
                pass

            # PRINT ALL PARAMETERS TO STDOUT
            for key, value in params.items():
                print key, ':', value

            # ONLY TRIGGER SMS ON NEW EVENTS
            if params["GraceID"] not in self.eventCache:
                # TRY A REPARSE OF THE ALERT CONTACTS - USE CACHE IF FAIL
                try:
                    self.cache_alert_contacts()
                except:
                    pass

                # SEND SMS ALERTS
                alerts = sms(
                    log=self.log,
                    settings=self.settings
                )
                alerts.set_mobile_numbers(self.contacts)
                alerts.send_message(smsContent)

            # CACHE THE EVENT ID SO NOT TO DUPLICATE ALERTS
            self.eventCache.append(params["GraceID"])

        # TRIGGER process_gcn ONCE IF TEST ALERT PACKET GIVEN - ELSE OPEN GCN
        # LISTENER
        if not testEventPacket:
            gcn.listen(handler=process_gcn)
        else:
            payload = open(testEventPacket, 'rb').read()
            root = lxml.etree.fromstring(payload)
            process_gcn(payload, root)

        self.log.debug('completed the ``listen`` method')
        return None

    def cache_alert_contacts(
            self):
        """*Download a copy of the alert contacts from google sheet and parse numbers into an array*

        **Return:**
            - None

        **Usage:**

            .. code-block:: python 

                from ENGRAVEAlerts import gcnListener
                alerts = gcnListener(
                    log=log,
                    settings=settings
                )
                alerts.cache_alert_contacts()
        """
        self.log.debug('starting the ``cache_alert_contacts`` method')

        # GET THE RELEVANT GOOGLE SHEET ID (DEV OR PRODUCTION VERSION)
        if self.test:
            url = self.settings["contact_sheet"]["development"]
        else:
            url = self.settings["contact_sheet"]["production"]

        # REQUEST THE CONTENT OF THE SHEET
        content = False
        try:
            response = requests.get(
                url=url,
            )
            content = response.content
            status_code = response.status_code
        except requests.exceptions.RequestException:
            print 'HTTP Request failed'

        # SOMETIMES THE CONTENT HEADER ISN'T RETURNED CORRECTLY
        content = content.replace(
            '"Name","","",', '"Name","Mobile (with country code)","SMS Alerts",')

        if content:
            # READ AS CSV CONTENT
            f = StringIO(content)
            csvReader = csv.DictReader(
                f, dialect='excel', delimiter=',', quotechar='"')
            self.contacts = []
            for row in csvReader:
                # IF SMS TOGGLE IS ON THEN NUMBER APPEND TO ARRAY
                if "SMS Alerts" in row and row["SMS Alerts"] == "TRUE":
                    if "+" not in row["Mobile (with country code)"]:
                        row["Mobile (with country code)"] = "+" + \
                            row["Mobile (with country code)"]
                    self.contacts.append(row["Mobile (with country code)"])

        self.log.debug('completed the ``cache_alert_contacts`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method
