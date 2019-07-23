from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime
from typing import Any
from sqlalchemy.orm.query import Query


class UtcNow(expression.FunctionElement):
    type = DateTime()


@compiles(UtcNow, 'postgresql')
def _pg_utcnow(element, compiler, **kw):
    # return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
    return "(date_part('epoch'::text, now()) * (1000)::double precision)"


@compiles(UtcNow, 'mysql')
def _mysql_utcnow(element, compiler, **kw):
    return "UNIX_TIMESTAMP()"


def compiled_sql(query: Any):
    if isinstance(query, Query):
        return str(query.statement.compile(compile_kwargs={"literal_binds": True}))
    return ''
