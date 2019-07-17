#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mesh.py

TODO

Created Nov 2016 by COOP team
"""



__all__ = ["Mesh"]
import re


import os
import logging
import h5py

from opentea.path_tools import PathTools
from opentea.constants import COMMON
from opentea.exceptions import OTException, OTInterrupt


class Mesh(PathTools):
    " Class Mesh that includes all the info about the mesh "

    def __init__(self, filename, process, **kwargs):
        self.process = process
        PathTools.__init__(self, base_dir=self.process.base_dir)
        self.h5_file = filename
        self.asciibound_file = self.h5_file.replace('mesh.h5', 'asciiBound')
        self.root_filename = (self.h5_file.replace('.mesh.h5', '')
                              .split("/")[-1])
        self.xmf_file = self.h5_file.replace('mesh.h5', 'mesh.xmf')
        self.ndim = None
        self.ndimlist = None
        self.nnodes = None
        self.ncells = None
        self.volelem_min = None
        self.volelem_max = None
        self.voldomain = None
        self.version = None
        self.npatches = None
        self.listofpatches = None
        self.listofsurfaces = None  # Surface area of patches
        self.listbndmin = None  # Bounding box
        self.listbndmax = None
        self.periodicity = None
        self._hmin = None
        self._hmax = None
        self.info_mesh_content = None
        self.__dict__.update(**kwargs)
        self.log = logging.getLogger(__name__)
        self.loadmesh_local()

    def __str__(self):
        """ string infos about the mesh """
        out_str = ""
        out_str += ("== Mesh infos ==" + "\n")
        out_str += (" Files      = " + self.root_filename + "\n")
        out_str += (" Files      = " + self.h5_file + "\n")
        out_str += (" Files      = " + self.xmf_file + "\n")
        out_str += (" Files      = " + self.asciibound_file + "\n")
        out_str += (" Version    = " + self.version + "\n")
        out_str += (" Ndim       = " + str(self.ndim) + "\n")
        out_str += (" N nodes    = " + str(self.nnodes) + "\n")
        out_str += (" N cells    = " + str(self.ncells) + "\n")
        out_str += (" Vol domain = " + str(self.voldomain) + "\n")
        out_str += (" Vol min    = " + str(self.volelem_min) + "\n")
        out_str += (" Vol max    = " + str(self.volelem_max) + "\n")
        out_str += (" N patches  = " + str(self.npatches) + "\n")
        out_str += (" Bnd min    = " + str(self.listbndmin) + "\n")
        out_str += (" Bnd max    = " + str(self.listbndmax) + "\n")
        out_str += (" Periodic case = " + str(self.periodicity) + "\n")
        out_str += (" List of patches :" + "\n")
        out_str += ("\n".join([str(item) for item in self.listofpatches])
                    + "\n")
        out_str += (" List of patches area :" + "\n")
        out_str += ("\n".join([str(item) for item in self.listofsurfaces])
                    + "\n")
        out_str += ("================" + "\n")
        return out_str

    def write_meshsample_choices(self, prefix, wdir):
        """ Write the choices file for the meshsample tool """
        os.chdir(wdir)
        choices = ("\'./../" + self.h5_file + "\' ! The mesh file\n" +
                   "\'./../" + self.asciibound_file + "\' ! asciiBound\n" +
                   " 1000 ! target number of samples ( skip IF = 0)\n" +
                   prefix + " ! prefix (5 CHARACTERs)\n")
        with open('meshsample.choices', 'w') as choices_file:
            choices_file.write(choices)

        os.chdir(self.process.base_dir)

    def write_hip_script(self, wdir):
        """ Write the hip script to read and write the hdf file avbp format """
        hipscript_ct = ("set check 0\n"
                        "read hdf \'./../" + self.h5_file + "\'\n"
                        "write hdf \'./" + self.root_filename + "\'\n"
                        "exit \n")
        with open(os.path.join(wdir, 'hipscript'), 'w') as fout:
            fout.write(hipscript_ct)

    def process_hip(self):
        """ Read the mesh with hip and write it again """
        local_common = self.abspath(COMMON)
        extor = self.process.get_executor("hip", [local_common])
        tmp_dir = extor.execute_dir
        tmp_dir_abs = self.abspath(tmp_dir)
        self.write_hip_script(tmp_dir_abs)
        extor.appli = "tool_hip"
        extor.execute()
        hip_warning_log = tmp_dir + "/hip-warning.log"
        if os.path.isfile(hip_warning_log):
            with open(hip_warning_log, "r") as fin:
                self.log.warning(fin.read())
        self.copy_file(tmp_dir_abs + "/" + self.root_filename
                       + ".mesh.h5", self.abspath(self.h5_file))
        self.copy_file(tmp_dir_abs + "/" + self.root_filename +
                       ".mesh.xmf", self.abspath(self.xmf_file))
        self.copy_file(tmp_dir_abs + "/" + self.root_filename +
                       ".asciiBound", self.abspath(self.asciibound_file))
        extor.finish()

    def execute_meshsample(self, prefix):
        """ Execute the hip tool to get the case en geo files that will
            be used to update the 3D view of the mesh
            hip 17.01 or higher
        """
        local_common = self.abspath(COMMON)
        if len(prefix) > 5:
            prefix = prefix[:5]
            self.log.warning("The name of the prefix has been trimmed down to "
                             "5 char")
        elif len(prefix) < 5:
            self.log.error("The name of the prefix is too short, should be 5 "
                           "char")
            raise OTException
        extor = self.process.get_executor("hip_meshsample", [local_common])
        extor.appli = "tool_hip"
        hipscript_ct = ("set check 0\n"
                        "read hdf \'./../" + self.h5_file + "\'\n"
                        "decimate \'" + self.h5_file + "\'\n"
                        "write ensight -a -s0 " + prefix + " \n"
                        "exit() \n")
        fname = os.path.join(self.process.base_dir,
                             extor.execute_dir,
                             'hipscript')
        with open(fname, 'w') as fout:
            fout.write(hipscript_ct)

        extor.execute()
        ex_dir = extor.abspath(extor.execute_dir)
        self.copy_file(ex_dir + "/" + prefix + ".case",
                       local_common)
        self.copy_file(ex_dir + "/" + prefix + ".geo",
                       local_common)
        extor.finish()

    def loadmesh_local(self):
        """ Load the mesh files in the COMMON directory"""
        abs_common = self.abspath(COMMON)
        self.h5_file = self.copy_file(self.h5_file,
                                      abs_common)
        self.asciibound_file = self.copy_file(self.asciibound_file,
                                              abs_common)
        try:
            self.xmf_file = self.copy_file(self.xmf_file,
                                           abs_common)
        except OSError:
            self.log.warning("No xmf file found for mesh")

        self.h5_file = self.relpath(self.h5_file)
        self.asciibound_file = self.relpath(self.asciibound_file)
        self.xmf_file = self.relpath(self.xmf_file)

    def get_mesh_version(self):
        """ Get the mesh version as a number from the hdf file """
        h5file = h5py.File(self.abspath(self.h5_file), "r")
        version_line = h5file["Parameters/hipversion"][()]
        h5file.close()

        # Hip versionstring follows the convention:
        #  "xx.xx(.x), 'Name of the version'"
        # The last digit is not always present and is forced to 0 if absent.

        match = re.findall(r"\d+\.\d+\.\d+", version_line)

        if not match:
            match = re.findall(r"\d+\.\d+", version_line)

        if not match:
            raise OTInterrupt("Cannot find HIP version in file")

        version_numbers = [int(i) for i in match[0].split('.')]

        if (len(version_numbers) > 3) or (len(version_numbers) < 2):
            raise OTInterrupt(
                "Wrong number of digits in mesh version: "
                "{mesh_version}.\n".format(**locals()) +
                "Examples of recognized mesh versions: 1.48, 1.48.1, 16.10.1")

        version_numbers.extend([0] * (3 - len(version_numbers)))
        mesh_version = "{0:02d}.{1:02d}.{2:02d}".format(*version_numbers)

        return mesh_version

    def get_infos(self):
        """ Get infos from the mesh files"""

        def striplist(self):
            """ Remove white spaces in a list """
            return [element.decode('utf-8').strip(' ') for element in self]

        def formatlist(self):
            """ Format the number of a list """
            return ["%.6e" % element for element in self]

        # Check the version of the mesh
        mesh_version = self.get_mesh_version()

        if mesh_version < "17.00.00":
            self.log.warning("The version of the mesh is old, launching latest"
                             " hip to update it")
            self.process_hip()

            # Check again the version of the mesh
            mesh_version = self.get_mesh_version()

            if mesh_version < "17.00.00":
                raise OTInterrupt("Failed at updating the mesh because " +
                                  "your version of hip is too old: " +
                                  str(mesh_version))
        self.log.info("Hip mesh version : %s", mesh_version)

        h5file = h5py.File(self.abspath(self.h5_file), "r")
        try:
            self.listofpatches = h5file["Boundary/PatchLabels"][:]
            self.version = h5file["Parameters/hipversion"][()]
            self.voldomain = h5file["Parameters/vol_domain/"][0]
            self.volelem_min = h5file["Parameters/vol_elem_min/"][0]
            self.volelem_max = h5file["Parameters/vol_elem_max/"][0]
            self.listbndmin = list(h5file["Parameters/x_min/"][:])
            self.listbndmax = list(h5file["Parameters/x_max/"][:])
        except KeyError:
            self.log.error("Unable to access the datasets of the h5 mesh file")
            raise OTException

        self.periodicity = "/Periodicity" in h5file

        try:
            self._hmin = h5file["Parameters/h_min/"][0]
            self._hmax = h5file["Parameters/h_max/"][0]
        except KeyError:
            self.log.warning("Unable to access hmin, hmax datasets in mesh")

        self.listbndmin = formatlist(self.listbndmin)
        self.listbndmax = formatlist(self.listbndmax)
        self.listofpatches = striplist(self.listofpatches)
        self.npatches = len(self.listofpatches)
        self.ndim = len(h5file["Coordinates"])

        if self.ndim == 2:
            self.ndimlist = "x;y"
        elif self.ndim == 3:
            self.ndimlist = "x;y;z"
        else:
            self.log.error("Ndim should be 2 or 3")

        self.nnodes = len(h5file["Coordinates/x"])
        if self.ndim == 2:
            self.ncells = 0
            if "tri->node" in list(h5file["Connectivity"].keys()):
                self.ncells += len(h5file["Connectivity"]["tri->node"])/3
            if "qua->node" in list(h5file["Connectivity"].keys()):
                self.ncells += len(h5file["Connectivity"]["qua->node"])/4
        else:
            self.ncells = 0
            if "tet->node" in list(h5file["Connectivity"].keys()):
                self.ncells += len(h5file["Connectivity"]["tet->node"])/4
            if "pri->node" in list(h5file["Connectivity"].keys()):
                self.ncells += len(h5file["Connectivity"]["pri->node"])/6
            if "hex->node" in list(h5file["Connectivity"].keys()):
                self.ncells += len(h5file["Connectivity"]["hex->node"])/8

        # Patch area list available from hip 16.11
        if "Patch->area" in list(h5file["Boundary"].keys()):
            self.listofsurfaces = list(h5file["Boundary/Patch->area"][:])
        elif "patch_area" in list(h5file["Boundary"].keys()):
            self.listofsurfaces = list(h5file["Boundary/patch_area"][:])
        else:
            self.listofsurfaces = [1] * len(self.listofpatches)
            self.log.warning("The list of patches area is not found in the h5 "
                             "file, use hip 16.11 or newer to process mesh")

        # Cylindrical bounding box list (x axis) available from hip 16.11
        self.listbndmin.append(self.listbndmin[0])
        self.listbndmax.append(self.listbndmax[0])
        try:
            rtheta_min = list(h5file["Parameters/r_min"][:])
            rtheta_max = list(h5file["Parameters/r_max"][:])
            self.listbndmin.extend(formatlist(rtheta_min))
            self.listbndmax.extend(formatlist(rtheta_max))
        except KeyError:
            self.listbndmin.extend((None, None))
            self.listbndmax.extend((None, None))
            self.log.warning("The rtheta bounding box is not found in the h5 "
                             "file, use hip 16.11 or newer to process mesh")

        self.info_mesh_content = "ndim : {0} ({1})\n".format(self.ndim,
                                                             self.ndimlist)
        self.info_mesh_content += "nnodes : " + str(self.nnodes) + "\n"
        self.info_mesh_content += "ncells : " + str(self.ncells) + "\n"
        self.info_mesh_content += "Periodic case = " + str(self.periodicity) \
            + "\n"

        print(
            self)

    @property
    def hmin(self):
        """Smallest edge in mesh"""
        if not self._hmin:
            self._ensure_hmin_hmax()
        return self._hmin

    @property
    def hmax(self):
        """Longest edge in mesh"""
        if not self._hmax:
            self._ensure_hmin_hmax()
        return self._hmax

    def _ensure_hmin_hmax(self):
        h5file = h5py.File(self.h5_file, "r")
        try:
            self._hmin = h5file["Parameters/h_min/"][0]
            self._hmax = h5file["Parameters/h_max/"][0]
            h5file.close()
        except KeyError:
            self.log.warning("Requesting hmin/hmax. "
                             "Launching latest hip to update the mesh.")
            self.process_hip()
            try:
                self._hmin = h5file["Parameters/h_min/"][0]
                self._hmax = h5file["Parameters/h_max/"][0]
                h5file.close()
            except KeyError:
                # Check again the version of the mesh
                mesh_version = self.get_mesh_version()
                if mesh_version < "17.07.04":
                    raise OTInterrupt("hmin/hmax is a feature available only "
                                      "with hip 17.07.4 and later. "
                                      "Your version is: " + str(mesh_version))
                else:
                    self.log.error("hmin/hmax not found.")
                    self.log.error("Hip version: {mesh_version}".format(
                        **locals()))
                    self.log.error("Check if hip ran successfully.")
                    raise OTInterrupt()
