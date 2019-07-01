#!/usr/bin/env python
"""Shared classes between the client and the server for plist parsing."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import calendar
import datetime


from future.utils import iteritems

from grr_response_core.lib import lexer
from grr_response_core.lib import objectfilter


class PlistFilterParser(objectfilter.Parser):
  """Plist specific filter parser.

  Because we will be filtering dictionaries and the path components will be
  matched against dictionary keys, we must be more permissive with attribute
  names.

  This parser allows path components to be enclosed in double quotes to allow
  for spaces, dots or even raw hex-escaped data in them, such as:

    "My\x20first\x20path component".2nd."TH.IRD" contains "Google"

  We store the attribute name as a list of paths into the object instead of as
  a simple string that will be chunked in objectfilter.
  """

  tokens = [
      # Operators and related tokens
      lexer.Token("INITIAL", r"\@[\w._0-9]+", "ContextOperator,PushState",
                  "CONTEXTOPEN"),
      lexer.Token("INITIAL", r"[^\s\(\)]", "PushState,PushBack", "ATTRIBUTE"),
      lexer.Token("INITIAL", r"\(", "PushState,BracketOpen", None),
      lexer.Token("INITIAL", r"\)", "BracketClose", "BINARY"),

      # Context
      lexer.Token("CONTEXTOPEN", r"\(", "BracketOpen", "INITIAL"),

      # Double quoted string
      lexer.Token("STRING", "\"", "PopState,StringFinish", None),
      lexer.Token("STRING", r"\\x(..)", "HexEscape", None),
      lexer.Token("STRING", r"\\(.)", "StringEscape", None),
      lexer.Token("STRING", r"[^\\\"]+", "StringInsert", None),

      # Single quoted string
      lexer.Token("SQ_STRING", "'", "PopState,StringFinish", None),
      lexer.Token("SQ_STRING", r"\\x(..)", "HexEscape", None),
      lexer.Token("SQ_STRING", r"\\(.)", "StringEscape", None),
      lexer.Token("SQ_STRING", r"[^\\']+", "StringInsert", None),

      # Basic expression
      lexer.Token("ATTRIBUTE", r"\.", "AddAttributePath", "ATTRIBUTE"),
      lexer.Token("ATTRIBUTE", r"\s+", "AddAttributePath", "OPERATOR"),
      lexer.Token("ATTRIBUTE", "\"", "PushState,StringStart", "STRING"),
      lexer.Token("ATTRIBUTE", r"[\w_0-9\-]+", "StringStart,StringInsert",
                  "ATTRIBUTE"),
      lexer.Token("OPERATOR", r"(\w+|[<>!=]=?)", "StoreOperator", "ARG"),
      lexer.Token("ARG", r"(\d+\.\d+)", "InsertFloatArg", "ARG"),
      lexer.Token("ARG", r"(0x\d+)", "InsertInt16Arg", "ARG"),
      lexer.Token("ARG", r"(\d+)", "InsertIntArg", "ARG"),
      lexer.Token("ARG", "\"", "PushState,StringStart", "STRING"),
      lexer.Token("ARG", "'", "PushState,StringStart", "SQ_STRING"),
      # When the last parameter from arg_list has been pushed

      # State where binary operators are supported (AND, OR)
      lexer.Token("BINARY", r"(?i)(and|or|\&\&|\|\|)", "BinaryOperator",
                  "INITIAL"),
      # - We can also skip spaces
      lexer.Token("BINARY", r"\s+", None, None),
      # - But if it's not "and" or just spaces we have to go back
      lexer.Token("BINARY", ".", "PushBack,PopState", None),

      # Skip whitespace.
      lexer.Token(".", r"\s+", None, None),
  ]

  def StringFinish(self, **_):
    """StringFinish doesn't act on ATTRIBUTEs here."""
    if self.state == "ARG":
      return self.InsertArg(string=self.string)

  def AddAttributePath(self, **_):
    """Adds a path component to the current attribute."""
    attribute_path = self.current_expression.attribute
    if not attribute_path:
      attribute_path = []

    attribute_path.append(self.string)
    self.current_expression.SetAttribute(attribute_path)


class PlistExpander(objectfilter.ValueExpander):
  """A custom expander specific to plists."""

  def _GetValue(self, obj, attr_name):
    try:
      return obj.get(attr_name, None)
    except AttributeError:
      # This is no dictionary... are we a list of dictionaries?
      return [item.get(attr_name, None) for item in obj]

  def _AtNonLeaf(self, attr_value, path):
    """Makes dictionaries expandable when dealing with plists."""
    if isinstance(attr_value, dict):
      for value in self.Expand(attr_value, path[1:]):
        yield value
    else:
      for v in objectfilter.ValueExpander._AtNonLeaf(self, attr_value, path):
        yield v


class PlistFilterImplementation(objectfilter.BaseFilterImplementation):
  FILTERS = {}
  FILTERS.update(objectfilter.BaseFilterImplementation.FILTERS)
  FILTERS.update({"ValueExpander": PlistExpander})


def PlistValueToPlainValue(plist):
  """Takes the plist contents generated by binplist and returns a plain dict.

  binplist uses rich types to express some of the plist types. We need to
  convert them to types that RDFValueArray will be able to transport.

  Args:
    plist: A plist to convert.

  Returns:
    A simple python type.
  """

  if isinstance(plist, dict):
    ret_value = dict()
    for key, value in iteritems(plist):
      ret_value[key] = PlistValueToPlainValue(value)
    return ret_value
  elif isinstance(plist, list):
    return [PlistValueToPlainValue(value) for value in plist]
  elif isinstance(plist, datetime.datetime):
    return (calendar.timegm(plist.utctimetuple()) * 1000000) + plist.microsecond
  return plist
