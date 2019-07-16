# -*- coding: utf-8 -*-

"""Top-level package for ganttify."""
import altair as alt
import pandas as pd

DEFAULT_COLOR_SCALE = alt.Scale(
    domain=[
        'queue',
        'success',
        'fail',
    ],
    range=['gray', 'blue', 'red'])

DEFAULT_LABEL_LIMIT = 1000
DEFAULT_WIDTH = 1000
DEFAULT_TIMESCALE = 'hoursminutes'

DEFAULT_YAXIS = alt.Axis(
    ticks=False,
    minExtent=60,
    domain=False)


def process_data(data):
    arr = []
    # we have to set an additional attribute so we can preserve
    # the sort order when showing the chart
    for i, entry in enumerate(data):
        status = 'success'
        if entry['status'].lower() != 'success':
            status = 'fail'

        if 'queue' in entry:
            arr.append({
                'label': entry['label'],
                'type': 'queue',
                'start': pd.to_datetime(entry['queue']),
                'end': pd.to_datetime(entry['start']),
                'idx': i,
            })

        arr.append({
            'label': entry['label'],
            'type': status,
            'start': pd.to_datetime(entry['start']),
            'end': pd.to_datetime(entry['end']),
            'idx': i,
        })

    return pd.DataFrame(arr)


def make_chart(
    data,
    outfile,
    color_scale=DEFAULT_COLOR_SCALE,
    labelLimit=DEFAULT_LABEL_LIMIT,
    width=DEFAULT_WIDTH,
    timescale=DEFAULT_TIMESCALE,
    yaxis=DEFAULT_YAXIS,
):
    df = process_data(data)

    chart = alt.Chart(df) \
        .mark_bar() \
        .configure_axisY(labelLimit=labelLimit) \
        .configure_view(width=width) \
        .encode(
            # we're slightly abusing the titles here
            x=alt.X(
                '{}(start):T'.format(timescale),
                title='Time'
            ),
            x2=alt.X(
                '{}(end):T'.format(timescale),
                title='Duration'
            ),
            y=alt.Y(
                'label:N',
                axis=yaxis,
                sort=alt.EncodingSortField(field='idx', op='sum', order='ascending'),
                title=None
            ),
            color=alt.Color(
                'type:N',
                legend=alt.Legend(title='segment'),
                scale=color_scale,
            ))

    chart.save(outfile)
