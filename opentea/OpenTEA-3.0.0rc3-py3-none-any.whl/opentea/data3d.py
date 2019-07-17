#!/usr/bin/env python



from math import sqrt, atan2, pi, hypot, cos, sin



def grouped(iterable, n):
    """ To iter n by n
    s -> (s0, s1, s2, ...sn-1), (sn, sn + 1, sn + 2, ...s2n-1),
    (s2n, s2n + 1, s2n + 2, ...s3n-1), ...
    """
    
    return list(zip(*[iter(iterable)]*n))


def norm(u):
    """ norm of a dictionary
    !see numpy
    """
    return sqrt(u["x"]**2 + u["y"]**2 + u["z"]**2)


def rotate(y, z, rotate_deg):
    """ rotation 2D of y, z coordinates
    ! see numpy
    """
    r = hypot(z, y)
    theta = atan2(z, y) + rotate_deg*pi/180
    y = r*cos(theta)
    z = r*sin(theta)
    return [y, z]


def makevect(points, a, b):
    """
    ! WTF
    """
    res = {}
    res["x"] = points[b, "x"] - points[a, "x"]
    res["y"] = points[b, "y"] - points[a, "y"]
    res["z"] = points[b, "z"] - points[a, "z"]
    return res


def pvect(u, v):
    """ cross product
    u, v dict with x, y, z entries
    """
    res = {}
    res["x"] = u["y"] * v["z"] - u["z"] * v["y"]
    res["y"] = u["z"] * v["x"] - u["x"] * v["z"]
    res["z"] = u["x"] * v["y"] - u["y"] * v["x"]
    return res


def getparts(data, subpart=""):
    """ read the parts in data
    is subpart (string) not null,
    read the data/suppart
    """
    if subpart != "":
        subpart = "." + subpart
    res = None
    i = data.index("root" + subpart + ".children :") + 1
    res = data[i].strip().split(", ")
    return res


def dumpparts(list_parts, subpart=""):
    """ write the parts in data
    list_part being a list of parts
    if subpart (string) not null,
    write the data/part/subpart
    """
    if subpart != "":
        subpart = "." + subpart
    res = "root" + subpart + ".children :\n" + ", ".join(list_parts) + "\n\n"
    return res


def getfield(part, field, data, datatype="integer", subpart=""):
    """ read dataset of data/part/subpart/field
    datatype is either spacedstring/float, integer
    """
    if subpart != "":
        subpart = "." + subpart
    i = data.index("root." + part + subpart + "." + field + " :") + 1
    j = i
    while data[j] != "":
        j += 1
    out = [_f for _f in ", ".join(data[i:j]).split(", ") if _f]

    if field == "children":
        datatype = "spacedstring"
    if datatype == "spacedstring":
        pass
    if datatype == "float":
        out = [float(x) for x in out]
    if datatype == "integer":
        out = [int(x) for x in out]
    return out


def dumpfield(part, field, listdata, subpart=""):
    """Dump field in part/subpart/field"""
    if subpart != "":
        subpart = "." + subpart
    dump = "root." + part + subpart + "." + field + " :\n"
    maxcol = 10
    col = 1
    for item in listdata:
        dump += str(item) + ", "
        if col == maxcol:
            dump += "\n"
            col = 1
        col += 1
    dump += "\n\n"
    return dump
