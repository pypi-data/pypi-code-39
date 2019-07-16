# -*- coding: utf-8 -*-

"""Console script for ganttify."""
import click
import json
import os

import ganttify


# allow -h as well as --help
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

TIMESCALE_CHOICES = [
    'date',
    'day',
    'hours',
    'hoursminutes',
    'hoursminutesseconds',
    'milliseconds'
    'minutes',
    'minutesseconds',
    'month',
    'monthdate',
    'quarter',
    'quartermonth',
    'seconds',
    'secondsmilliseconds',
    'year',
    'yearmonth',
    'yearmonthdate',
    'yearmonthdatehours',
    'yearmonthdatehoursminutes',
    'yearmonthdatehoursseconds',
    'yearquarter',
    'yearquartermonth',
]


@click.command(context_settings=CONTEXT_SETTINGS, name='ganttify')
@click.option(
    '-o',
    '--outfile',
    default='chart.html',
    help='The output file. Should be .html unless you have the prerequisites for other file types.'
)
@click.option(
    '-w',
    '--width',
    type=int,
    default=ganttify.DEFAULT_WIDTH,
    help='The width of the chart in pixels'
)
@click.option(
    '-l',
    '--label-limit',
    type=int,
    default=ganttify.DEFAULT_LABEL_LIMIT,
    help='The label length limit in pixels'
)
@click.option(
    '-t',
    '--timescale',
    type=click.Choice(TIMESCALE_CHOICES),
    default=ganttify.DEFAULT_TIMESCALE,
    help='The time units to use according to the Altair docs'
)
@click.argument('data', required=True)
def cli(data, outfile, width, label_limit, timescale):
    """This is a thin wrapper around the Altair python visualization library
    specifically for creating Gantt charts of CI pipeline results given data in
    the following JSON format:

    \b
    [
        {
            'queue': 'OPTIONAL - pandas parsable timestamp',
            'start': 'REQUIRED - pandas parsable timestamp',
            'end': 'REQUIRED - pandas parsable timestamp',
            'status': 'REQUIRED - any string other than "success" is interpreted as a failure',
            'label': 'REQUIRED - label string',
        },
        ...
    ]

    This satisfies my own use cases, use at your own risk.

    For more control, recommend importing the ganttify module and invoking
    make_chart from a script.

    The data argument here can be a json blob or a filename
    """
    try:
        data = json.loads(data)
    except ValueError:
        # this is a bit of a dumb sanity check, but it will probably suffice
        if '[' not in data and os.path.exists(data):
            with open(data) as f:
                data = json.load(f)
        else:
            raise

    ganttify.make_chart(
        data,
        outfile,
        labelLimit=label_limit,
        width=width,
        timescale=timescale)
