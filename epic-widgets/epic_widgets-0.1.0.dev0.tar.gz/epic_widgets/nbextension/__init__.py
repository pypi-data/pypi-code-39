#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Dmitry Romanov
# Distributed under the terms of the Modified BSD License.

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'nbextension/static',
        'dest': 'epic_widgets',
        'require': 'epic_widgets/extension'
    }]
