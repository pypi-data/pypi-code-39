# -*- coding: utf-8 -*-

import os as _os

# PyGame will suppress output if this environment variable is set.
_ENVIRONMENT_VAR_NAME = "PYGAME_HIDE_SUPPORT_PROMPT"

# Don't interfere if someone has already set it.
_ADD_VAR = _ENVIRONMENT_VAR_NAME not in _os.environ

if _ADD_VAR:
    _os.environ[_ENVIRONMENT_VAR_NAME] = "Added by pygamesilent"

try:
    from pygame import *
except ModuleNotFoundError:
    from warnings import warn as _warn
    _warn("pygamesilent requires pygame to be installed too.")
    raise

try:
    # Pretend to be pygame's version number.
    from pygame import __version__
    # This wasn't imported above, because of the leading underscores.
except ImportError:
    # If some version of pygame doesn't export it, neither will we.
    pass

if _ADD_VAR:
    del _os.environ[_ENVIRONMENT_VAR_NAME]

