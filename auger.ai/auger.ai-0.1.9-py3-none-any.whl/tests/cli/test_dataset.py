from auger.cli.cli import cli
from auger.api.utils.config_yaml import ConfigYaml
from auger.api.cloud.project import AugerProjectApi
from .utils import interceptor, ORGANIZATIONS, PROJECTS, object_status_chain


class TestDataSetCLI():
    def test_list(self, runner, log, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'get_project_files': {
                'meta': {
                    'status': 200,
                    'pagination': {
                        'count': 2, 'offset': 0, 'total': 2, 'limit': 100}
                },
                'data': [
                {'id': 1, 'name': 'test_dataset1'},
                {'id': 2, 'name': 'test_dataset2'}
                ],
            }
        }
        interceptor(PAYLOAD, monkeypatch)
        result = runner.invoke(cli, ['dataset', 'list'])
        assert result.exit_code == 0
        assert log.messages[0] == 'test_dataset1'
        assert log.messages[1] == 'test_dataset2'
        assert log.messages[2] == '2 DataSet(s) listed'

    def test_create(self, runner, log, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'create_project_file_url': {'data': {}},
            'get_project_files': {
                'data': [{
                    'project_id': 1,
                    'url': 's3://iris.csv',
                    'name': 'iris-2.csv',
                }],
                'meta': {'pagination': {'offset': 0, 'total': 1, 'count': 1, 'limit': 100}, 'status': 200},
            },
            'get_project_file': {'data': {}},
            'create_project_file': {'data': {}}
        }
        interceptor(PAYLOAD, monkeypatch)
        object_status_chain(['processing', 'processed'], monkeypatch)
        monkeypatch.setattr(AugerProjectApi, 'is_running', lambda x: True)
        monkeypatch.setattr('auger.api.cloud.data_set.AugerDataSetApi._upload_to_cloud', lambda *args: 's3://iris.csv')
        result = runner.invoke(cli, ['dataset', 'create', 'iris.csv'])
        assert result.exit_code == 0
        assert log.messages[-1] == 'Created DataSet iris-1.csv'

    def test_delete(self, runner, log, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
            'get_project_files': {
                'meta': {
                    'status': 200,
                    'pagination': {
                        'count': 2, 'offset': 0, 'total': 2, 'limit': 100}
                },
                'data': [
                {'id': 1, 'name': 'test_dataset1'},
                {'id': 2, 'name': 'test_dataset2'}
                ],
            },
            'delete_project_file': {
                'data': {}
            }
        }
        interceptor(PAYLOAD, monkeypatch)
        result = runner.invoke(cli, ['dataset', 'delete', 'test_dataset1'])
        assert result.exit_code == 0
        assert 'Deleted dataset test_dataset1.csv'

    def test_select(self, runner, log, isolated, project, authenticated):
        config = ConfigYaml()
        config.load_from_file('auger.yaml')
        assert config.dataset == 'iris-1.csv'
        result = runner.invoke(cli, ['dataset', 'select', 'iris'])
        config.load_from_file('auger.yaml')
        assert config.dataset == 'iris'
        assert result.exit_code == 0
