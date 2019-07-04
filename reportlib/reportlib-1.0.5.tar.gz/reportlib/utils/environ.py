from os import environ
from datetime import datetime
from dateutil import rrule


class EnvironParser:
    def __init__(self, date_fmt='%Y-%m-%d', month_fmt='%Y-%m', year_fmt='%Y'):
        self.date_fmt = date_fmt
        self.month_fmt = month_fmt
        self.year_fmt = year_fmt

        self._datetime_options = [
            ('REPORT_DATE', date_fmt),
            ('REPORT_MONTH', month_fmt),
            ('REPORT_YEAR', year_fmt),
        ]
        
        self._bool_options = ['REVERSE']

        self._range_options = [
            ('DATE_RANGE', date_fmt, rrule.DAILY),
            ('MONTH_RANGE', month_fmt, rrule.MONTHLY),
            ('YEAR_RANGE', year_fmt, rrule.YEARLY),
        ]

        self._copy_options = ['EMAIL_ENV', 'METADATA_PROFILE', 'EMAIL_CONFIG_PATH', 'HTML_OUTPUT_PATH']
        self._list_options = ['CUBE_NAME', 'ALLOW_STORAGE']

    def parse(self):
        options = {}
        for key, fmt in self._datetime_options:
            if key in environ:
                options[key] = datetime.strptime(environ[key], fmt)
        
        for key in self._bool_options:
            if key in environ:
                options[key] = bool(environ[key])

        for key, fmt, freq in self._range_options:
            if key in environ:
                start, end = map(lambda s: datetime.strptime(s, fmt), environ[key].split(',', 1))
                options[key] = list(rrule.rrule(freq, dtstart=start, until=end))
                if options.get('REVERSE'):
                    options[key] = options[key][::-1]

        for key in self._copy_options:
            if key in environ:
                options[key] = environ[key]

        for key in self._list_options:
            if key in environ:
                options[key] = environ[key].split(',')
        return options
