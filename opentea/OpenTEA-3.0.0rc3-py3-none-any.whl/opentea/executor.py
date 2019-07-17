#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""executor.py
           .            .                     .
                  _        .                          .            (
                 (_)        .       .                                     .
  .        ____.--^.
   .      /:  /    |                               +           .         .
         /:  `--=--'   .                                                .
        /: __[\==`-.___          *           .
       /__|\ _~~~~~~   ~~--..__            .             .
       \   \|::::|-----.....___|~--.                                 .
        \ _\_~~~~~-----:|:::______//---...___
    .   [\  \  __  --     \       ~  \_      ~~~===------==-...____
        [============================================================- PEW PEW
        /         __/__   --  /__    --       /____....----''''~~~~      .
  *    /  /   ==           ____....=---='''~~~~ .
      /____....--=-''':~~~~                      .                .
      .       ~--~
                     .                                   .           .
                          .                      .             +

    "With the Executor under my command, I will be the ultimate power in the
    universe!"

    -Admiral Kendal Ozzel, mere moments before his death at the hand of Darth
    Vader

Created Nov 2016 by COOP team
"""



__all__ = ["Executor"]

import imp
import logging
from os.path import join
from .constants import TEMP
from . import PathTools, OTTooManyNodesException


class Executor(PathTools):
    """Execute any tool or code according to plugins.

    Tool strategy: Populate local TEMP with tool inputs, run (distantly if
    needed) and retrieve.
    """
    def __init__(self, process, action, add_dirs=None, options="", **kwargs):
        """ startup of Executor
        note that _init() will recall Pathtools.__init__() in all cases"""
        PathTools.__init__(self, base_dir=process.base_dir)
        self.dataset = process.ds
        self.action = action
        self.add_dirs = add_dirs if add_dirs else []
        self.debug = process.debug
        self.options = options
        self.log = logging.getLogger(__name__)
        self.stdout = None
        self.plugin = None
        self._inits(process)
        self.__dict__.update(kwargs)

    def _inits(self, process):
        """Perform initializations. Switch between code and tool execution."""
        if self.action == "-code_exe-":  # Code execution
            self.execute_dir = process.this_run
            PathTools.__init__(self, process.base_dir,
                               rel_dir=self.abspath(process.base_dir,
                                                    self.execute_dir))
            self.load_code_plugin()
            self.appli = self.dataset.getValue("codeversion")
            self.add_dirs.extend([process.COMMON, process.this_run])
            self.retrieve = False
        else:                            # Tool execution
            self.execute_dir = TEMP + "_" + self.action
            PathTools.__init__(self, process.base_dir,
                               rel_dir=self.abspath(process.base_dir,
                                                    self.execute_dir))
            self.load_tool_plugin()
            self.appli = self.dataset.getValue("toolversion")
            self.add_dirs.append(self.abspath(self.execute_dir))
            self.retrieve = True

        # Ensure the execute_dir (TEMP_action) is available
        # and clean, and prepare for executions
        self.abs_execute_dir = process.abspath(self.execute_dir)
        self.ensure_dir(self.abs_execute_dir)
        self._setup_distant_bundle()

    def _setup_distant_bundle(self):
        """Strange old hack to make subscripts work in `distant` execution

        Since the scripts execution on a distant platform do not necessarily
        have access to the OpenTEA library, it is systematically shipped to the
        TEMP_* directory.

        This is a strange hack with several flaws:
          - only part of the opentea library is copied, so there is no
          assurance of what will be available
          - the distanttools.py reimplements execution wrapping, even though it
          is already fully implemented in plugin.py based on subprocess
          - this is always performed, even for all cases were it is
          unneccessary (*e.g.* local execution)
        """
        _, opentea_dir_path, _ = imp.find_module('opentea')
        distanttools_dir_path = join(opentea_dir_path, 'distant_bundle')
        self.copy_dir(distanttools_dir_path, self.execute_dir + '/')

        # Copy what we need from opentea, dataset and pathtools
        for filename in ['constants.py', 'exceptions.py',
                         'dataset.py', 'path_tools.py']:
            self.copy_file(join(opentea_dir_path, filename),
                           join(self.execute_dir, 'distant_bundle/'))

    def copy_file_temp(self, src, dest=None):
        """Wrapper for the most used form of copy_file call"""
        destination = self.execute_dir
        if dest:
            destination = join(destination, dest)
        self.copy_file(src, destination)

    def load_code_plugin(self, name=None):
        """Load the code plugin"""
        if name is None:
            try:
                name = self.dataset.getValue("code_plugins")
            except OTTooManyNodesException:
                name = self.dataset.getValue("code_plugins",
                                             self.dataset.getValue("name",
                                                                   "solver",
                                                                   "meta"))
        plugin_class = self._load_plugin(name)
        self.plugin = plugin_class(self.dataset, self.base_dir, 'code')

    def load_tool_plugin(self):
        """Load the tool plugin"""
        self.log.debug("Loading the tool plugin")
        name = self.dataset.getValue("tool_plugins", "config")
        plugin_class = self._load_plugin(name)
        self.plugin = plugin_class(self.dataset, self.base_dir, 'tool')

    def _load_plugin(self, name):
        """Load plugin 'name'"""
        plugin_path = join(self.dataset.getValue("pluginsPath",
                                                 "engine", "meta"),
                           "scripts",
                           name + '.py')
        self.log.debug("Loading plugin {0} at path {1} "
                       .format(name, plugin_path))
        plugin_lib = imp.load_source(name, plugin_path)
        plugin_class = getattr(plugin_lib, name)
        return plugin_class

    def execute(self):
        """Execute the tool or code"""
        self.dataset.save2file(self.abspath(self.execute_dir, 'dataset.xml'))
        self.log.info('Executing action :' + self.action)
        self.log.debug('Params : action: {0.action} '
                       '- execute_dir: {0.execute_dir} - '
                       'additional dirs: {0.add_dirs}'.format(self))
        self.stdout = self.plugin.execute_action(self.action, self.execute_dir,
                                                 self.appli, self.add_dirs,
                                                 retrieve=self.retrieve,
                                                 options=self.options)
        self.log.debug('... End of execution ')
        return self.stdout

    def finish(self, clean=True):
        """Kept for backwards compatibility"""
        clean = " and cleaning" if clean else ""
        self.log.debug('Finishing executor ' + str(self.action) + clean)

    def check_execution(self):
        """Backwards compatibility function"""
        pass
