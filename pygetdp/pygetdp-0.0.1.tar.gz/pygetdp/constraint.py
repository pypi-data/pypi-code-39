#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Benjamin Vial
# License: MIT


from .getdp_object import GetDPObject
from .helpers import make_args, _comment


class CaseItem_(object):
    def __init__(self, Region, comment=None, **kwargs):
        self.Region = Region
        self.comment = comment
        self.code = ""
        c = "{" + " Region {}".format(Region)
        for k, v in kwargs.items():
            self.__setattr__(k, v)
            c += "; " + k + " " + make_args(v, sep=",")
        c += "; } "
        if self.comment:
            c += _comment(comment)
        self.code += c


class Case_(object):
    def __init__(self, Name=None, comment=None, **kwargs):
        self.Name = Name
        self.comment = comment
        self.code = ""
        self.case_items = []
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        case_name = Name or ""
        c = "Case {} ".format(case_name)
        c += "{ "
        if self.comment:
            c += _comment(comment)
        c += " \n     }"
        self.code += c

    def add(self, *args, **kwargs):
        case_item = CaseItem_(*args, **kwargs)
        s = self.code
        n = 7
        self.code = s[:-n] + "\n       " + case_item.code + s[-n:]
        self.case_items.append(case_item)


class Constraint_(object):
    def __init__(self, Name, comment=None, **kwargs):
        self.Name = Name
        self.comment = comment
        self._code = ""
        self.cases = []
        c = "{" + " Name {}".format(Name)
        for k, v in kwargs.items():
            self.__setattr__(k, v)
            c += "; " + k + " " + make_args(v, sep=",")
        c += "; "
        if self.comment:
            c += _comment(comment)
        c += "\n}"
        self._code += c
        self._code0 = self._code

    @property
    def code(self):
        s = self._code0
        for case in self.cases:
            self._code = s[:-2] + "\n     " + case.code + s[-2:]
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    def add(self, *args, **kwargs):
        self._code0 = self.code
        case = Case_(*args, **kwargs)
        self.cases.append(case)
        return case


class Constraint(GetDPObject):
    """ Creates a constraint object: specifying constraints on function spaces and formulations
        Types for Constraint:
        
        Assign
            To assign a value (e.g., for boundary condition).
        
        Init
            To give an initial value (e.g., initial value in a time domain analysis). If two values are provided (with Value [ expression, expression ]), the first value can be used using the InitSolution1 operation. This is mainly useful for the Newmark time-stepping scheme.
        
        AssignFromResolution
            To assign a value to be computed by a pre-resolution.
        
        InitFromResolution
            To give an initial value to be computed by a pre-resolution.
        
        Network
            To describe the node connections of branches in a network.
        
        Link
            To define links between degrees of freedom in the constrained region with degrees of freedom in a “reference” region, with some coefficient. For example, to link the degrees of freedom in the contrained region Left with the degrees of freedom in the reference region Right, located Pi units to the right of the region Left along the X-axis, with the coeficient -1, one could write:

            { Name periodic;
              Case {
                { Region Left; Type Link ; RegionRef Right;
                  Coefficient -1; Function Vector[X[]+Pi, Y[], Z[]] ;
                  < FunctionRef XYZ[]; >
                }
              }
            }

            In this example, Function defines the mapping that translates the geometrical elements in the region Left by Pi units along the X-axis, so that they correspond with the elements in the reference region Right. For this mapping to work, the meshes of Left and Right must be identical. (The optional FunctionRef function allows to transform the reference region, useful e.g. to avoid generating overlapping meshes for rotational links.)
        
        LinkCplx
            To define complex-valued links between degrees of freedom. The syntax is the same as for constraints of type Link, but Coeficient can be complex.
        """

    name = "Constraint"
    content = ""

    def __init__(self, comment=None):
        self.comment = comment
        self._code = ""
        self.constraints = []
        self._content = ""
        self._content0 = ""
        super().__init__(name=self.name, content=self.content)

    @property
    def content(self):
        self._content = self._content0
        for const in self.constraints:
            self._content += const.code + "\n"
        self._content = self._content[:-1]
        return self._content

    #
    @content.setter
    def content(self, value):
        self._content = value

    def add(self, Name, **kwargs):
        self._content = self._content0
        bc = Constraint_(Name, **kwargs)
        self.constraints.append(bc)
        return bc

    def assign(self, Name, **kwargs):
        return self.add(Name, Type="Assign", **kwargs)
