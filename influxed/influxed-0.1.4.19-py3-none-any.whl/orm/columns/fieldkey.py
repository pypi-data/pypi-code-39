import pandas as pd
import datetime as dt
from influxed.ifql.functions import Count, Min, Max, Mean, Distinct, Percentile, Derivative, Sum, Stddev, First, Last
from influxed.ifql.column import Field
from influxed.orm.capabilities.queryable import queryable
from influxed.orm.capabilities.insertable import insertable

class FieldKey(Field, queryable, insertable):

    @property
    def database(self):
        return self.__measurement__.database

    @property
    def measurement(self):
        return self.__measurement__
    
    def set_measurement(self, val):
        self.__measurement__ = val
        return self


    def __select_prefix__(self, select_statement):
        return select_statement.from_(self.measurement.name).select(self)
