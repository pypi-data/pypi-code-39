#/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# ______                    _   _
#|  ____|                  | | (_)
#| |__  __  _____ ___ _ __ | |_ _  ___  _ __  ___
#|  __| \ \/ / __/ _ \ '_ \| __| |/ _ \| '_ \/ __|
#| |____ >  < (_|  __/ |_) | |_| | (_) | | | \__ \
#|______/_/\_\___\___| .__/ \__|_|\___/|_| |_|___/
#                    | |
#                    |_|
#
"""Exeptions.py

TODO

Created Nov 2016 by COOP team
"""

__all__ = ["XDRException",
           "XDRnoNodeException",
           "XDRtooManyNodesException",
           "XDRnoFileException",
           "XDRillFormed",
           "XDRUnknownValue",
           "XDRInterrupt",
           "OTException",
           "OTNoNodeException",
           "OTTooManyNodesException",
           "OTNoFileException",
           "OTIllFormed",
           "OTUnknownValue",
           "OTInterrupt",
          ]


class OTException(Exception):
    """Base exception for all OpenTEA library exceptions"""
    pass


class OTNoNodeException(OTException):
    """"No node found"""
    def __init__(self, msg="No node with this address found"):
        OTException.__init__(self, msg)


class OTTooManyNodesException(OTException):
    """Too many nodes have been found"""
    pass


class OTNoFileException(OTException):
    """No file found"""
    pass


class OTIllFormed(OTException):
    """Ill formed XML address"""
    pass


class OTUnknownValue(OTException):
    """Ill formed XML address"""
    def __init__(self, label, got_value, expected_values):
        OTException.__init__(self,
                             "XML tree at label {0} contains '{1}' but "
                             "expected one of : {2}".format(label,
                                                            got_value,
                                                            expected_values))


class OTInterrupt(OTException):
    """Interruption of the OpenTEA process"""
    pass


# For backwards compatibility, the old `XDR` form is kept
XDRException = OTException
XDRnoNodeException = OTNoNodeException
XDRtooManyNodesException = OTTooManyNodesException
XDRnoFileException = OTNoFileException
XDRillFormed = OTIllFormed
XDRUnknownValue = OTUnknownValue
XDRInterrupt = OTInterrupt
