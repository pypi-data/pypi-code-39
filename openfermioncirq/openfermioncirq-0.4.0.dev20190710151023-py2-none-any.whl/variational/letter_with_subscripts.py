# coding=utf-8
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from __future__ import absolute_import
from typing import Union, List

import sympy


def _name(letter, *subscripts):
    return letter + u''.join(u'_{}'.format(subscript)
                            for subscript in subscripts)


class LetterWithSubscripts(sympy.Symbol):

    def __new__(cls, letter, *subscripts):
        return super(LetterWithSubscripts, cls).__new__(cls, _name(letter, *subscripts))

    def __init__(self,
                 letter,
                 *subscripts):
        self.letter = letter
        self.subscripts = subscripts
        super(LetterWithSubscripts, self).__init__()

    def __eq__(self, other):
        if not isinstance(other, sympy.Symbol):
            return NotImplemented
        return unicode(self) == unicode(other)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(sympy.Symbol(unicode(self)))

    def __repr__(self):
        return (
            u'ofc.variational.letter_with_subscripts.'
            u'LetterWithSubscripts({!r}, {})'.format(
                self.letter,
                u', '.join(unicode(e) for e in self.subscripts)))

    def _subs(self, old, new, **hints):
        # HACK: work around sympy not recognizing child classes as symbols.
        if old == self:
            return new
        return super(LetterWithSubscripts, self)._subs(old, new, **hints)
