# -*- coding: utf-8 -*-
"""Domain Driven Design base framework - Value Object."""


class ValueObject(object):
    def same_as(self, other):
        return self == other
