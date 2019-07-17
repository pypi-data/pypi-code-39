#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Module for a programmable TK canvas
"""



import os
import logging

from time import time
from . import COMMON, PathTools, OTException

__all__ = ["WinCanvas"]


class WinCanvas(PathTools):
    """ programmable Tk canvas trough python
    API components
    """

    def __init__(self, dataset, target, prefix, balise):
        """ prepare a canvas object
        target : id ot the canvas
        prefix : !
        balise : XML balise in the OpenTEA App
        """
        PathTools.__init__(self)
        self.prefix = prefix
        self.content = "\n"
        self.target = target
        self.balise = balise
        self.folder = COMMON
        self.log = logging.getLogger(__name__)
        self.ensure_dir(self.folder)

        file_list = self.get_file_list(("./" + self.folder + "/"),
                                       filter_search=(self.prefix + "*@" +
                                                      self.target + ".can"),
                                       output="absolute")
        for filename in file_list:
            self.log.debug("Removal of file " + filename)
            os.remove(filename)

        glancevar = ";".join([str(time()), self.target,
                              ("./" + self.folder +
                               "/" + self.prefix +
                               "*@" + self.target + ".can")])

        dataset.setValue(glancevar, balise)

    def add_point(self, coords,
                  name="none",
                  title="none",
                  info="none",
                  moveable="no",
                  color="black",
                  size="1"):
        """ point object
        coords : 2 elements lists
        name : id of the object
        title : shown (permanent)
        info : text only during hoovering over object
        moveable : make position interactively adjustable
        color : color of the object
        size : float, 1 stands for 20 pix
        """
        self.content += "BEGIN\n"
        self.content += "TYPE=POINT" + "\n"
        self.content += "NAME=" + name + "\n"
        self.content += "INFO=" + info.replace("\n", "BREAKLINE") + "\n"
        self.content += "TITLE=" + title + "\n"
        self.content += "MOVEABLE=" + moveable + "\n"
        self.content += "SIZE=" + str(size) + "\n"
        self.content += "COLOR=" + color + "\n"
        strcoord = ""
        for x in coords:
            strcoord += str(x) + " "
        self.content += "COORDS=" + strcoord + "\n"
        self.content += "END\n\n"

    def add_segment(self, coords,
                    name="none",
                    title="none",
                    info="none",
                    moveable="no",
                    color="black",
                    fillcolor="",
                    refinement="no",
                    style="open"):
        """ segment object
        coords: list of 2xn coords
        name: id of the object
        title: shown (permanent)
        info: text only during hoovering over object
        moveable: make position interactively adjustable
            no/address of the widget
        refinement: no/yes
        color: color of the object
        style: open/closed, wether the polyline is closed or not.
        """
        for forbid in ["-", " "]:
            if "-" in name:
                msgerr = ("Function add segment: name " + name +
                          " not valid. Character " + forbid + " forbidden")
                self.log.error(msgerr)
                raise OTException
        self.content += "BEGIN\n"
        self.content += "TYPE=SEGMENT" + "\n"
        self.content += "NAME=" + name + "\n"
        self.content += "INFO=" + info.replace("\n", "BREAKLINE") + "\n"
        self.content += "TITLE=" + title + "\n"
        self.content += "MOVEABLE=" + moveable + "\n"
        self.content += "REFINEMENT=" + refinement + "\n"
        self.content += "COLOR=" + color + "\n"
        self.content += "FILLCOLOR=" + fillcolor + "\n"
        self.content += "STYLE=" + style + "\n"
        strcoord = ""
        for x in coords:
            strcoord += str(x) + " "
        self.content += "COORDS=" + strcoord + "\n"
        self.content += "END\n\n"

    def add_slider(self, coords, support,
                   name="none",
                   title="none",
                   info="none",
                   moveable="no",
                   npts=3,
                   color="black"):
        """ segment object
        coords : 1 or 2 element curvilinear coordinate (in m)
        support : id of the polyline
        name : id of the object
        title : shown (permanent)
        info : text only during hoovering over object
        moveable : make position interactively adjustable
        color : color of the object
        npts : if 2 elements, number of dots to represent the slider
        """
        self.content += "BEGIN\n"
        self.content += "TYPE=SLIDER" + "\n"
        self.content += "NAME=" + name + "\n"
        self.content += "INFO=" + info.replace("\n", "BREAKLINE") + "\n"
        self.content += "TITLE=" + title + "\n"
        self.content += "MOVEABLE=" + moveable + "\n"
        self.content += "SUPPORT=" + support + "\n"
        self.content += "NPTS=" + str(npts) + "\n"
        self.content += "COLOR=" + color + "\n"
        strcoord = ""
        for x in coords:
            strcoord += str(x) + " "
        self.content += "COORDS=" + strcoord + "\n"
        self.content += "END\n\n"

    def add_image(self, filename, dump="none"):
        """ image object
        dump : none/yes. Allow to dump the BMP content in RGB format
        Images are no more moveable due to calibration issues
        The canvas images will be centered on 0 0 canvas coords.
        name = os.path.basename(filename)
        """
        self.content += "BEGIN\n"
        self.content += "TYPE=IMAGEGIF" + "\n"
        self.content += "NAME=bkimage\n"
        self.content += "DUMP=" + dump + "\n"
        self.content += "FILENAME=" + filename + "\n"
        self.content += "MOVEABLE=none\n"
        self.content += "COORDS=0 0\n"
        self.content += "END\n\n"

    def add_calibration(self, coords, pixcoords, calibsource):
        """ image object
        coords : 2x2d coords, real metric
        pixcoords : 2x2d coords, image metric
        calibsource : XML balise in OpenTEA app.
        """
        self.content += "BEGIN\n"
        self.content += "TYPE=CALIBRATION" + "\n"
        self.content += "NAME=calibration" + "\n"
        self.content += "MOVEABLE=" + calibsource + "\n"
        strcoord = ""
        for x in coords:
            strcoord += str(x) + " "
        self.content += "COORDS=" + strcoord + "\n"
        strcoord = ""
        for x in pixcoords:
            strcoord += str(x) + " "
        self.content += "PIXCOORDS=" + strcoord + "\n"
        self.content += "END\n\n"

    def dump_object(self):
        """ save the object """
        tmpFile = open(
            os.path.join(self.folder, self.prefix)
            + "@" + self.target + ".can",
            "w")
        tmpFile.write(self.content)
        tmpFile.close()
