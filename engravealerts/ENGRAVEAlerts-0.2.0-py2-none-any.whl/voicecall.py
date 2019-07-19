#!/usr/local/bin/python
# encoding: utf-8
"""
*Send voicecall alert to ENGRAVErs*

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
from ENGRAVEAlerts import sms
import urllib
import twilio

# OR YOU CAN REMOVE THE CLASS BELOW AND ADD A WORKER FUNCTION ... SNIPPET TRIGGER BELOW
# xt-worker-def


class voicecall(sms.sms):
    """
    *The worker class for the voicecall module*

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary

    **Usage:**

        To setup your logger, settings and database connections, please use the ``fundamentals`` package (`see tutorial here <http://fundamentals.readthedocs.io/en/latest/#tutorial>`_). 

        To initiate a voicecall object, use the following:

        .. todo::

            - add a tutorial about ``voicecall`` to documentation

        .. code-block:: python 

            from ENGRAVEAlerts import voicecall
            alerts = voicecall(
                log=log,
                settings=settings
            )
    """

    def make_voicecall(
            self,
            message):
        """*make a voice call with a short message*

        **Key Arguments:**
            - ``message`` -- the message to speak is recipient answers

        **Return:**
            - None

        **Usage:**

            .. code-block:: python 

                from ENGRAVEAlerts import voicecall
                alerts = voicecall(
                    log=log,
                    settings=settings
                )
                alerts.set_mobile_numbers(
                    "+44795432071, +4474355071, +44343553371")
                alerts.make_voicecall(
                    "this is a test from the ENGRAVEAlerts package")

        """
        self.log.debug('starting the ``make_voicecall`` method')

        if len(self.numbers) == 0:
            log.error('cound not make voice call - no mobile numbers were given')
            return None
        for n in self.numbers:

            try:
                messageForCall = urllib.quote(message) + "&"
                call = self.client.calls.create(to=n,
                                                from_=self.mynumber,
                                                url="http://twimlets.com/message?Message%5B0%5D=" + messageForCall)
            except Exception, e:
                print "Can't call %(n)s" % locals()
                print "%(e)s" % locals()
                pass

        self.log.debug('completed the ``make_voicecall`` method')
        return None
