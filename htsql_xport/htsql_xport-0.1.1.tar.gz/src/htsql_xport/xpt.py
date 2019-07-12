from htsql.core.fmt.accept import Accept  
from htsql.core.fmt.format import Format
from htsql.core.fmt.emit import EmitHeaders, Emit
from htsql.core.adapter import Adapter, adapt, adapt_many, Protocol, call
from htsql.core.addon import Addon
from htsql.core.domain import (Domain, BooleanDomain, NumberDomain, DecimalDomain,
    TextDomain, EnumDomain, DateDomain, TimeDomain, DateTimeDomain, ListDomain, 
    RecordDomain, UntypedDomain, VoidDomain, OpaqueDomain, Profile, FloatDomain)
from htsql.core.cmd.summon import SummonFormat
from htsql.core.util import listof

from io import BytesIO
import xport
import math


XPT_MIME_TYPE = 'application/x-sas-xport'


class XPTAddon(Addon):
    name = 'htsql_xport'
    hint = 'Basic support for SAS V5 XPORT transport files'


class XPTFormat(Format):
    pass


class SummonXPT(SummonFormat):
    call('xpt')
    format = XPTFormat


class AcceptXPT(Accept):
    call(XPT_MIME_TYPE)
    format = XPTFormat


class EmitXPTHeaders(EmitHeaders):

    adapt(XPTFormat)

    def __call__(self):
        filename = None
        if self.meta.header:
            filename = self.meta.header.encode('utf-8')
        if not filename:
            filename = b'_'
        filename = filename.replace(b'\\', b'\\\\').replace(b'"', b'\\"')
        yield ('Content-Type', XPT_MIME_TYPE)
        yield ('Content-Disposition', 'attachment; filename="%s.xpt"' % filename)


class EmitXPT(Emit):

    adapt(XPTFormat)

    def __call__(self):
        product_to_xpt = to_xpt(self.meta.domain, [self.meta])
        if not product_to_xpt.width:
            return
        headers = product_to_xpt.headers()
        to_cells = product_to_xpt.cells
        assert len(headers) == product_to_xpt.width

        rows = []

        for vals in to_cells(self.data):
            row = {}
            for i in range(0, len(headers)):
                name = str(headers[i]).lower().replace(" ", "_")
                value = vals[i]
                row[name] = value

            rows.append(row)

        fp = BytesIO()
        xport.from_rows(rows, fp)
        fp.seek(0)
        return fp


class ToXPT(Adapter):

    adapt(Domain)

    def __init__(self, domain, profiles):
        assert isinstance(domain, Domain)
        assert isinstance(profiles, listof(Profile)) and len(profiles) > 0
        self.domain = domain
        self.profiles = profiles
        self.width = 1

    def __call__(self):
        return self

    def headers(self):
        return [self.profiles[-1].header]

    def cells(self, value):
        if value is None:
            yield [None]
        else:
            yield [self.domain.dump(value)]


class VoidToXPT(ToXPT):

    adapt(VoidDomain)

    def __init__(self, domain, profiles):
        super(VoidToXPT, self).__init__(domain, profiles)
        self.width = 0

    def headers(self):
        return []

    def cells(self):
        if False:
            yield []


class RecordToXPT(ToXPT):

    adapt(RecordDomain)

    def __init__(self, domain, profiles):
        super(RecordToXPT, self).__init__(domain, profiles)
        self.fields_to_xpt = [to_xpt(field.domain, profiles+[field])
                              for field in domain.fields]
        self.width = 0
        for field_to_xpt in self.fields_to_xpt:
            self.width += field_to_xpt.width

    def headers(self):
        row = []
        for field_to_xpt in self.fields_to_xpt:
            row.extend(field_to_xpt.headers())
        return row

    def cells(self, value):
        if not self.width:
            return
        if value is None:
            yield [None]*self.width
        else:
            streams = [(field_to_xpt.cells(item), field_to_xpt.width)
                       for item, field_to_xpt in zip(value, self.fields_to_xpt)]
            is_done = False
            while not is_done:
                is_done = True
                row = []
                for stream, width in streams:
                    subrow = next(stream, None)
                    if subrow is None:
                        subrow = [None]*width
                    else:
                        is_done = False
                    row.extend(subrow)
                if not is_done:
                    yield row


class ListToXPT(ToXPT):

    adapt(ListDomain)

    def __init__(self, domain, profiles):
        super(ListToXPT, self).__init__(domain, profiles)
        self.item_to_xpt = to_xpt(domain.item_domain, profiles)
        self.width = self.item_to_xpt.width

    def headers(self):
        return self.item_to_xpt.headers()

    def cells(self, value):
        if not self.width:
            return
        if value is not None:
            item_to_cells = self.item_to_xpt.cells
            for item in value:
                for row in item_to_cells(item):
                    yield row


class BooleanToXPT(ToXPT):

    adapt(BooleanDomain)

    def cells(self, value):
        if value is None:
            yield [None]
        elif value is True:
            yield ["1"]
        elif value is False:
            yield ["0"]


class NumberToXPT(ToXPT):

    adapt(NumberDomain)

    def cells(self, value):
        if value is None:
            yield [None]
        else:
            yield [int(value)]


class FloatToXPT(ToXPT):

    adapt(FloatDomain)

    def cells(self, value):
        if value is None or math.isinf(value) or math.isnan(value):
            yield [None]
        else:
            yield [float(value)]


class DecimalToXPT(ToXPT):

    adapt(DecimalDomain)

    def cells(self, value):
        if value is None or not value.is_finite():
            yield [None]
        else:
            yield [float(value)]


class TextToXPT(ToXPT):

    adapt_many(UntypedDomain,
               TextDomain,
               EnumDomain)

    def cells(self, value):
        yield [value]


class DateToXPT(ToXPT):

    adapt(DateDomain)

    def cells(self, value):
        if value is None:
            yield [None]
        else:
            yield [str(value)]


class TimeToXPT(ToXPT):

    adapt(TimeDomain)

    def cells(self, value):
        if value is None:
            yield [None]
        else:
            yield [str(value)]


class DateTimeToXPT(ToXPT):

    adapt(DateTimeDomain)

    def cells(self, value):
        if value is None:
            yield [None]
        elif not value.time():
            yield [str(value.date())]
        else:
            yield [str(value)]


class OpaqueToXPT(ToXPT):

    adapt(OpaqueDomain)

    def cells(self, value):
        if value is None:
            yield [None]
            return
        yield [str(value)]


to_xpt = ToXPT.__invoke__
