#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
"""Make sure from docx2python import ... works

:author: Shay Hill
:created: 7/17/2019

"""

from docx2python import get_docx_content

def test() -> None:
    """Just making sure the import works."""
    get_docx_content('resources/example.docx')