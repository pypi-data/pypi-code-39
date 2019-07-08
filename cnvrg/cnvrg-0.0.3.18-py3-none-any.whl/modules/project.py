import os
import yaml
from cnvrg.helpers.apis_helper import post as apis_post, get as apis_get, credentials
from cnvrg.modules.cnvrg_files import CnvrgFiles
from cnvrg.modules.errors import CnvrgError
import cnvrg.helpers.config_helper as config_helper
import cnvrg.helpers.param_build_helper as param_build_helper
from cnvrg.helpers.url_builder_helper import url_join

class Project(CnvrgFiles):
    def __init__(self, project=None, project_url=None, working_dir=None):
        if project_url:
            owner_slug, project_slug = Project.get_owner_and_project_from_url(project_url)
        else:
            owner_slug, project_slug = param_build_helper.parse_params(project, param_build_helper.PROJECT, working_dir=working_dir)
        self.__owner = owner_slug or credentials.owner
        self.__project = project_slug

        in_dir = config_helper.is_in_dir(config_helper.CONFIG_TYPE_PROJECT, project_slug, working_dir)
        super(Project, self).__init__()
        if in_dir:
            self._set_working_dir(config_helper.find_config_dir(path=working_dir))
            self.in_dir = True
        elif not self.__project or not self.__owner:
            raise CnvrgError("Cant init project without params and outside project directory")

    def __load_defaults(self):
        self.image = 'cnvrg'
        self.default_template = 'medium'

    def get_base_url(self):
        return "users/{owner}/projects/{project}".format(owner=self.__owner, project=self.__project)

    def _default_config(self):
        return {
            "project": self.__project,
            "owner": self.__owner,
            "commit": None
        }

    def get_project_name(self):
        return self.__project

    def get_output_dir(self):
        return self.get_working_dir()

    def run_experiment(self, cmd, **kwargs):
        resp = apis_post(url_join(self.get_base_url(), "experiments"), data={"cmd": cmd, **kwargs})
        exp = resp.get("experiment")
        if not exp:
            raise CnvrgError("Cant run experiment")
        return exp

    #
    # def create_experiment(self, command, commit='latest', image=None, templates=None, datasets=None, title=None):
    #     experiment_data = {
    #         "cmd": command,
    #         "commit": commit,
    #         "image": image,
    #         "templates": templates,
    #         "datasets": datasets,
    #         "title": title,
    #     }
    #     return apis_post(url_join(self.__base_url(), "experiments"), data=experiment_data)
    #
    # def get_experiment(self, id):
    #     return apis_get(url_join(self.__base_url(),"experiments", id))
    #
    #
    #
    # def create_endpoint(self, name="testEndpoint", min_replica=1, max_replica=1, templates=None, commit="latest", function="predict", file="deploy.py"):
    #     endpoint = {
    #         "name": name,
    #         "min_replica": min_replica,
    #         "max_replica": max_replica,
    #         "templates": templates,
    #         "models": [{
    #             "commit": commit,
    #             "function":function,
    #             "file": file
    #         }]
    #     }
    #     return apis_post(url_join(self.__base_url(), "endpoints"), data=endpoint)
    #
    #
    #
    #
