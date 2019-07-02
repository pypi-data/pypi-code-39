from functools import wraps

from teradataml.common.utils import UtilFuncs

from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes

from sqlalchemy import func, literal
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression

from .sql import _SQLColumnExpression
from .sql_interfaces import ColumnExpression

from teradatasqlalchemy.dialect import preparer, dialect as td_dialect
from teradatasqlalchemy import (CHAR, VARCHAR, CLOB, NUMBER)

__all__ = ['translate', 'to_numeric']

def _as_varchar_literal(arg):
    """
    return a sqlalchemy literal

    Parameters
    ---------
    arg: string literal

    """
    return literal(arg, type_ = VARCHAR(len(arg)))

# TODO: refactor this once more functions are created
#def _implementation(fn):
#
#  """
#    This decorator wraps sql functions that generate expressions
#    that can be used in DataFrame and Series methods such as assign.
#
#    The wrapper performs error checks as well as implements
#    the kind of ColumnExpression instance to return
#
#    Parameters
#    ----------
#      A function or method that generates sql.
#      The function is from the sql_functions module.
#
#    Examples
#    --------
#      @implementation
#      def unicode_to_latin(x)
#
#  """
#  @wraps
#  def inner(*args, **kw):
#
#      res = fn(*args, **kw)
#      return _SQLColumnExpression(res)
#
#
#@_implementation

def translate(x, source = 'UNICODE', target = 'LATIN'):
    """
    Returns a TRANSLATE(x USING source_TO_target) expression

    PARAMETERS:
      x: A ColumnExpression instance coming from the DataFrame
         or output of other functions in sql_functions. A python
         string literal may also be used.

      source, target: str with values:
        - 'UNICODE'
        - 'LATIN'

    REFERENCES:
      Chapter 28: String Operators and Functions
      Teradata® Database SQL Functions, Operators, Expressions, and
      Predicates, Release 16.20

    EXAMPLES:
      >>> from teradataml.dataframe.sql_functions import translate

      >>> df = DataFrame('df')
      >>> tvshow = df['tvshow']

      >>> res = df.assign(tvshow = translate(tvshow))
    """

    # error checking
    if not isinstance(x, str) and not isinstance(x, ColumnExpression):
      msg = Messages.get_message(MessageCodes.TDMLDF_UNKNOWN_TYPE).format('x', "a DataFrame column or string")
      raise TeradataMlException(msg, MessageCodes.TDMLDF_UNKNOWN_TYPE)

    if not isinstance(source, str):
      msg = Messages.get_message(MessageCodes.TDMLDF_UNKNOWN_TYPE).format('source', "a string")
      raise TeradataMlException(msg, MessageCodes.TDMLDF_UNKNOWN_TYPE)

    if not isinstance(target, str):
      msg = Messages.get_message(MessageCodes.TDMLDF_UNKNOWN_TYPE).format('target', "a string")
      raise TeradataMlException(msg, MessageCodes.TDMLDF_UNKNOWN_TYPE)

    supported = ('UNICODE', 'LATIN')
    if (source.upper() not in supported):
      msg = Messages.get_message(MessageCodes.INVALID_ARG_VALUE).format(source.upper(), 'source', "in {}".format(supported))
      raise TeradataMlException(msg, MessageCodes.INVALID_ARG_VALUE)

    if (target.upper() not in supported):
      msg = Messages.get_message(MessageCodes.INVALID_ARG_VALUE).format(target.upper(), 'target', "in {}".format(supported))
      raise TeradataMlException(msg, MessageCodes.INVALID_ARG_VALUE)

    # get the sqlalchemy expression
    expr = None
    if isinstance(x, ColumnExpression):
      expr = x.expression

    else:
      expr = literal(x, type_ = VARCHAR(length = len(x), charset = 'UNICODE'))

    if not isinstance(expr.type, (CHAR, VARCHAR, CLOB)):
      msg = Messages.get_message(MessageCodes.TDMLDF_UNKNOWN_TYPE).format('x', "a DataFrame column of type CHAR, VARCHAR, or CLOB")
      raise TeradataMlException(msg, MessageCodes.TDMLDF_UNKNOWN_TYPE)

    # get the result type
    length, charset = expr.type.length, target
    typ_ = CLOB(length, charset) if isinstance(expr.type, CLOB) else VARCHAR(length, charset)

    # define an inner class to generate the sql expression
    class _translate(expression.FunctionElement):
        name = '_translate'
        type = typ_

    custom = source + '_TO_' + target
    @compiles(_translate)
    def default__translate(element, compiler, **kw):
        column_expression = compiler.process(element.clauses, **kw)
        return ('TRANSLATE({x} USING ' + custom + ')').format(x = column_expression)

    return _SQLColumnExpression(_translate(expr.expression))



def to_numeric(arg, **kw):

    """
    Convert a string-like representation of a number to a Numeric type.

    PARAMETERS:
      arg: DataFrame column
      kw: optional keyword arguments
        format_: string. Specifies the format of a string-like number to convert to numeric
        nls: dict where 'param' and 'value' are keys:

             - param specifies one of the following string values:
                 -'CURRENCY', 'NUMERIC_CHARACTERS', 'DUAL_CURRENCY', 'ISO_CURRENCY'

             - value: specifies characters that are returned by number format elements.
                      See References for more information

    REFERENCES:
      Chapter 14: Data Type Conversion Functions
      Teradata® Database SQL Functions, Operators, Expressions, and
      Predicates, Release 16.20


    RETURNS:
      A DataFrame column of numeric type

    NOTES:
      - If the arg column input is a numeric type, it is returned as is
      - Nulls may be introduced in the result if the parsing fails
      - You may need to strip() columns that have leading or trailing spaces
        in order for to_numeric to parse correctly

    EXAMPLES:

      >>> df = DataFrame('numeric_strings')

                    hex decimal commas numbers
          0        19FF   00.77   08,8       1
          1        abcd    0.77   0,88       1
          2  ABCDEFABCD   0.7.7   ,088     999
          3        2018    .077   088,       0

      >>> df.dtypes

          hex        str
          decimal    str
          commas     str
          numbers    str

      # converting string numbers to numeric
      >>> df.assign(drop_columns = True,
                    numbers = df.numbers,
                    numeric = to_numeric(df.numbers))

            numbers numeric
          0       1       1
          1       1       1
          2     999     999
          3       0       0


      # converting decimal-like strings to numeric
      # Note that strings not following the format return None
      >>> df.assign(drop_columns = True,
                   decimal = df.decimal,
                   numeric_dec = to_numeric(df.decimal))

            decimal numeric_dec
          0   00.77         .77
          1    0.77         .77
          2   0.7.7        None
          3    .077        .077

      # converting comma (group separated) strings to numeric
      # Note that strings not following the format return None
      >>> df.assign(drop_columns = True,
                    commas = df.commas,
                    numeric_commas = to_numeric(df.commas, format_ = '9G99'))

            commas numeric_commas
          0   08,8           None
          1   0,88             88
          2   ,088           None
          3   088,           None

      # converting hex strings to numeric
      >>> df.assign(drop_columns = True,
                    hex = df.hex, 
                    numeric_hex = to_numeric(df.hex, format_ = 'XXXXXXXXXX'))

                    hex   numeric_hex
          0        19FF          6655
          1        abcd         43981
          2  ABCDEFABCD  737894443981
          3        2018          8216

      # converting literals to numeric
      >>> df.assign(drop_columns = True,
                    a = to_numeric('123,456',format_ = '999,999'),
                    b = to_numeric('1,333.555', format_ = '9,999D999'),
                    c = to_numeric('2,333,2',format_ = '9G999G9'),
                    d = to_numeric('3E20'),
                    e = to_numeric('$41.99', format_ = 'L99.99'),
                    f = to_numeric('$.12', format_ = 'L.99'),
                    g = to_numeric('dollar123,456.00',
                                   format_ = 'L999G999D99', 
                                   nls = {'param': 'currency', 'value': 'dollar'})).head(1)

              a         b      c                         d      e    f       g
          0  123456  1333.555  23332 300000000000000000000  41.99  .12  123456

      # For more information on format elements and parameters, see the Reference.
    """

    # validation
    if not isinstance(arg, str) and not isinstance(arg, ColumnExpression):
        msg = Messages.get_message(MessageCodes.TDMLDF_UNKNOWN_TYPE).format('arg', "a string or DataFrame column of type CHAR or VARCHAR")
        raise TeradataMlException(msg, MessageCodes.TDMLDF_UNKNOWN_TYPE)

    expr = None
    if isinstance(arg, ColumnExpression):
        expr = arg.expression
    else:
        expr = literal(arg, type_ = VARCHAR(length = len(arg), charset = 'UNICODE'))

    # The only reason to use to_numeric with a numerically typed column is if downcast is used, 
    # but those downcasted types are not supported (uint8, int8, float32)
    # TODO: Look into supporting downcasting if we implement the three downcasted types above
    if isinstance(expr.type, tuple(UtilFuncs()._get_numeric_datatypes())):
        return arg

    if not isinstance(expr.type, (VARCHAR, CHAR)):
        msg = Messages.get_message(MessageCodes.TDMLDF_UNKNOWN_TYPE).format('arg', "a string or DataFrame column of type CHAR or VARCHAR")
        raise TeradataMlException(msg, MessageCodes.TDMLDF_UNKNOWN_TYPE)

    fmt = kw.get('format_', None)
    nls = kw.get('nls', None)

    if fmt is not None and not isinstance(fmt, str):
        msg = Messages.get_message(MessageCodes.TDMLDF_UNKNOWN_TYPE).format('format_', "a string")
        raise TeradataMlException(msg, MessageCodes.TDMLDF_UNKNOWN_TYPE)

    if nls is not None and not isinstance(nls, dict):
        msg = Messages.get_message(MessageCodes.TDMLDF_UNKNOWN_TYPE).format('nls', "a dict")
        raise TeradataMlException(msg, MessageCodes.TDMLDF_UNKNOWN_TYPE)

    # prepare for _to_number
    if fmt is not None:
        fmt = _as_varchar_literal(fmt)

        if nls is not None:
            if not (('param' in nls) and ('value' in nls)):
                msg = Messages.get_message(MessageCodes.INVALID_ARG_VALUE).format(nls, 'nls', 'dict with "param" and "value" keys')
                raise TeradataMlException(msg, MessageCodes.INVALID_ARG_VALUE)

            if not isinstance(nls['param'], str) and not isinstance(nls['value'], str):
                msg = Messages.get_message(MessageCodes.INVALID_ARG_VALUE).format(nls, 'nls', 'dict with "param" and "value" keys mapping to string values')
                raise TeradataMlException(msg, MessageCodes.INVALID_ARG_VALUE)

            nls_params = ('NUMERIC_CHARACTERS', 'CURRENCY', 'DUAL_CURRENCY', 'ISO_CURRENCY')

            if not nls['param'].upper() in nls_params:
                msg = Messages.get_message(MessageCodes.INVALID_ARG_VALUE).format(nls['param'].upper(), "nls['param']", 'in {}'.format(nls_params))
                raise TeradataMlException(msg, MessageCodes.INVALID_ARG_VALUE)

            nls_param = nls['param'].upper()
            nls_value = _as_varchar_literal(nls['value'])
            nls = {'param': nls_param, 'value': nls_value}

    elif nls is not None:
      msg = Messages.get_message(MessageCodes.MISSING_ARGS).format('format_. format_ keyword must be specfied if the nls keyword is used')
      raise TeradataMlException(msg, MessageCodes.MISSING_ARGS)

    label = arg.name if isinstance(arg, ColumnExpression) else arg
    stmt = _to_number(expr, format_=fmt, nls=nls).label(label)

    return _SQLColumnExpression(stmt)


class _to_number(expression.FunctionElement):
    """
    Internal class used for representing the TO_NUMBER function in the SQL Engine.

    """
    name = '_to_number'
    type = NUMBER()

    def __init__(self, arg, format_=None, nls=None, **kw):
        """
        See docstring for_to_numeric.

        Reference
        ---------
        Chapter 14: Data Type Conversion Functions
        Teradata® Database SQL Functions, Operators, Expressions, and
        Predicates, Release 16.20

        """
        args = [arg, format_]
        if nls is not None:
            args.append(nls['value'])
            self.nls_param = 'NLS_' + nls['param']

        args = (x for x in args if x is not None)
        super().__init__(*args)

@compiles(_to_number)
def _visit_to_number(element, compiler, **kw):
    """
    Compilation method for the _to_number function element class

    Parameters
    ----------
    element: A sqlalchemy ClauseElement instance
    compiler: A sqlalchemy.engine.interfaces.Compiled instance

    """
    col_exps = [compiler.process(exp, **kw) for exp in element.clauses]

    optional = ''

    # handle format
    if len(col_exps) >= 2:
        optional += ', {}'.format(col_exps[1])

        # handle nls
        if len(col_exps) >= 3:
            optional += ", '{} = '{}''".format(element.nls_param, col_exps[2])

    res = ('TO_NUMBER({x}{optional})').format(x = col_exps[0], optional = optional)
    return res
