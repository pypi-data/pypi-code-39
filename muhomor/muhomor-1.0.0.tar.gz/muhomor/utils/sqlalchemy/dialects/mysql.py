from sqlalchemy.dialects.mysql import TINYBLOB
from sqlalchemy import func


class TINYBLOB_ENCODED(TINYBLOB):
    """MySQL TINYBLOB type, for binary data up encoded using ENCODE() func."""

    def __init__(self, secret: str, length: int = None):
        TINYBLOB.__init__(self, length=length)
        self.secret = secret

    def bind_expression(self, bindvalue):
        return func.ENCODE(bindvalue, self.secret)

    def column_expression(self, col):
        return func.DECODE(col, self.secret)

