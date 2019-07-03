#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kgtools.annotation import Lazy


class Synset:
    def __init__(self, terms):
        self.terms = terms
        self.text = "<%s>" % ", ".join([term for term in list(sorted(self.terms, key=lambda x: x))])

    @Lazy
    def key(self):
        return max(self.terms, key=lambda x: len(x))

    def __add__(self, other):
        return Synset(self.terms | other.terms)

    def __str__(self):
        return self.text

    def __hash__(self):
        return hash(str(self))

    def __iter__(self):
        return iter(self.terms)

    def __eq__(self, other):
        return hash(self) == hash(other)
