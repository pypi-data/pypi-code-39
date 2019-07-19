#!/usr/local/bin/python
# encoding: utf-8
"""
*Send SMS Alerts to ENGRAVErs*

:Author:
    David Young

:Date Created:
    March  1, 2019
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from twilio.rest import Client
import time


class sms():
    """
    *The worker class for the sms module*

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary

    **Usage:**

        To setup your logger, settings and database connections, please use the ``fundamentals`` package (`see tutorial here <http://fundamentals.readthedocs.io/en/latest/#tutorial>`_). 

        To initiate a sms object, use the following:

        .. todo::

            - add a tutorial about ``sms`` to documentation

        .. code-block:: python 

            from ENGRAVEAlerts import sms
            alerts = sms(
                log=log,
                settings=settings
            )
    """
    # Initialisation

    def __init__(
            self,
            log,
            settings=False
    ):
        self.log = log
        log.debug("instansiating a new 'sms' object")
        self.settings = settings
        self.numbers = []
        self.mynumber = self.settings["twilio"][
            "phone"]
        self.mynumber2 = self.settings["twilio"][
            "phone2"]
        self.myid = self.settings["twilio"][
            "smsid"]
        self.client = Client(self.settings["twilio"][
                             "sid"], self.settings["twilio"]["auth_token"])

        return None

    def set_mobile_numbers(
            self,
            numbers):
        """*set the recipients of the SMS alert as either a single number or a list of numbers*

        **Key Arguments:**
            - ``numbers`` -- either a single mobile number as a string, a comma separated string or a list of numbers.

        **Usage:**

            .. code-block:: python 

                from ENGRAVEAlerts import sms
                this = sms(
                    log=log,
                    settings=settings
                )
                this.set_mobile_numbers("+4479134471, +44791253271, +44791345391")
        """
        self.log.debug('starting the ``set_mobile_numbers`` method')

        if isinstance(numbers, str):
            numbers = numbers.replace(",", " ")
            numbers = numbers.split()

        tmp = []
        tmp[:] = [t.strip() for t in numbers]
        self.numbers = tmp

        self.log.debug('completed the ``set_mobile_numbers`` method')
        return None

    def send_message(
            self,
            message):
        """*send a message (160 characters) to the list of mobile numbers*

        **Key Arguments:**
            - ``message`` -- the message (will be clipped to 160 characters)

        **Usage:**

            .. code-block:: python 

                from ENGRAVEAlerts import sms
                alerts = sms(
                    log=log,
                    settings=settings
                )
                alerts.set_mobile_numbers("+4479134471, +44791253271, +44791345391")
                alerts.send_message("this is a test from the ENGRAVEAlerts package")
        """
        self.log.debug('starting the ``send_message`` method')

        if len(self.numbers) == 0:
            log.error('cound not send sms - no mobile numbers were given')
            return None

        for n in self.numbers:
            sent = False
            try:
                sms = self.client.messages.create(
                    body=message[0:300],
                    from_=self.mynumber,
                    to=n
                )
                sent = True
            except Exception, e:
                print "Can't send to %(n)s" % locals()
                print "%(e)s" % locals()
                pass

            if not sent:
                # TRY THE BACKUP NUMBER IF DEFAULT NUMBER DIDN'T WORK (e.g.
                # WITH NORTH AMERICAN NUMBERS)
                try:
                    sms = self.client.messages.create(
                        body=message[0:300],
                        from_=self.mynumber2,
                        to=n
                    )
                    sent = True
                except Exception, e:
                    print "Can't send to %(n)s" % locals()
                    print "%(e)s" % locals()
                    pass

        self.log.debug('completed the ``send_message`` method')
        return None
