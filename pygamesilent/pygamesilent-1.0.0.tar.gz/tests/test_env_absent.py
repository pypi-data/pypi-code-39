# -*- coding: utf-8 -*-

import os

import pytest

def test_env_absent():
    # Even if the env var is not initially set, the environ
    # variables should not be affected.
    assert "PYGAME_HIDE_SUPPORT_PROMPT" not in os.environ
    import pygamesilent
    assert "PYGAME_HIDE_SUPPORT_PROMPT" not in os.environ
