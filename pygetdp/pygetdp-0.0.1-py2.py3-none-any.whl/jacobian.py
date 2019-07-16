#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# License: MIT


from .getdp_object import GetDPObject
from .helpers import make_args, _comment
from .constraint import Constraint_


class Jacobian_(Constraint_):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Jacobian(GetDPObject):
    name = "Jacobian"
    content = ""

    def __init__(self, comment=None):
        self.comment = comment
        self._code = ""
        self.items = []
        self._content = ""
        self._content0 = ""
        super().__init__(name=self.name, content=self.content)

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
        bc = Jacobian_(Name, **kwargs)
        self.items.append(bc)
        return bc
