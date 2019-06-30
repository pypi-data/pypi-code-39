from __future__ import annotations

from piccolo.query.base import Query
from piccolo.query.mixins import ValuesMixin, WhereMixin
from piccolo.querystring import QueryString


class Update(Query, ValuesMixin, WhereMixin):

    @property
    def sqlite_querystring(self) -> QueryString:
        raise NotImplementedError()

    def validate(self):
        if len(self._values) == 0:
            raise ValueError(
                "No values were specified to update - please use .values"
            )

        for column, value in self._values.items():
            if len(column.call_chain) > 0:
                raise ValueError(
                    "Related values can't be updated via an update"
                )

    @property
    def postgres_querystring(self) -> QueryString:
        self.validate()

        columns_str = ', '.join([
            f'{col._name} = {{}}' for col, _ in self._values.items()
        ])

        query = f'UPDATE {self.table.Meta.tablename} SET ' + columns_str

        querystring = QueryString(
            query,
            *self._values.values()
        )

        # TODO - need to support joins
        # UPDATE band SET name='bob' FROM manager WHERE band.manager = manager.id AND manager.name = 'Guido';
        # I think the joins should work differently from select i.e. no need
        # to shared underlying code.

        if self._where:
            where_querystring = QueryString(
                '{} WHERE {}',
                querystring,
                self._where.querystring
            )
            return where_querystring
        else:
            return querystring

