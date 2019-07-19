#
# Copyright (c) 2016, deepsense.io
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import base64
import logging

from future.builtins import object
from requests_oauthlib import oauth2_session

from neptune.generated.swagger_client import ExperimentsBackups, models
from neptune.generated.swagger_client.models.experiment_state import ExperimentState
from neptune.internal.cli.commands.exceptions.data_exceptions import InsufficientFundsError
from neptune.internal.cli.commands.framework import CommandUnsuccessfulError
from neptune.internal.common.api.exceptions import NeptuneServerResponseErrorException
from neptune.internal.common.api.raw_requests import raw_http_get
from neptune.internal.common.api.retry_decorator import no_retry_by_default, retry_by_default
from neptune.internal.common.api.utils import REQUESTS_TIMEOUT, WithRetries
from neptune.internal.common.utils.compression import gzip_compress
from neptune.server import __api__ as server_api_prefix

oauth2_session.log.setLevel(logging.WARNING)


class JobApiService(object):
    def __init__(self, urls, requests_client, neptune_api_handler, retries_enabled, utilities_service):
        self._logger = logging.getLogger(__name__)
        self._urls = urls
        self._requests_client = requests_client
        self._api_handler = neptune_api_handler
        self._retries_enabled = retries_enabled
        self._utilities_service = utilities_service
        self._json_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    @no_retry_by_default
    def login(self, **options):
        return self._api_handler_with_options(**options).login()

    @no_retry_by_default
    def user_logged_to_cli(self, **options):
        try:
            return self._api_handler_with_options(**options).update_user_profile(
                models.UserProfileUpdate(has_logged_to_cli=True))
        except NeptuneServerResponseErrorException as e:
            # intentional, user login should not be interrupted by failing to update some misc internal settings
            self._logger.info("Unable to call user_logged_to_cli: %s", e)

    @retry_by_default
    def get_project_by_name(self, organization_name, project_name, **options):
        return self._api_handler_with_options(**options).get_project_by_name(organization_name=organization_name,
                                                                             project_name=project_name)

    @retry_by_default
    def guess_project(self, organization_name=None, project_key=None, **options):
        return self._api_handler_with_options(**options).guess_project(
            organization_name=organization_name,
            project_key=project_key)

    @retry_by_default
    def create_channel(self, experiment_id, channel_params, **options):
        return self._api_handler_with_options(**options).create_channel(experiment_id, channel_params.to_swagger())

    @retry_by_default
    def create_system_channel(self, experiment_id, channel_params, **options):
        return self._api_handler_with_options(**options).create_system_channel(
            experiment_id, channel_params.to_swagger())

    @retry_by_default
    def get_api_token(self, **options):
        return self._api_handler_with_options(**options).get_api_token()

    @no_retry_by_default
    def create_experiment(self, experiment_params, **options):
        experiment = self._api_handler_with_options(**options).create_experiment(experiment_params)
        self._logger.debug('Created experiment %s with tags: %s', experiment.id, experiment.tags)
        return experiment

    @no_retry_by_default
    def add_experiment_git_history(self, git_history_params, **options):
        return self._api_handler_with_options(**options).add_experiment_git_history(git_history_params)

    @no_retry_by_default
    def create_group(self, group_creation_params, **options):
        """
        :param group_creation_params: neptune.generated.swagger_client.GroupCreationParams
        :rtype: neptune.generated.swagger_client.Group
        """
        group = self._api_handler_with_options(**options).create_group(group_creation_params)
        return group

    @retry_by_default
    def get_group(self, group_id, **options):
        """
        :rtype: neptune.generated.swagger_client.Group
        """
        return self._api_handler_with_options(**options).get_group(group_id=group_id)

    @retry_by_default
    def ls_path(self, path, **options):
        return self._api_handler_with_options(**options).ls_path(path)

    @retry_by_default
    def download_path(self, session, http_url, path, **_):
        r = session.get(
            u"{}/{}/storage/download".format(
                http_url,
                server_api_prefix
            ),
            params={u"pathParam": path},
            stream=True
        )
        if r.status_code == 402:
            raise InsufficientFundsError()
        if r.status_code != 200:
            raise CommandUnsuccessfulError(u"Connection error")
        return r

    @retry_by_default
    def get_experiment(self, experiment_id, **options):
        return self._api_handler_with_options(**options).get_experiment(experiment_id=experiment_id)

    def get_experiments(self, params):
        """
        Get the list of experiments in the project. This request is not handled by Swagger because of costly
        type conversions from dictionaries to objects.
        :param params: A dictionary of GET request parameters. Must contain the projectId parameter.
        :rtype: list
        """
        return raw_http_get(
            session=self._requests_client,
            url=self._urls.get_experiments_url,
            params=params,
            headers=self._json_headers,
            timeout=REQUESTS_TIMEOUT
        ).json()

    @retry_by_default
    def update_experiment(self, experiment_id, edit_experiment_params, **options):
        experiment = self._api_handler_with_options(**options).update_experiment(experiment_id, edit_experiment_params)
        return experiment

    @retry_by_default
    def mark_experiment_succeeded(self, experiment, **options):
        completed_params = models.CompletedExperimentParams()
        completed_params.state = ExperimentState.succeeded
        completed_params.traceback = ''
        experiment = self._api_handler_with_options(**options).mark_experiment_completed(experiment.id,
                                                                                         completed_params)
        self._logger.debug('Marked experiment %s as succeeded', experiment.id)
        return experiment

    @retry_by_default
    def mark_experiment_failed(self, experiment, traceback, **options):
        completed_params = models.CompletedExperimentParams()
        completed_params.state = ExperimentState.failed
        completed_params.traceback = traceback
        experiment = self._api_handler_with_options(**options).mark_experiment_completed(experiment.id,
                                                                                         completed_params)
        self._logger.debug('Marked experiment %s as failed', experiment.id)
        return experiment

    @retry_by_default
    def mark_experiment_running(self,
                                experiment_id,
                                run_command=None,
                                **options):
        running_experiment_params = models.RunningExperimentParams(run_command=run_command)

        experiment = self._api_handler_with_options(**options).mark_experiment_running(experiment_id,
                                                                                       running_experiment_params)
        self._logger.debug('Marked experiment %s as running', experiment_id)
        return experiment

    @retry_by_default
    def mark_experiment_aborted(self, experiment, **options):
        experiments = self._api_handler_with_options(**options).abort_experiments(experiment)
        self._logger.debug('Marked experiment %s as aborted', experiments[0].experiment_id)
        return experiments[0].experiment_id

    @retry_by_default
    def mark_experiment_cleaning(self, experiment, **options):
        experiment = self._api_handler_with_options(**options).mark_experiment_cleaning(experiment.id)
        self._logger.debug('Marked experiment %s as cleaning', experiment.id)
        return experiment

    @retry_by_default
    def mark_experiment_waiting(self, experiment_id, **options):
        experiment = self._api_handler_with_options(**options).mark_experiment_waiting(experiment_id)
        self._logger.debug('Marked experiment %s as waiting', experiment.id)
        return experiment

    @retry_by_default
    def mark_experiment_initializing(self, experiment_id, **options):
        experiment = self._api_handler_with_options(**options).mark_experiment_initializing(experiment_id)
        self._logger.debug('Marked experiment %s as initializing', experiment.id)
        return experiment

    @retry_by_default
    def send_channel_values(self, experiment_id, channel_values, **options):
        self._logger.debug('Sending channel values %s.', experiment_id)
        return self._api_handler_with_options(**options).post_channel_values(
            experiment_id=experiment_id, channels_values=channel_values)

    @retry_by_default
    def ping_experiment(self, experiment_id, **options):
        self._api_handler_with_options(**options).ping_experiment(experiment_id)
        self._logger.debug('Pinged experiment %s', experiment_id)

    @retry_by_default
    def abort_experiments(self, experiment_ids, **options):
        return self._api_handler_with_options(**options).abort_experiments(experiment_ids=experiment_ids)

    @retry_by_default
    def get_execution_info(self, experiment_id, **options):
        return self._api_handler_with_options(**options).get_execution_info(experiment_id)

    @retry_by_default
    def get_experiment_backups(self, experiment_id, **options):
        return self._api_handler_with_options(**options).get_experiment_backups(experiment_id)

    @retry_by_default
    def mark_action_invocation_succeeded(self, experiment_id, action_id, action_invocation_id, result, **options):
        self._mark_action_invocation_completed(
            experiment_id, action_id, action_invocation_id, models.CompletedActionParams(result=result), **options)

    @retry_by_default
    def mark_action_invocation_failed(self, experiment_id, action_id, action_invocation_id, traceback, **options):
        self._mark_action_invocation_completed(
            experiment_id,
            action_id,
            action_invocation_id,
            models.CompletedActionParams(traceback=traceback),
            **options)

    def _mark_action_invocation_completed(self, experiment_id, action_id, action_invocation_id, params, **options):
        status = 'succeeded' if params.traceback is None else 'failed'
        self._logger.debug('Marking action invocation %s for action %s of experiment %s as %s.',
                           action_invocation_id, action_id, experiment_id, status)
        self._api_handler_with_options(**options).mark_action_invocation_completed(
            experiment_id, action_id, action_invocation_id, params)

    @retry_by_default
    def put_tensorflow_graph(self, experiment_id, tensorflow_graph, **options):

        # Bytes are needed for compression.
        bingraph = tensorflow_graph.value.encode('UTF-8')

        compressed_graph_data = base64.b64encode(gzip_compress(bingraph))

        # Bytes are needed for json.dumps.
        data = compressed_graph_data.decode('UTF-8')

        compressed_tensorflow_graph = models.CompressedTensorflowGraph(
            id=tensorflow_graph.id, value=data)
        self._api_handler_with_options(**options).put_tensorflow_graph(
            experiment_id, compressed_tensorflow_graph)

    @retry_by_default
    def delete_channel(self, experiment_id, channel_id, **options):
        return self._api_handler_with_options(**options).delete_channel(
            experiment_id=experiment_id,
            channel_id=channel_id)

    @retry_by_default
    def delete_channel_values(self, experiment_id, channel_id, **options):
        return self._api_handler_with_options(**options).delete_channel_values(
            experiment_id=experiment_id,
            channel_id=channel_id)

    @staticmethod
    def _upload_loop_chunk(fun, part, data, **kwargs):
        part_to_send = part.get_data()
        if part.end:
            binary_range = "bytes=%d-%d/%d" % (part.start, part.end - 1, data.length)
        else:
            binary_range = "bytes=%d-/%d" % (part.start, data.length)
        return fun(binary_data=part_to_send,
                   binary_filename=data.filename,
                   binary_range=binary_range,
                   binary_permissions=data.permissions,
                   **kwargs)

    def _upload_loop_(self, fun, data, checksums=None, **kwargs):
        ret = None
        for part in data.generate():
            skip = False
            if checksums and part.start in checksums:
                skip = checksums[part.start].checksum == part.md5()

            if not skip:
                ret = self._upload_loop_chunk(fun, part, data, **kwargs)
            else:
                part.skip()
        data.close()
        return ret

    @retry_by_default
    def upload_data(self, project_id, data, **options):
        chunks = self.verify_upload_data(project_id, data.filename)
        checksums = dict([(c.start, c) for c in chunks.checksums])

        return self._upload_loop_(self._api_handler_with_options(**options).upload_data,
                                  data=data,
                                  project_id=project_id,
                                  checksums=checksums)

    @retry_by_default
    def upload_data_as_tarstream(self, project_id, data, **options):
        return self._api_handler_with_options(**options).upload_data_as_tarstream(
            project_id=project_id,
            binary_data=data)

    @retry_by_default
    def verify_upload_data(self, project_id, path, **options):
        return self._api_handler_with_options(**options).verify_upload_data(
            project_id=project_id,
            path=path)

    @retry_by_default
    def ls_data(self, project_id, path_param, recursive, **options):
        return self._api_handler_with_options(**options).ls_data(
            project_id=project_id, path_param=path_param, recursive=recursive
        )

    @retry_by_default
    def rm_data(self, project_id, path_param, recursive, **options):
        return self._api_handler_with_options(**options).rm_data(project_id=project_id, path_param=path_param,
                                                                 recursive=recursive)

    @retry_by_default
    def upload_experiment_source(self, experiment_id, data, **options):
        return self._upload_loop_(self._api_handler_with_options(**options).upload_experiment_source,
                                  data=data,
                                  experiment_id=experiment_id)

    @retry_by_default
    def upload_experiment_source_as_tarstream(self, experiment_id, data, **options):
        return self._api_handler_with_options(**options).upload_experiment_source_as_tarstream(
            experiment_id=experiment_id,
            binary_data=data)

    @retry_by_default
    def finalize_experiment_upload(self, experiment_id, target_experiment_ids, **options):
        return self._api_handler_with_options(**options).finalize_experiment_upload(
            experiment_id=experiment_id,
            target_experiment_ids=target_experiment_ids)

    @retry_by_default
    def upload_experiment_stdout(self, experiment_id, data, **options):
        return self._upload_loop_(self._api_handler_with_options(**options).upload_experiment_stdout,
                                  data=data,
                                  experiment_id=experiment_id)

    @retry_by_default
    def upload_experiment_stderr(self, experiment_id, data, **options):
        return self._upload_loop_(self._api_handler_with_options(**options).upload_experiment_stderr,
                                  data=data,
                                  experiment_id=experiment_id)

    @retry_by_default
    def upload_experiment_output(self, experiment_id, data, **options):
        return self._upload_loop_(self._api_handler_with_options(**options).upload_experiment_output,
                                  data=data,
                                  experiment_id=experiment_id)

    @retry_by_default
    def extract_experiment_output(self, experiment_id, data, **options):
        return self._api_handler_with_options(**options).upload_experiment_output_as_tarstream(
            experiment_id=experiment_id,
            binary_data=data)

    @retry_by_default
    def upload_experiment_backups(self, experiment_id, data, **options):
        return self._upload_loop_(self._api_handler_with_options(**options).upload_experiment_backups,
                                  data=data,
                                  experiment_id=experiment_id)

    @retry_by_default
    def add_experiments_backups(self, experiment_ids, globs, **options):
        return self._api_handler_with_options(**options).add_experiments_backups(
            ExperimentsBackups(experiment_ids=experiment_ids, globs=globs))

    @retry_by_default
    def list_environments(self, **options):
        return self._api_handler_with_options(**options).list_environments()

    def _api_handler_with_options(self, **options_dict):
        if self._retries_enabled and options_dict.get(u'with_retries'):
            return WithRetries(self._api_handler)
        else:
            return self._api_handler

    @retry_by_default
    def create_system_metric(self, experiment_id, system_metric_params, **options):
        return self._api_handler_with_options(**options).create_system_metric(experiment_id, system_metric_params)

    @retry_by_default
    def send_system_metric_values(self, experiment_id, metric_values, **options):
        return self._api_handler_with_options(**options).post_system_metric_values(experiment_id, metric_values)
