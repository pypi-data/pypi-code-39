#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# License: MIT


from .getdp_object import GetDPObject, ObjectItem
from .helpers import _comment, make_args


class Jacobian(GetDPObject):
    name = "Jacobian"
    content = ""

    def __init__(self, comment=None):
        self.comment = comment
        self._code = ""
        self.items = []
        self._content = ""
        self._content0 = ""
        super().__init__(name=self.name, content=self.content, comment=self.comment)

    @property
    def content(self):
        self._content = self._content0
        for const in self.items:
            self._content += const.code + "\n"
        self._content = self._content[:-1]
        return self._content

    #
    @content.setter
    def content(self, value):
        self._content = value

    def add(self, Name, **kwargs):
        self._content = self._content0
        o = ObjectItem(Name, **kwargs)
        self.items.append(o)
        return o

    def add_case(self, item_number=0, **kwargs):
        self.items[item_number].add(**kwargs)

    def add_case_item(self, item_number=0, case_number=0, **kwargs):
        self.items[item_number].cases[case_number].add(**kwargs)
