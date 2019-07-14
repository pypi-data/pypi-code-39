# Generated from /home/omry/dev/antelope/python/grammar/YAML.g4 by ANTLR 4.7.2
# encoding: utf-8
from __future__ import print_function
from antlr4 import *
from io import StringIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write(u"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2")
        buf.write(u"\7\37\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2")
        buf.write(u"\3\2\3\3\3\3\3\4\3\4\3\5\6\5\25\n\5\r\5\16\5\26\3\6\6")
        buf.write(u"\6\32\n\6\r\6\16\6\33\3\6\3\6\2\2\7\3\3\5\4\7\5\t\6\13")
        buf.write(u"\7\3\2\4\3\2\62;\5\2\13\f\17\17\"\"\2 \2\3\3\2\2\2\2")
        buf.write(u"\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\3\r\3")
        buf.write(u"\2\2\2\5\17\3\2\2\2\7\21\3\2\2\2\t\24\3\2\2\2\13\31\3")
        buf.write(u"\2\2\2\r\16\7}\2\2\16\4\3\2\2\2\17\20\7.\2\2\20\6\3\2")
        buf.write(u"\2\2\21\22\7\177\2\2\22\b\3\2\2\2\23\25\t\2\2\2\24\23")
        buf.write(u"\3\2\2\2\25\26\3\2\2\2\26\24\3\2\2\2\26\27\3\2\2\2\27")
        buf.write(u"\n\3\2\2\2\30\32\t\3\2\2\31\30\3\2\2\2\32\33\3\2\2\2")
        buf.write(u"\33\31\3\2\2\2\33\34\3\2\2\2\34\35\3\2\2\2\35\36\b\6")
        buf.write(u"\2\2\36\f\3\2\2\2\5\2\26\33\3\b\2\2")
        return buf.getvalue()


class YAMLLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    INT = 4
    WS = 5

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ u"DEFAULT_MODE" ]

    literalNames = [ u"<INVALID>",
            u"'{'", u"','", u"'}'" ]

    symbolicNames = [ u"<INVALID>",
            u"INT", u"WS" ]

    ruleNames = [ u"T__0", u"T__1", u"T__2", u"INT", u"WS" ]

    grammarFileName = u"YAML.g4"

    def __init__(self, input=None, output=sys.stdout):
        super(YAMLLexer, self).__init__(input, output=output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


