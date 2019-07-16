import pytest

import ganttify


@pytest.fixture
def data():
    return [
        {
            'queue': '2019-04-02T16:51:15-05:00',
            'start': '2019-04-02T16:51:30-05:00',
            'end': '2019-04-02T16:52:22-05:00',
            'status': 'success',
            'label': 'foo1',
        },
        {
            'queue': '2019-04-02T16:51:15-05:00',
            'start': '2019-04-02T16:53:00-05:00',
            'end': '2019-04-02T16:53:44-05:00',
            'status': 'failure',
            'label': 'foo2',
        },
        {
            'start': '2019-04-02T16:51:33-05:00',
            'end': '2019-04-02T16:52:33-05:00',
            'status': 'success',
            'label': 'foo3',
        },
    ]


def describe_process_data():
    @pytest.fixture(autouse=True)
    def mocked_data_frame(mocker):
        patched = mocker.patch('ganttify.pd.DataFrame', autospec=True)
        return patched

    def creates_data_frmes_for_the_data(data, mocked_data_frame):
        result = ganttify.process_data(data)
        expected = []

        for i, entry in enumerate(data):
            status = 'success'
            if entry['status'].lower() != 'success':
                status = 'fail'

            if 'queue' in entry:
                expected.append({
                    'label': entry['label'],
                    'type': 'queue',
                    'start': ganttify.pd.to_datetime(entry['queue']),
                    'end': ganttify.pd.to_datetime(entry['start']),
                    'idx': i,
                })

            expected.append({
                'label': entry['label'],
                'type': status,
                'start': ganttify.pd.to_datetime(entry['start']),
                'end': ganttify.pd.to_datetime(entry['end']),
                'idx': i,
            })

        # sanity check to ensure the above does what we expected
        assert len(expected) == len(data) * 2 - 1

        assert result == mocked_data_frame.return_value
        mocked_data_frame.assert_called_once_with(expected)


def describe_make_chart():
    @pytest.fixture
    def outfile_name():
        return 'mychart.html'

    @pytest.fixture(autouse=True)
    def mocked_process_data(mocker):
        patched = mocker.patch('ganttify.process_data', autospec=True)
        return patched

    # so this is pretty crappy, but it's to be expected
    # given the way the altair api is
    def creates_the_chart(mocker, data, outfile_name, mocked_process_data):
        mocked_chart = mocker.patch('ganttify.alt.Chart', autospec=True)

        ganttify.make_chart(data, outfile_name)

        mocked_process_data.assert_called_once_with(data)
        mocked_chart.assert_called_once_with(
            ganttify.process_data(data))

        target = mocked_chart.return_value
        target.mark_bar.assert_called_once_with()

        target = target.mark_bar.return_value
        target.configure_axisY.assert_called_once_with(
            labelLimit=ganttify.DEFAULT_LABEL_LIMIT)

        target = target.configure_axisY.return_value
        target.configure_view.assert_called_once_with(
            width=ganttify.DEFAULT_WIDTH)

        target = target.configure_view.return_value
        target.encode.assert_called_once_with(
            x=ganttify.alt.X(
                '{}(start):T'.format(ganttify.DEFAULT_TIMESCALE),
                title='Time'
            ),
            x2=ganttify.alt.X(
                '{}(end):T'.format(ganttify.DEFAULT_TIMESCALE),
                title='Duration'
            ),
            y=ganttify.alt.Y(
                'label:N',
                axis=ganttify.DEFAULT_YAXIS,
                sort=ganttify.alt.EncodingSortField(
                    field='idx',
                    op='sum',
                    order='ascending'
                ),
                title=None
            ),
            color=ganttify.alt.Color(
                'type:N',
                legend=ganttify.alt.Legend(title='segment'),
                scale=ganttify.DEFAULT_COLOR_SCALE,
            ))

        target = target.encode.return_value
        target.save.assert_called_once_with(outfile_name)
