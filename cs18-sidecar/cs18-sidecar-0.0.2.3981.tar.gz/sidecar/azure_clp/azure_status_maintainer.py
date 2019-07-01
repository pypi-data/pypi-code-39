import threading
from datetime import datetime
from typing import List

from retrying import retry

from sidecar.azure_clp.data_store_service import DataStoreService
from sidecar.azure_clp.retrying_helpers import retry_if_connection_error, retry_if_result_none_or_empty
from sidecar.const import Const
from sidecar.status_maintainer import StatusMaintainer
from logging import Logger
from sidecar.sandbox_error import SandboxError




class AzureStatusMaintainer(StatusMaintainer):
    ROOT_SPEC_KEY = "spec"
    EXPECTED_APPS_KEY = "expected_apps"
    ROOT_APPS_KEY = "apps"
    INSTANCES_KEY = "instances"
    ROOT_SERVICES_KEY = "services"

    def __init__(self, data_store_service: DataStoreService, sandbox_id: str, logger: Logger):
        super().__init__(logger)
        self._data_store_service = data_store_service
        self._sandbox_id = sandbox_id
        self._lock = threading.RLock()

        self._cached_realtime_apps = None
        self._cached_realtime_services = None
        self._cached_spec = None
        self._cached_sandbox_errors = []

        self._cache_sandbox_data()

    def _cache_sandbox_data(self):
        sandbox_document = self._get_sandbox_document_with_retries()
        if not sandbox_document:
            raise Exception("Failed to get sandbox data from cosmos_db after 5 retries")

        self._cached_realtime_apps = sandbox_document[self.ROOT_APPS_KEY]
        self._cached_realtime_services = sandbox_document[self.ROOT_SERVICES_KEY]
        self._cached_spec = sandbox_document[self.ROOT_SPEC_KEY]
        # the get and [] is for backward compatibility (so that if there is a sandbox that don't have the
        # item SANDBOX_ERRORS in the DB we will return [] and not get Noun)
        self._cached_sandbox_errors = sandbox_document.get(Const.SANDBOX_ERRORS, [])

    @retry(stop_max_attempt_number=5, wait_fixed=1000, retry_on_result=retry_if_result_none_or_empty,
           retry_on_exception=retry_if_connection_error)
    def _get_sandbox_document_with_retries(self):
        return self._data_store_service.find_data_by_id(data_id=self._sandbox_id)

    def _construct_instances_key_path(self, instance_logical_id):
        return '{apps_key}.{instance_logical_id}.{instances_key}'.format(apps_key=self.ROOT_APPS_KEY,
                                                                         instance_logical_id=instance_logical_id,
                                                                         instances_key=self.INSTANCES_KEY)

    def update_app_instance_status(self, instance_logical_id, instance_id, app_name, status):
        with self._lock:
            instances_under_logical_id = self._cached_realtime_apps[instance_logical_id][self.INSTANCES_KEY]
            apps_under_instance_id = instances_under_logical_id.setdefault(instance_id, {"apps": {}})["apps"]
            app_details = apps_under_instance_id.setdefault(app_name, {})
            app_details[Const.APP_STATUS_TAG] = status
            self._cached_realtime_apps[instance_logical_id][self.INSTANCES_KEY] = instances_under_logical_id

            self._data_store_service.update_data(data_id=self._sandbox_id,
                                                 data=self._cached_realtime_apps,
                                                 column_name=self.ROOT_APPS_KEY)

    def get_app_names_on_instance(self, instance_logical_id: str) -> List[str]:
        return self._cached_spec[self.EXPECTED_APPS_KEY][instance_logical_id]["apps"]

    def update_sandbox_end_status(self, sandbox_deployment_end_status: str):
        # assume that DB-level lock is good enough here
        self._data_store_service.update_data(data_id=self._sandbox_id,
                                             data=sandbox_deployment_end_status,
                                             column_name=Const.SANDBOX_DEPLOYMENT_END_STATUS)

        self._data_store_service.update_data(data_id=self._sandbox_id,
                                             data=sandbox_deployment_end_status,
                                             column_name=Const.SANDBOX_DEPLOYMENT_END_STATUS_v2)

    def update_sandbox_start_status(self, sandbox_start_time: datetime):
        # assume that DB-level lock is good enough here

        # todo gil:add update data bulk
        self._data_store_service.update_data(data_id=self._sandbox_id,
                                             data=str(sandbox_start_time),
                                             column_name=Const.SANDBOX_START_TIME)

        self._data_store_service.update_data(data_id=self._sandbox_id,
                                             data=str(sandbox_start_time),
                                             column_name=Const.SANDBOX_START_TIME_v2)

    def update_service_status(self, name: str, status: str):
        self._cached_realtime_services[name]["status"] = status
        self._data_store_service.update_data(data_id=self._sandbox_id,
                                             data=self._cached_realtime_services,
                                             column_name=self.ROOT_SERVICES_KEY)

    def update_lazy_load_artifacts_waiting(self, value: bool):
        self._data_store_service.update_data(data_id=self._sandbox_id,
                                             data=bool(value),
                                             column_name=Const.LAZY_LOAD_ARTIFACTS_WAITING)

    def update_sandbox_errors(self, errors: List[SandboxError]):
        with self._lock:
            self._cached_sandbox_errors = [{"message": error.message, "code": error.code, "time": error.time} for error in errors]

            self._data_store_service.update_data(data_id=self._sandbox_id,
                                                 data=self._cached_sandbox_errors,
                                                 column_name=Const.SANDBOX_ERRORS)

    def get_sandbox_errors(self) -> List[SandboxError]:
        errors = []
        for error in self._cached_sandbox_errors:
            errors.append(SandboxError(message=str(error["message"]),
                                       code=str(error["code"]),
                                       time=str(error["time"])))
        return errors


    def update_service_outputs(self, name: str, outputs: {}):
        self._cached_realtime_services[name]["outputs"] = outputs
        self._data_store_service.update_data(data_id=self._sandbox_id,
                                             data=self._cached_realtime_services,
                                             column_name=self.ROOT_SERVICES_KEY)

    def get_service_deployment_outputs(self, service_name: str) -> {}:
        service = self._cached_realtime_services.get(service_name, None)
        if service:
            return service.get("outputs", {})
        raise Exception(f"could not find service with name '{service_name}'")

    def update_app_instance_deployment_outputs(self, instance_logical_id, instance_id, app_name, outputs: {}):
        with self._lock:
            instances_under_logical_id = self._cached_realtime_apps[instance_logical_id][self.INSTANCES_KEY]
            apps_under_instance_id = instances_under_logical_id.setdefault(instance_id, {"apps": {}})["apps"]

            app_details = apps_under_instance_id.setdefault(app_name, {})
            app_details['outputs'] = outputs
            self._cached_realtime_apps[instance_logical_id][self.INSTANCES_KEY] = instances_under_logical_id

            self._data_store_service.update_data(data_id=self._sandbox_id,
                                                 data=self._cached_realtime_apps,
                                                 column_name=self.ROOT_APPS_KEY)

    def get_app_deployment_outputs(self, app_name: str) -> {}:
        app_details = self._get_first_application(app_name)
        if app_details:
            return app_details.get('outputs', {})
        raise Exception(f"could not find application with name '{app_name}'")

    def _get_first_application(self, app_name: str):
        for logical_id, logical_details in self._cached_realtime_apps.items():
            for instance_id, instance_json in logical_details[self.INSTANCES_KEY].items():
                for name, app_details in instance_json['apps'].items():
                    if name == app_name:
                        return app_details
        return None
