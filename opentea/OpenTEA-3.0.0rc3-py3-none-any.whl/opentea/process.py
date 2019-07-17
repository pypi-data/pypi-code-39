#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Process.py

TODO

Created Nov 2016 by COOP team
"""



__all__ = ["BaseProcess",
           "CodeProcess",
           "LibProcess"]
#import re
import time
import os
import shutil
import logging
import inspect
import warnings

from os.path import samefile, dirname, realpath
from glob import glob

from opentea.exceptions import OTInterrupt
from opentea.constants import COMMON, RUN_CURRENT
from opentea.dataset import Dataset
from opentea.path_tools import PathTools
from opentea.executor import Executor
from opentea.mesh import Mesh


class BaseProcess(PathTools):
    """Central class of the C3Sm architecture.

    Defines and holds a Dataset instance to manipulate the xml dataset, a
    Plugin instance for tool and code plugins, and holds all generic file
    manipulation functions.
    """
    def __init__(self, dataset_name='dataset.xml', base_dir=None):
        if base_dir is not None:
            warnings.warn("The use of base_dir is deprecated from version 2.2."
                          " Instead, the directory of dataset_name is used."
                          " See issue #42", DeprecationWarning)
        else:
            base_dir = dirname(realpath(dataset_name))
        PathTools.__init__(self, base_dir)
        self.ds = Dataset(dataset_name)
        self.start_dir = os.getcwd()
        self.mesh = None
        self.exto = None
        self.timestamp = None
        self.verbose = None
        self.script_dir = None
        self.original_application_name = None
        self.project_name = None
        self.executors = {}
        self.debug = (int(self.ds.getValue("debug", "meta")) == 1)
        self.log = logging.getLogger(__name__)
        self._init_defs_base()

    def _init_defs_base(self):
        """Initialize 'global' attributes used everywhere downstream"""
        self.timestamp = time.time()
        self.verbose = 0

        PathTools.__init__(self,
                           base_dir=self.base_dir)
        # Path to the current process script directory
        self.script_dir = dirname(inspect.getfile(self.__class__))

        self.original_application_name = self.ds.getValue("name", "solver",
                                                          "meta")
        self.project_name = self.ds.getValue("name", "project", "meta")

        if self.original_application_name == "none":
            self.log.warning("OpenTEA unable to find the origin application")

        self.COMMON = COMMON
        self.ensure_dir(self.abspath(COMMON))

        self.log.info("Instance of {} created".format(__name__))
        self.log.info("Use of OpenTEA for project {0} ({1})".format(
            self.project_name, self.original_application_name))

    def finish(self):
        """Close the OpenTEA environment.

        This procedure saves the output XML file and changes the directory to
        the initial one.  Must be called at the end of every script using
        OpenTEA.
        """
        if not samefile(self.start_dir, os.getcwd()):
            os.chdir(self.start_dir)
            self.log.warning("Didn't finish in starting dir.")
            self.log.warning("This is not a healthy behavior")
        self.ds.save2file(self.abspath("out_dataset.xml"))

    def loadmesh(self, filename):
        """Load a mesh"""
        self.mesh = Mesh(filename, self)
        self.mesh.get_infos()
        return self.mesh

    def get_executor(self, action, add_dirs=None, options=""):
        """Open an execution environment"""
        self.executors[action] = Executor(self, action, add_dirs=add_dirs,
                                          options=options)
        return self.executors[action]

    def progress(self, progr_frac, text):
        """ give a visual cue on progress
        progr_frac is a real btw 0 and 1
        text is the text to show

        return a log starting with a pct
        complying with regexp ^\ {0,2}\d{1,3}%.*$
        for progress bar features in opentea...
        """
        progr_frac = min(progr_frac, 1)
        progr_frac = max(progr_frac, 0)

        pct_cue = '{num:3d}%'.format(num=int(progr_frac*100))
        info_cue = pct_cue + " " + text

        # pattern = re.compile("^\ {0,2}\d{1,3}%.*$")
        # if pattern.match(info_cue):
        #     print "OK |", info_cue
        # else:
        #     print "XX |", info_cue

        self.log.info(info_cue)
        time.sleep(0.1) # small pause to see changes in the GUI
        return info_cue

class CodeProcess(BaseProcess):
    """Process class for applications surrounding a code setup and execution

    Specificities:
        - a RUN_CURRENT directory is filled progressively with all inputs
        - files that can be shared between runs are kept in
          COMMON/original_application_name
        - a call to self.write_case() simply performs a copy of RUN_CURRENT
          as RUN_XXX, where XXX is incremented from 1 for each run. RUN_CURRENT
          should be fully ready to run at that time.
    """
    def __init__(self, dataset_name, base_dir=None):
        BaseProcess.__init__(self, dataset_name, base_dir)
        self.this_run = None
        self.next_run = None
        self._init_defs_code()

    def _init_defs_code(self):
        """Initialize 'global' attributes used everywhere downstream"""
        self.ensure_dir(self.abspath(RUN_CURRENT))
        # In CodeProcess, paths are considered from inside RUN_CURRENT
        self.rel_dir = RUN_CURRENT
        self._update_run_dirs()

    def _update_run_dirs(self):
        """Detect run numbers (current, next) from RUN_00X directories"""
        def run_nb():
            """Return last run nb from list of RUN_??? dirs"""
            runs = sorted(glob(self.abspath('RUN_???')))
            if runs:
                return int(runs[-1].split('_')[-1])
            return 0
        self.this_run = (None if run_nb() == 0
                         else "RUN_{:03d}".format(run_nb()))
        self.next_run = "RUN_{:03d}".format(run_nb() + 1)
        self.log.debug("Current run: {0}. Next run: {1}".format(self.this_run,
                                                                self.next_run))

    def write_case(self):
        """Copy full contents of RUN_CURRENT in next RUN_XXX"""
        self._update_run_dirs()
        src = self.abspath(RUN_CURRENT)
        dest = self.abspath(self.next_run)
        self.log.debug("Copying {0} to {1}".format(src, dest))
        shutil.copytree(src, dest)
        self.ds.save2file(self.abspath(self.next_run, self.next_run + '.xml'))
        self._update_run_dirs()


class LibProcess(BaseProcess):
    """Process class for applications surrounding a library application

    Specificities:
        - libobjs attribute contains names of library objects
        - naive methods for manipulation of libobj are provided. Then should be
          overwritten if more complex object manipulation is needed
        - 2 lists are expected in XML:
           - list_libobjs_in_project: contains exactly self.libobjs
           - list_written_libobjs: subset of list_libobjs_in_project that have
             actually been written to disc
    """
    def __init__(self, dataset_name):
        BaseProcess.__init__(self, dataset_name)
        self.log = logging.getLogger(__name__)
        self.update_libobjs()

    def update_libobjs(self):
        """Update multiple containing libobjects

        All files present should be accounted for in mul_libobjs.
        Any libobj in mul_libobjs not present as an actual file on disk is
        not yet written.  It must stay in the multiple, but with details empty.
        """
        files = glob(self.libobj_file('*'))
        self.log.debug('Found following libobj files: ' + repr(files))
        self.libobjs = [self.libobj_name(path) for path in files]
        self.ds.setValue(";".join(self.libobjs), "list_written_libobjs")
        for obj in self.libobjs:
            self.ds.addToUniqList(obj, "list_libobjs_in_project")
        self.unwritten_libobjs = [
            f for f in self.ds.getListValue("list_libobjs_in_project")
            if f not in self.ds.getListValue("list_written_libobjs")]
        self.log.debug("Unwritten libobjs in xml: "
                       + repr(self.unwritten_libobjs))
        # rebuild = (set(self.libobjs + self.unwritten_libobjs) !=
        #           set([self.ds.getValue(node)
        #                for node in self.ds.getChildrenName("mul_libobjs")]))
        # if rebuild:
        self.log.debug("Rebuilding multiple containing libobjects")
        self.ds.removeNode("mul_libobjs")
        self.ds.addChild("mul_libobjs", "", "flame_library")
        self.write_metas()

    def libobj_file(self, name):
        """Get path to libobj using its name"""
        raise NotImplementedError("Implement libobj_file according to app")

    def libobj_name(self, path):
        """Get name of libobj using its path"""
        raise NotImplementedError("Implement libobj_name according to app")

    def write_metas(self):
        """Fill mul_libobjs"""
        raise NotImplementedError("Implement metas to display for libobject")

    def add_libobj(self, *names):
        """Add library object(s)"""
        for name in names:
            if name in self.libobjs + self.unwritten_libobjs:
                raise OTInterrupt("Object {} already exists".format(name))
            self.ds.addToUniqList(name, "list_libobjs_in_project")
        self.update_libobjs()

    def rename_libobj(self, src_name, dest_name):
        """Rename one of the currently declared objects"""
        if src_name not in self.libobjs + self.unwritten_libobjs:
            raise OTInterrupt("No object {} exists, cannot "
                              "rename".format(src_name))
        self._rename(src_name, dest_name)
        self.add_libobj(dest_name)
        self.del_libobj(src_name)

    def _rename(self, src_name, dest_name):
        """Specific implementation of object renaming"""
        self.move_file(self.libobj_file(src_name), self.libobj_file(dest_name))

    def import_libobj(self, path):
        """Specific implementation of object importing"""
        raise NotImplementedError("Implement import_libobj")

    def duplicate_libobj(self, name):
        """Specific implementation of object duplication"""
        raise NotImplementedError("Implement duplicate_libobj")

    def del_libobj(self, name):
        """Delete object `name`"""
        if name in self.libobjs:
            self.log.warning("Deleting libobj file " + self.libobj_file(name))
            self.libobjs.remove(name)
            os.remove(self.libobj_file(name))
            libobj_list = self.ds.getListValue("list_written_libobjs")
            libobj_list.remove(name)
            self.ds.setValue(";".join(libobj_list), "list_written_libobjs")
        elif name in self.unwritten_libobjs:
            self.log.info("Forgetting unwritten libobj " + name)
        else:
            self.log.warning(name + " is not a known libobj. "
                             "Nothing to delete.")
            return
        libobj_list = self.ds.getListValue("list_libobjs_in_project")
        libobj_list.remove(name)
        self.ds.setValue(";".join(libobj_list), "list_libobjs_in_project")
        for child in sorted(self.ds.getChildrenName("mul_libobjs")):
            if self.ds.getValue(child) == name:
                self.ds.removeNode(child)
