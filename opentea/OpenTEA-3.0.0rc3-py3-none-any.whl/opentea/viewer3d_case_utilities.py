#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Module to create 3D object visible in the 3D view """



import os
import logging

from math import pi, cos, sin
from time import time

import numpy as np

from . import PathTools, COMMON
from .geometry import rotation

__all__ = ["View3dObject"]


class View3dObject(PathTools):
    """ programmable Tk objects 3D trough python API
    """

    def __init__(self,
                 dataset,
                 anchor,
                 balise,
                 default_color="#ff0000",
                 default_aspect="edges",
                 base_dir=os.getcwd()):

        """ prepare a canvas object
        ds is an OpenTEA XML dataset
        anchor : prefix to name the familly
        balise : XML balise in the OpenTEA App
        """
        self.log = logging.getLogger(__name__)
        self.log.debug("Instance of View3DObject created")

        PathTools.__init__(self, base_dir=base_dir)

        self.anchor = anchor
        self.default_color = default_color
        self.default_aspect = default_aspect
        self.balise = balise
        # TODO : this should not be COMMON but the COMMON folder of the process
        # this would ask process, not dataset, as the argument of this class
        # which have a LOT of ramifications.
        # will wait till OpenTEA 2.2
        self.folder = self.abspath(COMMON)
        self.ds = dataset
        self.part_attributes = ["color", "aspect"]
        self.supported_elements = ["bar2"]

        self.list_vtx = []

        self.list_parts = []
        self.parts = {}
        self.ensure_dir(self.folder)

    def update(self):
        """ update the 3d balise
        """

        glancevar = ";".join([str(time()),
                              self.default_color,
                              self.default_aspect,
                              self.folder + "/" + self.anchor + ".case"
                             ])
        self.ds.setValue(glancevar, self.balise)

    def add_part(self,
                 part_name,
                 color=None,
                 aspect=None):
        """ initiate a new part
        """

        if color is None:
            color = self.default_color
        if aspect is None:
            aspect = self.default_aspect

        self.list_parts.append(part_name)
        self.parts[part_name, "color"] = color
        self.parts[part_name, "aspect"] = aspect
        for elts in self.supported_elements:
            self.parts[part_name, elts] = []

    def test_part(self, part):
        """ raise error id part is not declared
        """
        if part not in self.list_parts:
            msgerror = ("part "
                        + part
                        + " not in declared parts "
                        + str(self.list_parts))
            self.log.error(msgerror)
            raise IOError

    def add_segment(self, part, xyz, xyz2):
        """ append a segment to a part
        part - an existing part
        xyz = a tuple for coordinates
        xyz2 = a tuple for coordinates
        """

        self.test_part(part)
        index = self.vtx_index(xyz)
        index2 = self.vtx_index(xyz2)

        self.parts[part, "bar2"].append((index, index2))

    def add_point(self, part, xyz):
        """ append a point to a part
        part - an existing part
        xyz = a tuple for coordinates
        """
        self.add_segment(part, xyz, xyz)

    def vtx_index(self, xyz):
        """ return the index of a coordianate
        in the self.list_vtx.
        xyz = a tuple for coordinates
        if xyz not part of recorded coordinates , it is created
        """
        tuxyz = tuple(xyz)
        if tuxyz not in self.list_vtx:
            self.list_vtx.append(tuxyz)

        return self.list_vtx.index(tuxyz)

    def dump(self):
        """ write the case and geo file
        """
        self.update()

        casename = os.path.join(self.folder, self.anchor + ".case")
        geoname = os.path.join(self.folder, self.anchor + ".geo")

        if not self.list_parts:
            self.log.info("No part for anchor " + self.anchor)
            try:
                os.remove(casename)
                os.remove(geoname)
            except OSError:
                pass
            return

        ### case file ###
        content = ""
        content += "#\n"
        content += "# New 3d case file format for : " + self.anchor + "\n"
        content += "#\n"
        content += "\n"
        content += "FORMAT\n"
        content += "type:  ensight\n"
        content += "\n"
        content += "GEOMETRY\n"
        content += "model: " + self.anchor + ".geo\n"
        content += "\n"
        content += "# part formatting for viewer3D \n"
        for part in self.list_parts:
            attr_line = part + " "
            for attr in self.part_attributes:
                attr_line += attr + "=" + self.parts[part, attr] + " "
            content += "#V3D " + attr_line + "\n"

        with open(casename, "w") as fout:
            fout.write(content)

        ### geo file ###
        content = ""

        content += "\n"
        content += "\n"
        content += "node id given\n"
        content += "element id given\n"
        content += "coordinates\n"
        content += "{0: 8}".format(len(self.list_vtx)) + "\n"
        for i, vtx in enumerate(self.list_vtx):
            vtx_line = ""
            vtx_line += "{0: 8}".format(i + 1)
            for j in range(3):
                coord = "{0:+08.5E}".format(vtx[j])
                if coord[0] == "+":
                    coord = " " + coord[1:]
                vtx_line += coord
            content += vtx_line + "\n"

        for i, part in enumerate(self.list_parts):
            content += "part " + str(i + 1) + "\n"
            content += part + "\n"
            for elt in self.supported_elements:
                if self.parts[part, elt]:
                    content += "bar2\n"
                    content += "{0: 8}".format(
                        len(self.parts[part, elt])) + "\n"
                    for j, conn in enumerate(self.parts[part, elt]):
                        conn_line = ""
                        conn_line += "{0: 8}".format(j + 1)
                        for node in conn:
                            conn_line += "{0: 8}".format(node + 1)
                        content += conn_line + "\n"

        with open(geoname, "w") as fout:
            fout.write(content)


# primitives

    def add_plane(self, part, origin, normal, tangent1, size1, size2, n1, n2):
        """ add cartesian plane
        part : an existing part name
        origin : 3D tuple, the center of the plane
        normal : the direction normal to the plane
        tangent1 : approximate vector tengeant to the plane, for direction 1
        size1 : size of the rectangle in direction tangent1
        size2 : size of the rectangle orthogonal to direction 1
        n1 : sampling in direction 1
        n2 : sampling in direction 2
        """
        self.test_part(part)
        # comput frame
        normal /= np.linalg.norm(normal)
        dir2 = np.cross(normal, tangent1)
        dir2 /= np.linalg.norm(dir2)
        dir1 = np.cross(dir2, normal)

        llcorner = origin - 0.5 * size1 * dir1 - 0.5 * size2 * dir2
        lrcorner = origin + 0.5 * size1 * dir1 - 0.5 * size2 * dir2
        ulcorner = origin - 0.5 * size1 * dir1 + 0.5 * size2 * dir2
        urcorner = origin + 0.5 * size1 * dir1 + 0.5 * size2 * dir2

        for i in range(n1):
            scale = 1. * i / (n1 - 1)
            start = llcorner * scale + lrcorner * (1 - scale)
            end = ulcorner * scale + urcorner * (1 - scale)
            self.add_segment(part, start, end)
        for i in range(n2):
            scale = 1. * i / (n2 - 1)
            start = urcorner * scale + lrcorner * (1 - scale)
            end = ulcorner * scale + llcorner * (1 - scale)
            self.add_segment(part, start, end)

    def add_box(self, part, xyz1, xyz2, nsampling):
        """ add cartesian box
        part : an existing part name
        xyz1 = point1
        xyz2 = point2
        nsampling : sampling in 3 directions

        """

        xyz1 = np.asarray(xyz1, dtype=float)
        xyz2 = np.asarray(xyz2, dtype=float)

        box_center = 0.5 * (xyz1 + xyz2)
        box_dim = xyz1 - xyz2

        for sign in [-1, 1]:
            shift = np.zeros(3)
            shift[0] = sign * 0.5 * box_dim[0]
            center = box_center + shift
            normal = [1, 0, 0]
            tangent1 = [0, 1, 0]
            self.add_plane(part,
                           center,
                           normal,
                           tangent1,
                           box_dim[1],
                           box_dim[2],
                           nsampling, nsampling)

            shift = np.zeros(3)
            shift[1] = sign * 0.5 * box_dim[1]
            center = box_center + shift
            normal = [0, 1, 0]
            tangent1 = [0, 0, 1]
            self.add_plane(part,
                           center,
                           normal,
                           tangent1,
                           box_dim[2],
                           box_dim[0],
                           nsampling, nsampling)

            shift = np.zeros(3)
            shift[2] = sign * 0.5 * box_dim[2]
            center = box_center + shift
            normal = [0, 0, 1]
            tangent1 = [1, 0, 0]
            self.add_plane(part,
                           center,
                           normal,
                           tangent1,
                           box_dim[0],
                           box_dim[1],
                           nsampling, nsampling)

    def add_revsurf(self, part, origin, direction, dir_zeroangle, x1, x2, r1,
                    r2, angle_start, angle_end, samples_longi, samples_azi):
        """ Creates a 3D set for revolution surface,
        going from discs to cylinders
        origin  - origin point for the main direction (x,y,z)
        direction  - direction vector for the main direction (x,y,z)
        dir_zeroangle  - second vector, to define the zero angle plane (x,y,z)
        x1 - abcissa of first point on the dir axis, with respect to the origin
        x2 - abcissa of second point on the dir axis, wrt the origin
        r1 - radius of first point on the dir axis, wrt the origin
        r2 - radius of second point on the dir axis, wrt the origin
        angle_start - start angle in deg, 0 being in the plane (direction,dir2)
        angle_end - end angle in deg , 0 being in the plane (direction,dir2)
        samples_longi - longitudinal sampling
        samples_azi - azimuthal sampling
        """
        self.test_part(part)
        # comput frame
        direction /= np.linalg.norm(direction)
        tmp = np.cross(direction, dir_zeroangle)
        tmp /= np.linalg.norm(tmp)
        dir_zeroangle = np.cross(tmp, direction)

        theta0 = np.deg2rad(angle_start)
        theta1 = np.deg2rad(angle_end)
        dtheta = (theta1-theta0)/(samples_azi-1)

        point1 = origin + x1 * direction + r1 * dir_zeroangle
        point2 = origin + x2 * direction + r2 * dir_zeroangle

        initial_angle = rotation(origin, direction, theta0)
        shift_angle = rotation(origin, direction, dtheta)

        # initial segment
        p1_cur = initial_angle.rotate(point1)
        p2_cur = initial_angle.rotate(point2)
        self.add_segment(part, p1_cur, p2_cur)

        for _ in range(samples_azi - 1):
            p1_nex = shift_angle.rotate(p1_cur)
            p2_nex = shift_angle.rotate(p2_cur)
            self.add_segment(part, p1_nex, p2_nex)

            for j in range(samples_longi):
                scale = 1.0 * j / (samples_longi - 1)
                pa = scale * p1_cur + (1 - scale) * p2_cur
                pb = scale * p1_nex + (1 - scale) * p2_nex
                self.add_segment(part, pa, pb)

            p1_cur = p1_nex
            p2_cur = p2_nex

    def add_disc(self, part, origin, direction, rmin, rmax):
        """ add a disc
        orgin (x,y,z) the center of the disc
        direction  (x,y,z) the normal of the disc
        rmin minimal radius
        rmax maximal radius
        sample : sampling
        """

        SAMPLING_AZI = 24
        SAMPLING_RAD = 4

        # define the ref frame
        direction /= np.linalg.norm(direction)

        xaxis = np.zeros(3)
        xaxis[0] = 1.0
        if np.dot(direction, xaxis) == 1.0:
            dir2 = (0, 1, 0)
        else:
            tmp = (1, 0, 0)
            dir2 = np.cross(direction, tmp)
            dir2 /= np.linalg.norm(dir2)

        self.add_revsurf(part, origin, direction, dir2, 0, 0, rmin,
                         rmax, -180, 180, SAMPLING_RAD, SAMPLING_AZI)

    def add_sphere(self, part, origin, radius, sampling=15):
        """ add a sphere
        orgin (x,y,z) the center of the sphere
        radius radius
        sampling number of points
        """
        # define the ref frame
        direction = (1, 0, 0)
        dir2 = (0, 1, 0)
        sampling_revsurf = int(sampling*0.5)
        for i in range(sampling_revsurf):
            theta0 = pi * i / (sampling_revsurf - 1)
            theta1 = pi * (i + 1) / (sampling_revsurf - 1)
            x0 = radius * cos(theta0)
            r0 = radius * sin(theta0)
            x1 = radius * cos(theta1)
            r1 = radius * sin(theta1)
            self.add_revsurf(part, origin, direction, dir2, x0, x1, r0,
                             r1, -180, 180, 2, sampling)

    def add_cylinder(self, part, origin, direction, length, radius):
        """ add a cylinder
        orgin (x,y,z) the center of the cylinder
        direction  (x,y,z) the axis of the cylinder
        radius : the radius
        length : the length
        """

        SAMPLING_AZI = 12
        SAMPLING_RAD = 2

        # define the ref frame
        direction /= np.linalg.norm(direction)
        xaxis = np.zeros(3)
        xaxis[0] = 1.0
        if np.dot(direction, xaxis) == 1.0:
            dir2 = (0, 1, 0)
        else:
            tmp = (1, 0, 0)
            dir2 = np.cross(direction, tmp)
            dir2 /= np.linalg.norm(dir2)

        self.add_revsurf(part, origin, direction, dir2, 0, length, radius,
                         radius, -180, 180, SAMPLING_RAD, SAMPLING_AZI)

    def add_cone(self, part, origin, direction, length, radius):
        """ add a cone
        orgin (x,y,z) the center of the cone
        direction  (x,y,z) the axis of the cone
        radius : the radius
        length : the length
        """

        SAMPLING_AZI = 24
        SAMPLING_RAD = 4

        # define the ref frame
        direction /= np.linalg.norm(direction)
        xaxis = np.zeros(3)
        xaxis[0] = 1.0
        if np.abs(np.dot(direction, xaxis)) == 1.0:
            dir2 = (0, 1, 0)
        else:
            tmp = (1, 0, 0)
            dir2 = np.cross(direction, tmp)
            dir2 /= np.linalg.norm(dir2)

        self.add_revsurf(part, origin, direction, dir2, 0, length, 0,
                         radius, -180, 180, SAMPLING_RAD, SAMPLING_AZI)
