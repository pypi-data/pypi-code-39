#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# License: MIT


from .helpers import _comment, _add_raw_code


class GetDPObject(object):
    """
    Base Getdp object


    """

    def __init__(self, name="Group", content="", comment=None):
        """Short summary.

        Parameters
        ----------
        name : str
            Name of the object.
        content : str
            Content of the object.
        comment : str
            A comment.

        """
        self.name = name
        self.content = content
        self.comment = comment
        self.indent = " " * 4  # len(self.name)
        return

    @property
    def code(self):
        code_ = []
        code_.append("{}{{".format(self.name))
        [code_.append(_) for _ in self.content.splitlines()]
        code_.append("}")
        code_ = ("\n" + self.indent).join(code_) + "\n"
        if self.comment:
            code_ = _comment(self.comment) + "\n" + code_
        return code_

    def add_raw_code(self, raw_code, newline=True):
        self.content = _add_raw_code(self.content, raw_code, newline=newline)

    def add_comment(self, comment, newline=True):
        self.add_raw_code(_comment(comment, newline=False), newline=newline)
