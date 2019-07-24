# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 22:47:12 2019

@author: Reuben
"""

import fastwire

import unittest


class Test_Decorators(unittest.TestCase):
    
    def test_receive(self):
        signal = fastwire.Signal()

        class A(fastwire.Wired):
            @fastwire.receive(signal)
            def connected(self, a):
                self._a = a

        a = A()
        self.assertEqual(len(signal._receivers.keys()), 1)

        
    def test_supply(self):
        signal = fastwire.Signal(receiver_limit=1)

        class A(fastwire.Wired):
            @fastwire.supply(signal)
            def connected(self, a):
                self._a = a

        a = A()
        self.assertEqual(len(signal._receivers.keys()), 1)

        
    def test_receive_emit(self):
        signal = fastwire.Signal()

        class A(fastwire.Wired):
            @fastwire.receive(signal)
            def connected(self, a):
                self._a = a

        a = A()
        val = 5.7
        signal.emit(a=val)
        self.assertEqual(a._a, val)


    def test_fn_receive_emit(self):
        signal = fastwire.Signal()

        test = [0]
        
        @fastwire.fn_receive(signal)
        def connected(a):
            test[0] = a

        val = 5.7
        signal.emit(a=val)
        self.assertEqual(test[0], val)
