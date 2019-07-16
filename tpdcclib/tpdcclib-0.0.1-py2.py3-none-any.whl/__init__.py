#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for tpDccLib
"""

from __future__ import print_function, division, absolute_import

import os
import inspect

from tpPyUtils import importer
from tpDccLib.abstract import dcc as abstract_dcc, shelf as abstract_shelf, callback as abstract_callback

main = __import__('__main__')

# =================================================================================

logger = None
Dcc = abstract_dcc.AbstractDCC()
Shelf = abstract_shelf.AbstractShelf()
Callback = abstract_callback.AbstractCallback

# =================================================================================


class Callbacks(object):
    SelectionChanged = None


# =================================================================================

class Dccs(object):
    Houdini = 'houdini'
    Maya = 'maya'
    Max = 'max'
    Nuke = 'nuke'

# =================================================================================


class tpDccLib(importer.Importer, object):
    def __init__(self):
        super(tpDccLib, self).__init__(module_name='tpDccLib')

    def get_module_path(self):
        """
        Returns path where tpDccLib module is stored
        :return: str
        """

        try:
            mod_dir = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
        except Exception:
            try:
                mod_dir = os.path.dirname(__file__)
            except Exception:
                try:
                    import tpDccLib
                    mod_dir = tpDccLib.__path__[0]
                except Exception:
                    return None

        return mod_dir


def init(do_reload=False):
    """
    Initializes module
    :param do_reload: bool, Whether to reload modules or not
    """

    dcclib_importer = importer.init_importer(importer_class=tpDccLib, do_reload=do_reload)

    global logger
    logger = dcclib_importer.logger

    dcclib_importer.import_modules()
    dcclib_importer.import_packages(only_packages=True)

    init_dcc(do_reload=do_reload)


def init_dcc(do_reload=False):
    """
    Checks DCC we are working on an initializes proper variables
    """

    if 'cmds' in main.__dict__:
        import tpMayaLib
        tpMayaLib.init(do_reload=do_reload)
    elif 'MaxPlus' in main.__dict__:
        import tpMaxLib
        tpMaxLib.init(do_reload=do_reload)
    elif 'hou' in main.__dict__:
        raise NotImplementedError('Houdini is not a supported DCC yet!')
    elif 'nuke' in main.__dict__:
        raise NotImplementedError('Nuke is not a supported DCC yet!')
    else:
        raise NotImplementedError('Current DCC is not supported yet!')


def is_nuke():
    """
    Checks if Nuke is available or not
    :return: bool
    """

    return Dcc.get_name() == Dccs.Nuke


def is_maya():
    """
    Checks if Maya is available or not
    :return: bool
    """

    return Dcc.get_name() == Dccs.Maya


def is_max():
    """
    Checks if Max is available or not
    :return: bool
    """

    return Dcc.get_name() == Dccs.Max


def is_houdini():
    """
    Checks if Houdini is available or not
    :return: bool
    """

    return Dcc.get_name() == Dccs.Houdini
