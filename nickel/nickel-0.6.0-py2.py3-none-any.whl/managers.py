# coding=utf8

from __future__ import unicode_literals

from django.db import models


class HBaseQueryset(models.QuerySet):
    def retrieve_object(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


def optional_query(**kwargs):
    qd = {k: v for k, v in kwargs.items() if v is not None}
    return models.Q(**qd)


def keyword_query(keyword, fields=None, sep='-'):
    if keyword is None:
        return models.Q()
    if isinstance(fields, str):
        fields = fields.split(sep)
    q = models.Q()
    for f in fields:
        q |= models.Q(**{f + '__icontains': keyword})
    return q


def period_year_month_query(start_month=None, end_month=None, *, year_field='year', month_field='month'):
    q = models.Q()
    try:
        sy, sm = map(int, start_month.split('-'))
        q &= models.Q(**{year_field + '__gt': sy}) | models.Q(**{year_field: sy, month_field + '__gte': sm})
    except (AttributeError, TypeError, ValueError):
        pass
    try:
        ey, em = map(int, end_month.split('-'))
        q &= models.Q(**{year_field + '__lt': ey}) | models.Q(**{year_field: ey, month_field + '__lte': em})
    except (AttributeError, TypeError, ValueError):
        pass
    return q
