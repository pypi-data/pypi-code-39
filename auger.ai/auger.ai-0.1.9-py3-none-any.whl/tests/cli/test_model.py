import os

import pytest

from auger.cli.cli import cli
from .utils import interceptor, object_status_chain, ORGANIZATIONS, PROJECTS


class TestModelCLI():
    def test_deploy_locally(self, log, runner, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
        }
        interceptor(PAYLOAD, monkeypatch)
        object_status_chain(['undeployed', 'deployed', 'deploying', 'running'], monkeypatch)
        monkeypatch.setattr('auger.api.mparts.deploy.ModelDeploy._docker_pull_image', lambda self: 'experimental')
        monkeypatch.setattr('auger.api.mparts.deploy.ModelDeploy._start_project', lambda self: None)
        os.remove('models/model-87C81FE615DE46D.zip')
        # FIXME: let AugerPipelineFileApi do it's work
        monkeypatch.setattr('auger.api.cloud.pipeline_file.AugerPipelineFileApi.create', lambda self, model_id: {'signed_s3_model_path': 'None'})
        monkeypatch.setattr('auger.api.cloud.pipeline_file.AugerPipelineFileApi.download', lambda *a, **kw: 'models/export-%s.zip' % '87C81FE615DE46D')
        result = runner.invoke(cli, ['model', 'deploy', '--locally', '87C81FE615DE46D'])
        assert result.exit_code == 0
        assert log.messages[0] == 'Downloading model 87C81FE615DE46D'
        assert log.messages[1] == 'Downloaded model to models/export-87C81FE615DE46D.zip'
        assert log.messages[2] == 'Pulling docker image required to predict'


    @pytest.mark.skip(reason="not implemented on server-side currently")
    def test_deploy_remoteley(self, log, runner, project, authenticated, monkeypatch):
        result = runner.invoke(cli, ['model', 'deploy'])
        pass

    def test_predict_locally(self, log, runner, project, authenticated, monkeypatch):
        PAYLOAD = {
            'get_organizations': ORGANIZATIONS,
            'get_projects': PROJECTS,
        }
        interceptor(PAYLOAD, monkeypatch)
        monkeypatch.setattr('subprocess.check_output', lambda *a, **kw: 0)
        result = runner.invoke(cli, ['model', 'predict', '-m', '87C81FE615DE46D', 'iris.csv', '--locally'])
        assert result.exit_code == 0
        assert log.messages[0] == 'Predicting on data in iris.csv'
        assert log.messages[1] == 'Running model in deeplearninc/auger-ml-worker:experimental'
        dirname = os.path.dirname(os.getcwd())
        assert log.messages[2] == 'Predictions stored in %s' % os.path.join('tmp', dirname, 'test_project', 'iris_predicted.csv')


    @pytest.mark.skip(reason="not implemented on server-side currently")
    def test_predict_remoteley(self, log, runner, project, authenticated, monkeypatch):
        result = runner.invoke(cli, ['model', 'predict', 'iris.csv'])
        pass
