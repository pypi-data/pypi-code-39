# -*- coding: utf-8 -*-
import pprint
import os

import pytest

def test_env_absent():
    # If the env var is already set, the environ
    # variables should not be affected.
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "Set by test"
    original_vars = dict(os.environ)

    import pygamesilent

    assert dict(os.environ) == original_vars
