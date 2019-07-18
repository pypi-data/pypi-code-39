# !usr\bin\env python
# -*- coding:utf-8 -*-
from setuptools import setup

setup(
    name='timetoolkit',
    version='2.0',
    author='张乐涛',
    author_email='1668151593@qq.com',
    url='https://github.com',
    description='Some great tools about time.',
    long_description='''
    <h2>How to use this package:</h2>



    >>> import timetoolkit as t


    >>> print(t.GetDateTimeNow())


    [2019, 7, 18, 16, 27, 1, 958]


    >>> c = t.Calendar.GetCalendarByYear(2018)


    >>> print(c.GetWeekdayByMonthAndDay(7, 2))


    0
''',
    packages=['timetoolkit'],
    install_requires=[])
