from pointwise import GlyphClient
from pointwise.glyphapi import *

def echo(text):
    print "Script:", text 

# port 0 is special as it launches a Glyph batch process locally

with GlyphClient(port=0, callback=echo) as glf:

# port 2807 is the default Glyph Server port (when running active server
# in Pointwise GUI)

#with GlyphClient(port=2807, callback=echo) as glf:

    pw = glf.get_glyphapi()

    pw.Connector.setCalculateDimensionMethod("Spacing")
    pw.Connector.setCalculateDimensionSpacing(.3)

    # create a loop of connectors from a cyclic list of points
    points = [(0, 0, 0), (10, 0, 0), (10, 10, 0), (0, 10, 0)]
    cons = []
    with pw.Application.begin("Create") as creator:
        for p1, p2 in zip(points, points[1:]+points[:1]):
            seg = pw.SegmentSpline()
            seg.addPoint(p1)
            seg.addPoint(p2)
            con = pw.Connector()
            con.addSegment(seg)
            con.calculateDimension() 
            cons.append(con)

    # create an unstructured domain from the connectors
    with pw.Application.begin("Create") as creator:
        edge = pw.Edge.createFromConnectors(cons)
        dom = pw.DomainUnstructured()
        dom.addEdge(edge)

    print "Domain:", dom.getName(), "cells:", dom.getCellCount()
