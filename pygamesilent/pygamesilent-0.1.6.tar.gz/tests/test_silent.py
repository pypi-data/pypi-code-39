# -*- coding: utf-8 -*-

try:
    from io import StringIO
except:
    # Python 2.
    from cStringIO import StringIO
import sys

import pytest


def test_import_is_silentp():
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    import pygamesilent

    sys.stdout = old_stdout

    assert len(mystdout.getvalue()) == 0, \
        "Unexpected output: %s" % mystdout.getvalue()
