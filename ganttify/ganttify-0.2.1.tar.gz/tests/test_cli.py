import json
import os
import pytest

from click.testing import CliRunner

import ganttify
import ganttify.cli as cli


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


@pytest.fixture
def runner():
    return CliRunner()


def _invoke(runner, args):
    return runner.invoke(
        cli.cli,
        args,
        catch_exceptions=False)


# so these are actually integration tests, but they're fine thanks to tmpdir
def describe_cli():
    def makes_a_chart(mocker, runner, data, tmpdir):
        with tmpdir.as_cwd():
            # sanity check
            assert not os.path.exists(str(tmpdir.join('chart.html')))

            spy = mocker.patch('ganttify.make_chart', wraps=ganttify.make_chart)

            args = [json.dumps(data)]
            result = _invoke(runner, args)
            assert result.exit_code == 0

            spy.assert_called_once_with(
                data,
                'chart.html',
                labelLimit=ganttify.DEFAULT_LABEL_LIMIT,
                width=ganttify.DEFAULT_WIDTH,
                timescale=ganttify.DEFAULT_TIMESCALE)

            assert os.path.exists(str(tmpdir.join('chart.html')))

    def allows_overrides(mocker, runner, data, tmpdir):
        with tmpdir.as_cwd():
            # sanity check
            assert not os.path.exists(str(tmpdir.join('foo.html')))

            spy = mocker.patch('ganttify.make_chart', wraps=ganttify.make_chart)

            args = ['-o', 'foo.html', '-w', 11, '-l', 123, '-t', 'hours', json.dumps(data)]
            result = _invoke(runner, args)
            assert result.exit_code == 0

            spy.assert_called_once_with(
                data,
                'foo.html',
                labelLimit=123,
                width=11,
                timescale='hours')

            assert os.path.exists(str(tmpdir.join('foo.html')))

    def allows_for_data_to_be_a_file(mocker, runner, data, tmpdir):
        with tmpdir.as_cwd():
            # sanity check
            assert not os.path.exists(str(tmpdir.join('chart.html')))

            spy = mocker.patch('ganttify.make_chart', wraps=ganttify.make_chart)

            with open('datafile.json', 'w') as f:
                json.dump(data, f)

            args = ['datafile.json']
            result = _invoke(runner, args)
            assert result.exit_code == 0

            spy.assert_called_once_with(
                data,
                'chart.html',
                labelLimit=ganttify.DEFAULT_LABEL_LIMIT,
                width=ganttify.DEFAULT_WIDTH,
                timescale=ganttify.DEFAULT_TIMESCALE)

            assert os.path.exists(str(tmpdir.join('chart.html')))
