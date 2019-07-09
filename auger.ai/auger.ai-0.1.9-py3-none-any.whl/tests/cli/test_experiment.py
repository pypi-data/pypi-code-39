import os

import pytest

from auger.cli.cli import cli
from auger.api.utils.config_yaml import ConfigYaml
from .utils import interceptor, ORGANIZATIONS, PROJECTS


PROJECT_FILE = {
    'data': {
        'name': 'iris-1.csv',
        'id': 1256,
        'statistics': {
            'columns_count': 5, 'count': 150, 
            'stat_data': [{
                'datatype': 'categorical',
                'column_name': 'class',
                'unique_values': 3
            }]
         },
    }
}

PROJECT_FILES = {
    'meta': {
        'pagination': {'offset': 0, 'count': 1, 'total': 1, 'limit': 100},
        'status': 200},
    'data': [PROJECT_FILE['data']]
}

EXPERIMENTS = {
    'meta': {
        'pagination': {'offset': 0, 'count': 1, 'total': 1, 'limit': 100},
        'status': 200},
    'data': [{
        'name': 'iris-1.csv-experiment',
        'project_file_id': 1256,
    }]
}

EXPERIMENT_SESSIONS = {
    'meta': {
        'pagination': {'offset': 0, 'count': 2, 'total': 2, 'limit': 100},
        'status': 200},
    'data': [{
        'id': 'test_id_1',
        'model_settings': {'start_time': '2019-06-26 22:00:00.405'},
        'status': 'completed',
    },
    {
        'id': 'test_id_2',
        'model_settings': {'start_time': '2019-06-28 20:30:00.992405'},
        'status': 'completed',
    }
    ]
}

EXPERIMENT_SESSION = {
    'data': {
        'id': 'test_id_2',
        'model_settings': {'start_time': '2019-06-28 20:30:00.992405'},
        'status': 'completed',
        'project_file_id': '1234',
    }
}

TRIALS = {
    'meta': {'pagination': {'offset': 0, 'limit': 100, 'count': 20, 'total': 20}, 'status': 200},
    'data': [{
        'id': 'A79FBADD8CCD417',
        'score_name': 'f1_macro',
        'score_value': 0.123,
        'hyperparameter': {'algorithm_name': 'auger_ml.algorithms.baseline.BaselineClassifier'},
    }]*20
}

PROJECT = {
    'data': {
        'status': 'running',
    }
}


class TestExperimentCLI():
    def test_list(self, runner, log, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'get_project': PROJECT,
            'get_project_files': PROJECT_FILES,
            'get_experiments': EXPERIMENTS,
        }
        interceptor(PAYLOAD, monkeypatch)
        result = runner.invoke(cli, ['experiment', 'list'])
        assert result.exit_code == 0
        assert log.messages[0] == 'iris-1.csv-experiment'
        assert log.messages[-1] == '1 Experiment(s) listed'

    def test_start(self, runner, log, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'get_project': PROJECT,
            'get_project_files': PROJECT_FILES,
            'get_project_file': PROJECT_FILE,
            'get_experiments': EXPERIMENTS,
            'get_experiment_sessions': EXPERIMENT_SESSIONS,
            'create_experiment_session': EXPERIMENT_SESSION,
            'get_experiment_session': EXPERIMENT_SESSION,
            'update_experiment_session': EXPERIMENT_SESSION,
            'get_trials': TRIALS,
        }
        interceptor(PAYLOAD, monkeypatch)
        result = runner.invoke(cli, ['experiment', 'start'])
        assert result.exit_code == 0
        assert log.messages[0] == 'Started Experiment iris-1.csv-experiment search...'

    @pytest.mark.skip(reason="Make it work first, edge cases next")
    def test_start_without_target(self, runner, log, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'get_project_files': PROJECT_FILES,
            'get_experiments': EXPERIMENTS,
            'get_experiment_sessions': EXPERIMENT_SESSIONS,
            'get_trials': TRIALS,
        }
        interceptor(PAYLOAD, monkeypatch)
        # TODO: ensure cli throws error on trying to start exp w/o target
        result = runner.invoke(cli, ['experiment', 'start'])
        assert result.exit_code != 0
        assert log.messages[-1] == 'Please set target to build model.'

    def test_stop(self, runner, log, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'get_project_files': PROJECT_FILES,
            'get_experiments': EXPERIMENTS,
            'get_experiment_sessions': EXPERIMENT_SESSIONS,
            'update_experiment_session': EXPERIMENT_SESSION,
        }
        interceptor(PAYLOAD, monkeypatch)
        monkeypatch.setattr('auger.api.cloud.experiment_session.AugerExperimentSessionApi.status', lambda *a, **kw: 'started')
        result = runner.invoke(cli, ['experiment', 'stop'])
        assert result.exit_code == 0
        assert log.messages[0] == 'Search is stopped...'

    def test_leaderboard(self, runner, log, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'get_project_files': PROJECT_FILES,
            'get_experiments': EXPERIMENTS,
            'get_experiment_session': EXPERIMENT_SESSION,
            'get_experiment_sessions': EXPERIMENT_SESSIONS,
            'get_trials': TRIALS,
        }
        interceptor(PAYLOAD, monkeypatch)
        result = runner.invoke(cli, ['experiment', 'leaderboard'])
        assert result.exit_code == 0
        assert len(log.messages) == 44
        assert log.messages[-1] == 'Search is completed.'

    def test_history(self, runner, log, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'get_project_files': PROJECT_FILES,
            'get_experiments': EXPERIMENTS,
            'get_experiment_sessions': EXPERIMENT_SESSIONS,
        }
        interceptor(PAYLOAD, monkeypatch)
        result = runner.invoke(cli, ['experiment', 'history'])
        assert result.exit_code == 0
        assert (log.messages[0] ==
            '''run id: test_id_1, start time: 2019-06-26 22:00:00.405, '''
            '''status: completed''')
        assert 'run id: test_id_2' in log.messages[1]
