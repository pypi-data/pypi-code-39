# coding=utf8


class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '{:04d}'.format(value)


class MonthConverter:
    regex = '[0-9]{2}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '{:02d}'.format(value)


class PrimeKeyConverter:
    regex = '\d+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)
