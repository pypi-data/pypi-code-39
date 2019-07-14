import token
import tokenize
from io import StringIO

"""
The expression:
    content_type = 'BlogPost' and date

becomes:

    getattr(page, 'content_type', None) == 'BlogPost' and getattr(page, 'date', None)
"""

def parse(src):
    tokens = tokenize.generate_tokens(StringIO(src).readline)

    state = []

    for token in tokens:
        if token.exact_type == token.NAME:
            node = {
                'and': And,
                'or': Or,
                'all': All,
                'any': Any,
                ''
            }.get(token.string, None)
            if token.string == 'and':
            elif token.string == 'or':
            elif token.string == 'any':
            elif
            state.push(Attr(token.string))
        elif token.type == token.OP:


    return tokens
