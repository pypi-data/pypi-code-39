from auger.cli.cli import cli
from auger.api.cloud.rest_api import RestApi
from auger.api.utils.config_yaml import ConfigYaml
from auger.api.credentials import Credentials

from .utils import interceptor, object_status_chain, ORGANIZATIONS, PROJECTS


class TestProjectCLI():
    def test_list(self, runner, log, monkeypatch, authenticated):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
        }
        interceptor(PAYLOAD, monkeypatch)
        result = runner.invoke(cli, ['project', 'list'])
        assert result.exit_code == 0
        assert log.messages[0] == 'project_1'
        assert log.messages[1] == 'test_project'
        assert log.messages[2] == '2 Project(s) listed'

    def test_create(self, log, runner, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'create_project': {
                'data': {
                    'id': 1,
                    'name': 'igor-test',
                },
            },
            'get_project': {
                'data': {
                    'id': 1,
                    'name': 'igor-test',
                },
            }
        }
        interceptor(PAYLOAD, monkeypatch)
        result = runner.invoke(cli, ['project', 'create', 'test'])
        assert result.exit_code == 0
        assert log.messages[-1] == 'Created Project test'

    def test_delete(self, log, runner, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'delete_project': {
                'data': {}
            }
        }
        interceptor(PAYLOAD, monkeypatch)
        result = runner.invoke(cli, ['project', 'delete', 'test_project'])
        assert result.exit_code == 0
        assert log.messages[-1] == 'Deleted Project test_project'

    def test_select(self, log, runner, project, authenticated):
        config_file = 'auger.yaml'
        config = ConfigYaml()
        config.load_from_file(config_file)
        assert config.project == 'test_project'
        result = runner.invoke(cli, ['project', 'select', 'another_project'])
        assert result.exit_code == 0
        config.load_from_file(config_file)
        assert config.project == 'another_project'
        assert log.messages[-1] == 'Selected Project another_project'

    def test_start(self, log, runner, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_organization': {'data': {} },
            'get_projects': PROJECTS,
            'get_project': {'data': {}},
            'update_project': {'data': {}},
            'deploy_project': {'data': {}}
        }
        interceptor(PAYLOAD, monkeypatch)
        object_status_chain(['deploying', 'deployed', 'running'], monkeypatch)
        result = runner.invoke(cli, ['project', 'start'])
        assert result.exit_code == 0
        assert 'Starting Project...' in log.messages
        assert 'Started Project test_project' in log.messages

    def test_stop(self, log, runner, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'get_project': {
                'data': {
                    'id': 1,
                    'name': 'test_project',
                    'status': 'running',
                },
                'meta': {'status': 404},
            },
            'undeploy_project': {'meta': {'status': 200}, 'data': {}},
        }
        interceptor(PAYLOAD, monkeypatch)
        object_status_chain(['running', 'undeploying', 'undeployed'], monkeypatch)
        monkeypatch.setattr('auger.api.cloud.project.AugerProjectApi.status', lambda x: 'undeployed')
        result = runner.invoke(cli, ['project', 'stop'])
        assert result.exit_code == 0
        assert 'Stopping Project...' in log.messages
        assert 'Stopped Project test_project' in log.messages
