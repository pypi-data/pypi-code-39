"""
Babel extractor for Red.

Main entry point is the ``extract_red()`` function.
"""
import sys
from token import COMMENT, INDENT, NAME, NEWLINE, NL, OP, STRING
from tokenize import tokenize
from typing import (
    Any,
    BinaryIO,
    Callable,
    Collection,
    Container,
    Iterator,
    List,
    Mapping,
    Optional,
    Tuple,
)

try:
    from babel.util import parse_encoding, parse_future_flags
except ModuleNotFoundError:
    parse_encoding = lambda *a: "UTF-8"
    parse_future_flags = lambda *a: 0

__version__ = "0.1.0"

_MessageEntry = Tuple[int, str, str, List[str]]


def extract_red(
    fileobj: BinaryIO,
    keywords: Container[str],
    comment_tags: Collection[str],
    options: Mapping[str, Any],
) -> Iterator[_MessageEntry]:
    encoding = parse_encoding(fileobj) or options.get("encoding", "UTF-8")
    eater = TokenEater(
        keywords=keywords,
        comment_tags=comment_tags,
        future_flags=parse_future_flags(fileobj, encoding),
        filename=getattr(fileobj, "name", None),
    )
    for ttype, string, (lineno, _), _, _ in tokenize(fileobj.readline):
        entry = eater(ttype, string, lineno)
        if entry is not None:
            yield entry


class TokenEater:
    def __init__(
        self,
        keywords: Container[str],
        comment_tags: Collection[str] = frozenset(),
        future_flags: int = 0,
        filename: Optional[str] = None,
    ):
        self.__state: Callable[
            [int, str, int], Optional[_MessageEntry]
        ] = self.__waiting
        self.__buf: List[str] = []
        self.__enclosure_count: int = 0
        self.__keywords: Container[str] = keywords
        self.__future_flags: int = future_flags
        self.__cur_funcname: Optional[str] = None
        self.__translator_comments: List[Tuple[int, str]] = []
        self.__messages: List[Optional[str]] = []
        self.__message_lineno: Optional[int] = None
        self.__filename: str = filename or "unknown file"
        self.__comment_tags: Collection[str] = comment_tags
        self.__docstring_type: Optional[str] = None
        self.__after_def: bool = False

    def __call__(self, ttype: int, string: str, lineno: int) -> Optional[_MessageEntry]:
        return self.__state(ttype, string, lineno)

    def __waiting(self, ttype: int, string: str, lineno: int) -> None:
        # cog or command docstring?
        if ttype == OP and string == "@":
            self.__state = self.__decorator_seen
            return
        elif ttype == NAME and string == "class":
            self.__after_def = True
            self.__state = self.__class_seen
            return
        elif ttype == COMMENT:
            self.__translator_comments.clear()
            value = string[1:].strip()
            if value.startswith(tuple(self.__comment_tags)):
                self.__translator_comments.append((lineno, value))
                self.__state = self.__translator_comment_seen
        if ttype == NAME and string in self.__keywords:
            self.__cur_funcname = string
            self.__state = self.__keyword_seen

    def __translator_comment_seen(self, ttype: int, string: str, lineno: int) -> None:
        if ttype == COMMENT:
            value = string[1:].strip()
            self.__translator_comments.append((lineno, value))
        elif ttype != NL:
            self.__state = self.__waiting
            self.__state(ttype, string, lineno)

    # noinspection PyUnusedLocal
    def __decorator_seen(self, ttype: int, string: str, lineno: int) -> None:
        # Look for the @command(), @group() or @cog_i18n() decorators
        if ttype == NAME and string in ("command", "group", "cog_i18n"):
            if string == "cog_i18n":
                self.__docstring_type = "cog"
            else:
                self.__docstring_type = "command"
            self.__state = self.__suite_seen
        elif ttype == NEWLINE:
            self.__state = self.__waiting

    # noinspection PyUnusedLocal
    def __class_seen(self, ttype: int, string: str, lineno: int) -> None:
        # Look for the `Cog` base class
        if self.__enclosure_count == 1:
            if (ttype == NAME and string == "Cog") or (
                ttype == STRING and string in ('"Cog"', "'Cog'")
            ):
                self.__docstring_type = "cog"
                self.__state = self.__suite_seen
                return
        elif self.__after_def and ttype == NAME:
            # This is the cog name
            self.__cur_funcname = string
            self.__after_def = False
        if ttype == OP:
            if string == ":" and self.__enclosure_count == 0:
                # we see a colon and we're not in an enclosure: end of def/class
                self.__state = self.__waiting
            elif string in "([{":
                self.__enclosure_count += 1
            elif string in ")]}":
                self.__enclosure_count -= 1

    # noinspection PyUnusedLocal
    def __suite_seen(self, ttype: int, string: str, lineno: int) -> None:
        if ttype == NAME and string in ("class", "def"):
            self.__after_def = True
        elif ttype == NAME and self.__after_def:
            # This is the command name
            self.__cur_funcname = string
            self.__after_def = False
        elif ttype == OP:
            if string == ":" and self.__enclosure_count == 0:
                # we see a colon and we're not in an enclosure: end of def/class
                self.__state = self.__suite_docstring
            elif string in "([{":
                self.__enclosure_count += 1
            elif string in ")]}":
                self.__enclosure_count -= 1

    def __suite_docstring(
        self, ttype: int, string: str, lineno: int
    ) -> Optional[_MessageEntry]:
        if ttype == STRING and _is_literal_string(string):
            self.__state = self.__waiting
            return (
                lineno,
                "",
                _safe_eval(string),
                [
                    f"This is a help string for the {self.__docstring_type} "
                    f'"{self.__cur_funcname}".'
                ],
            )
        elif ttype not in (NEWLINE, INDENT, COMMENT):
            # there was no class docstring
            self.__state = self.__waiting

    def __keyword_seen(self, ttype: int, string: str, lineno: int) -> None:
        if ttype == OP and string == "(":
            self.__message_lineno = lineno
            self.__state = self.__open_seen
        else:
            self.__cur_funcname = None
            self.__state = self.__waiting

    # noinspection PyUnusedLocal
    def __open_seen(
        self, ttype: int, string: str, lineno: int
    ) -> Optional[_MessageEntry]:
        nested = ttype == NAME and string in self.__keywords
        if (ttype == OP and string == ")") or nested:
            # We've seen the last of the translatable strings.  Record the
            # line number of the first line of the strings and update the list
            # of messages seen.  Reset state for the next batch.  If there
            # were no strings inside _(), then just ignore this entry.
            if self.__buf:
                self.__messages.append("".join(self.__buf))
                self.__buf.clear()
            else:
                self.__messages.append(None)

            if len(self.__messages) > 1:
                messages = tuple(self.__messages)
            else:
                messages = self.__messages[0]

            if (
                self.__translator_comments
                and self.__translator_comments[-1][0] < self.__message_lineno - 1
            ):
                translator_comments = []
            else:
                translator_comments = self.__translator_comments.copy()

            self.__messages.clear()
            self.__translator_comments.clear()
            funcname = self.__cur_funcname
            if nested:
                self.__cur_funcname = string
                self.__state = self.__keyword_seen
            else:
                self.__state = self.__waiting

            return (
                self.__message_lineno,
                funcname,
                messages,
                [comment for lineno, comment in translator_comments],
            )
        elif ttype == STRING and _is_literal_string(string):
            self.__buf.append(_safe_eval(string))
        elif ttype == OP and string == ",":
            if self.__buf:
                self.__messages.append("".join(self.__buf))
                self.__buf.clear()
            else:
                self.__messages.append(None)
        elif self.__cur_funcname == "_" and ttype not in (COMMENT, NL):
            # warn if we see anything else other than STRING or whitespace
            print(
                f'*** {self.__filename}:{lineno}: Seen unexpected token "{string}"',
                file=sys.stderr,
            )
            self.__messages.clear()
            self.__buf.clear()
            self.__state = self.__waiting


# We only want to extract string literals which aren't f-strings.
# https://docs.python.org/3.7/reference/lexical_analysis.html#string-and-bytes-literals
ALLOWED_STRING_PREFIXES = {"r", "u", "R", "U"}


def _is_literal_string(string: str) -> bool:
    quote_pos = string.find("'")
    if quote_pos < 0:
        quote_pos = string.find('"')
        if quote_pos < 0:
            return False
    prefix = string[:quote_pos]
    return not prefix or prefix in ALLOWED_STRING_PREFIXES


def _safe_eval(string: str, encoding: str = "UTF-8", future_flags: int = 0) -> str:
    code = compile(
        "# coding=%s\n%s" % (str(encoding), string), "<string>", "eval", future_flags
    )
    return eval(code, {"__builtins__": {}}, {})
