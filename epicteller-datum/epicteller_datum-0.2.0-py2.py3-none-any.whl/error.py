#!/usr/bin/env python
# -*- coding: utf-8 -*-


class DiceParameterInvalidError(ValueError):
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self.message = 'Dice parameter invalid: {}'.format(kwargs)


class InvalidOperatorError(ValueError):
    pass


class InvalidDiceletCalculationError(ValueError):
    pass
