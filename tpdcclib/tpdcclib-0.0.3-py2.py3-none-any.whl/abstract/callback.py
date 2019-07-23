#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for tpQtLib
"""

from __future__ import print_function, division, absolute_import

import traceback

import tpDccLib as tp


class AbstractCallback(object):
    """
    Wrapper class to handle DCC callbacks in a DCC agnostic way
    """

    def __init__(self, fn=None, parent=None):
        super(AbstractCallback, self).__init__()
        self.callback_id = self.create_callback(fn, parent)
        tp.logger.debug('Adding Callback: %s' % self.callback_id)

    def __del__(self):
        try:
            self.remove_callback(self.callback_id)
            tp.logger.debug('Removing Callback: %s' % self.callback_id)
        except Exception:
            tp.logger.error('Error while removing Callback: %s | {}'.format(self.callback_id, traceback.format_exc()))

    def __repr__(self):
        return 'MCallbackIdWrapper(%r)' % self.callback_id

    def create_callback(self, fn, parent):
        return None

    @staticmethod
    def remove_callback(callback_id):
        pass
