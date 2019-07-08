import os
import yaml

from logging import getLogger

logger = getLogger(__name__)


class MockAppEngineEnvironment:
    @classmethod
    def load_app_yaml(cls, app_yaml_path):
        print('xxxx')
        with open(app_yaml_path, 'r+') as f:
            app_yaml = yaml.load(f, Loader=yaml.CLoader)

        if 'env_variables' not in app_yaml:
            print('not exists')
            logger.debug('"env_variables" doest not exists in app.yaml')
        else:
            print('exists')
            logger.debug('"env_variables" exists in app.yaml:')
            for key, value in app_yaml['env_variables'].items():
                os.environ[key] = str(value)
                logger.debug(f'* load "{key}"')
