'''
__created__: 01. Aug. 2016

@author: fredriksson
'''

import datetime

#from types import NoneType
#from .generate import generate_datetime, strptime

DATETIME_DUMMY = "CCYY-MM-DDTHH:MMZ"
DATETIME_FORMAT = "%Y-%m-%dT%H:%MZ"


def to_dt(dts):
    try:
        dt = datetime.datetime.strptime(dts, DATETIME_FORMAT)
    except:
        dt = datetime.datetime.max
    finally:
        return dt
        

def to_str(dt):
    assert isinstance(dt, (datetime.datetime, type(None)))
    if dt == datetime.datetime.max or dt is None:
        return DATETIME_DUMMY
    else:
        return dt.strftime(DATETIME_FORMAT)


class TimeWindow(object):

    def __init__(self, **kwargs):
        valid_from = kwargs.get("valid_from")
        valid_until = kwargs.get("valid_until")

        assert isinstance(valid_from, datetime.datetime)
        assert isinstance(valid_until, (datetime.datetime, type(None)))
        self.valid_from = valid_from
        self.valid_until = valid_until

    def __str__(self, *args, **kwargs):
        return u"%s - %s" % (to_str(self.valid_from), to_str(self.valid_until))

    def is_covering_datetime(self, date_time):
        """
        This methods checks a DateTime against a TimeWindow

        :param date_time: DateTime to test
        :type date_time: datetime.datetime
        :returns: True, if date_time lies in TimeWindow, else False
        """
        assert isinstance(date_time, (datetime.datetime, type(None)))

        valid_from = self.valid_from
        valid_until = self.valid_until

        if self.valid_until is None:
            valid_until = datetime.datetime.now().replace(second=0, microsecond=0)

        if valid_until is None and date_time is None:
            return True

        if valid_until is not None and date_time is None:
            return True

        is_g = valid_from <= date_time

        if is_g and valid_until is None:
            return True

        is_l = date_time < valid_until

        return is_g and is_l

    def is_covering_sensor(self, sensor):
        raise NotImplementedError
    #     window_valid_from = self.valid_from
    #     window_valid_until = self.valid_until
    #     if self.valid_until is None:
    #         window_valid_until = datetime.datetime.now().replace(second=0, microsecond=0)

    #     if sensor.valid_until is None or sensor.valid_until == DATETIME_DUMMY:
    #         sensor_valid_until = window_valid_until
    #     else:
    #         sensor_valid_until = sensor.valid_until
    #     if type(sensor_valid_until) == str:
    #         sensor_valid_until = strptime(sensor_valid_until)
    #     sensor_valid_from = strptime(sensor.valid_from)

    #     valid_from = window_valid_from >= sensor_valid_from
    #     valid_until = window_valid_until <= sensor_valid_until

    #     if valid_from and valid_until:
    #         return True
        
    #     return False

    def is_covering_date(self, da):
        """
        :param da: Date to cover
        :type da: datetime.date
        """
        valid_from = self.valid_from.date()
        valid_until = self.valid_until.date()
        is_covered = da >= valid_from and da <= valid_until
        return is_covered

    def get_duration(self):
        """
        :return: Duration of current time window
        :rtype: datetime.timedelta
        """
        if self.valid_until is None:
            valid_until = datetime.datetime.now() + datetime.timedelta(days=7)
        else:
            valid_until = self.valid_until
        return (valid_until - self.valid_from).total_seconds()

    @staticmethod
    def get_time_windows(type_a_list, type_b_list):
        """
        Generates a list of TimeWindows for the TypeA and TypeB lists

        :returns: List of TimeWindows
        :rtype: list
        """
        # lock type_a, check type_bs
        twr = []
        twi = []
        tw = []

        assert isinstance(type_a_list, list)
        assert isinstance(type_b_list, list)
        assert len(type_a_list) > 0
        assert len(type_b_list) > 0

        type_a = sorted(type_a_list, key=lambda x: x.valid_from)
        type_b = sorted(type_b_list, key=lambda x: x.valid_from)

        for ai in type_a:
            a_valid_until = ai.valid_until
            if a_valid_until is None:
                a_valid_until = datetime.datetime.max
            a_valid_from = ai.valid_from
            for bi in type_b:
                b_valid_until = bi.valid_until
                if b_valid_until is None:
                    b_valid_until = datetime.datetime.max
                b_valid_from = bi.valid_from
                if (a_valid_until <= b_valid_until and a_valid_until > b_valid_from) or \
                        a_valid_until is None:
                    twr.append(a_valid_until)

                if a_valid_from >= b_valid_from and a_valid_from < b_valid_until:
                    twi.append(a_valid_from)

                if (b_valid_until <= a_valid_until and b_valid_until > a_valid_from) or \
                        b_valid_until is None:
                    twr.append(b_valid_until)

                if b_valid_from >= a_valid_from and b_valid_from < a_valid_until:
                    twi.append(b_valid_from)

        twr = sorted(list(set(twr)))
        twi = sorted(list(set(twi)))

        assert len(twr) == len(twi)
        for i in range(len(twr)):

            valid_until = None if twr[i] == datetime.datetime.max else twr[i]

            temp_window = TimeWindow(
                valid_from=twi[i],
                valid_until=valid_until
            )
            tw.append(temp_window)
        return tw
