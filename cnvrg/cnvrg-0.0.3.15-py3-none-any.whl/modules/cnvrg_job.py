from cnvrg.modules.base_module import CnvrgBase
from cnvrg.modules.project import Project
import cnvrg.helpers.apis_helper as apis_helper
import cnvrg.helpers.string_helper as string_helper
import os
import cnvrg.helpers.env_helper as env_helper
import cnvrg.helpers.config_helper as config_helper
import cnvrg.helpers.time_helper as time_helper
from cnvrg.modules.errors import UserError
from cnvrg.helpers.url_builder_helper import url_join



LOGS_TYPE_OUTPUT = "output"
LOGS_TYPE_ERROR = "error"
LOGS_TYPE_INFO = "info"
LOGS_TYPE_WARNING = "warning"
MAX_LOGS_PER_SEND = 400

class CnvrgJob(CnvrgBase):
    def __init__(self, slug=None, job_type=None, project=None):
        self.job_slug = slug or env_helper.CURRENT_JOB_ID
        self.job_type = job_type or env_helper.CURRENT_JOB_TYPE
        if not project:
            if not config_helper.config_type() == config_helper.CONFIG_TYPE_PROJECT:
                raise UserError(
                    "Cant create an experiment without a project, please pass a project or cd into cnvrg project dir")
            project = Project()
        self.project = project


    def _base_job_url(self):
        return url_join(
            #### hackish :D
            self.project.get_base_url(),"jobs", string_helper.to_snake_case(self.job_type), self.job_slug
        )


    def send_util(self, utilization):
        apis_helper.post(url_join(self._base_job_url(), "utilization"), data=[utilization])


    def log(self, logs, log_type=LOGS_TYPE_OUTPUT):
        for i in range(0, len(logs), env_helper.MAX_LOGS_PER_SEND):
            apis_helper.post(url_join(self._base_job_url(), "log"), data={"logs": logs[i:i + env_helper.MAX_LOGS_PER_SEND], "log_level": log_type, "timestamp": time_helper.now_as_string()})
