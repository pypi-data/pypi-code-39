# -*- coding: utf-8 -*-

from pprint import pprint
import pytest

def test_exports():
    # Modules should export identical names.

    import pygamesilent
    import pygame

    # Check an arbitrary export is the same.
    assert pygame.draw == pygamesilent.draw

    # Check version numbers match.
    assert pygamesilent.__version__ == pygame.__version__

    # Check list of exports match:
    pygame_exports = set(
        entry for entry in dir(pygame) if not entry.startswith("_"))
    pygamesilent_exports = set(
        entry for entry in dir(pygamesilent) if not entry.startswith("_"))

    assert pygame_exports == pygamesilent_exports


