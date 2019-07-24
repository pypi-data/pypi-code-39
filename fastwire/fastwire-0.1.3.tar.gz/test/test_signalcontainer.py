# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 22:46:33 2019

@author: Reuben
"""

import fastwire

import unittest


class Test_SignalContainer(unittest.TestCase):
    
    def test_unnamed_signal(self):
        sc = fastwire.SignalContainer()
        signal = sc.signal()
        self.assertEqual(signal.__class__, fastwire.Signal)
        
    def test_named_signal(self):
        sc = fastwire.SignalContainer()
        signal = sc.signal('this_name')
        self.assertEqual(signal.name, 'this_name')
