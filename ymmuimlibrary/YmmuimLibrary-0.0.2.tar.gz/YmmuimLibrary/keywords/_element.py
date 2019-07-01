# -*- coding: utf-8 -*-

from YmmuimLibrary.action.actioner import Actioner
from .keywordgroup import KeywordGroup
from robot.libraries.BuiltIn import BuiltIn
import ast
from unicodedata import normalize

try:
    basestring  # attempt to evaluate basestring


    def isstr(s):
        return isinstance(s, basestring)
except NameError:
    def isstr(s):
        return isinstance(s, str)

class _YmmiumKeywords(KeywordGroup):
    def __init__(self):
        self._element_actioner = Actioner()
        self._bi = BuiltIn()

    # Public, element lookups
    def click_element(self, name):
        """ Click element identified by `locator`. """
        self._click_action(name)

    # private
    def _click_action(self, name):
        try:
            print(name)
        except Exception as e:
            raise 'Cannot click the element with name "%s"' % name