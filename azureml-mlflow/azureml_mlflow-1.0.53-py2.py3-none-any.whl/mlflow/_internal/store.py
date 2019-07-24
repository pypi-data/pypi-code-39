# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""**AzureMLflowStore** provides a class to read and record run metrics and artifacts on Azure via MLflow."""

import logging
import os
import time

from functools import wraps

from mlflow.store.rest_store import RestStore
from mlflow.utils.rest_utils import MlflowHostCreds
from mlflow.exceptions import RestException

from azureml.core.authentication import AzureMLTokenAuthentication

from azureml._restclient.clientbase import DEFAULT_BACKOFF, DEFAULT_RETRIES
from azureml._restclient.run_client import RunClient

logger = logging.getLogger(__name__)

PARAM_PREFIX = "azureml.param."

_EXPERIMENT_NAME_ENV_VAR = "MLFLOW_EXPERIMENT_NAME"
_MLFLOW_RUN_ID_ENV_VAR = "MLFLOW_RUN_ID"


class AzureMLRestStore(RestStore):
    """
    Client for a remote tracking server accessed via REST API calls.

    :param service_context: Service context for the AzureML workspace
    :type service_context: azureml._restclient.service_context.ServiceContext
    """

    def __init__(self, service_context):
        """
        Construct an AzureMLRestStore object.

        :param service_context: Service context for the AzureML workspace
        :type service_context: azureml._restclient.service_context.ServiceContext
        """
        logger.debug("Initializing the AzureMLRestStore")
        self.service_context = service_context
        self.get_host_creds = self.get_host_credentials
        super(AzureMLRestStore, self).__init__(self.get_host_creds)

    def get_host_credentials(self):
        """
        Construct a MlflowHostCreds to be used for obtaining fresh credentials and the host url.

        :return: The host and credential for rest calls.
        :rtype: mlflow.utils.rest_utils.MlflowHostCreds
        """
        return MlflowHostCreds(
            self.service_context._get_run_history_url() +
            "/history/v1.0" + self.service_context._get_workspace_scope(),
            token=self.service_context.get_auth().get_authentication_header()["Authorization"][7:])

    @wraps(RestStore._call_endpoint)
    def _call_endpoint(self, *args, **kwargs):
        total_retry = DEFAULT_RETRIES
        backoff = DEFAULT_BACKOFF
        for i in range(total_retry):
            try:
                return super(AzureMLRestStore, self)._call_endpoint(*args, **kwargs)
            except RestException as rest_exception:
                more_retries_left = i < total_retry - 1
                is_throttled = rest_exception.json.get("error", {"code": 0}).get("code") == "RequestThrottled"
                if more_retries_left and is_throttled:
                    logger.debug("There were too many requests. Try again soon.")
                    self._wait_for_retry(backoff, i, total_retry)
                else:
                    raise

    @classmethod
    def _wait_for_retry(cls, back_off, left_retry, total_retry):
        delay = back_off * 2 ** (total_retry - left_retry - 1)
        time.sleep(delay)

    def _update_authentication(self, run_id, experiment_name):
        """
        Helper function for initializing the AzureMLTokenAuthentication class
        to avoid expiring AAD tokens. Also initializes the AzureML token refresher.

        :param run_id: The run id for the Run.
        :type run_id: str
        :param experiment_name: The name of the experiment.
        :type experiment_name: str
        """
        run_client = RunClient(self.service_context, experiment_name, run_id)
        token = run_client.get_token().token
        auth = AzureMLTokenAuthentication.create(
            azureml_access_token=token,
            expiry_time=None,
            host=self.service_context._get_run_history_url(),
            subscription_id=self.service_context.subscription_id,
            resource_group_name=self.service_context.resource_group_name,
            workspace_name=self.service_context.workspace_name,
            experiment_name=experiment_name,
            run_id=run_id
        )
        self.service_context._authentication = auth

    @wraps(RestStore.create_run)
    def create_run(self, *args, **kwargs):
        auth = self.service_context.get_auth()
        logger.debug("Creating an Mlflow run with {} auth token".format(auth.__class__.__name__))
        run = super(AzureMLRestStore, self).create_run(*args, **kwargs)
        if not isinstance(auth, AzureMLTokenAuthentication) and _EXPERIMENT_NAME_ENV_VAR in os.environ:
            self._update_authentication(run.info.run_id, os.environ[_EXPERIMENT_NAME_ENV_VAR])

        return run

    def get_experiment_by_name(self, experiment_name, *args, **kwargs):
        """
        Fetch the experiment by name from the backend store.

        :param experiment_name: Name of experiment

        :return: A single :py:class:`mlflow.entities.Experiment` object if it exists.
        """
        if len(args) + len(kwargs) > 0:
            logger.debug("Found unsupported inputs to {}.get_experiment_by_name: args {} and kwargs {}. "
                         "The inputs will be ignored.".format(self.__class__.__name__, args, kwargs))
        experiment_id = None
        try:
            from azureml._restclient.workspace_client import WorkspaceClient
            workspace_client = WorkspaceClient(self.service_context)
            azureml_experiment = workspace_client.get_experiment(experiment_name)
            experiment_id = azureml_experiment.experiment_id
        except Exception as e:
            logger.debug("Could not load experiment '{}' with exception: {}".format(experiment_name, e))
        return None if experiment_id is None else self.get_experiment(experiment_id)
