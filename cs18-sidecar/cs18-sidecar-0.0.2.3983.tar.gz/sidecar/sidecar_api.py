import logging.config
import os
from datetime import datetime
from logging import Logger

import requests
from blinker import Namespace
from blinker import signal
from flask import Flask, request, Request
from jsonpickle import json
from werkzeug.exceptions import HTTPException

from sidecar.app_instance_config_status_event_reporter import AppInstanceConfigStatusEventReporter
from sidecar.app_instance_event_handler import AppInstanceEventHandler
from sidecar.app_instance_events import AppInstanceEvents
from sidecar.app_instance_identifier import AppInstanceIdentifier
from sidecar.app_instance_identifier_creator import IAppInstanceIdentifierCreator
from sidecar.app_services.app_service import K8sAppService, AWSAppService, AppService
from sidecar.app_status_maintainer import AppStatusMaintainer
from sidecar.apps_configuration_end_tracker import AppsConfigurationEndTracker
from sidecar.aws_app_instance_identifier_creator import AwsAppInstanceIdentifierCreator
from sidecar.aws_app_instance_service import AwsAppInstanceService
from sidecar.aws_sandbox_deployment_end_updater import AwsSandboxDeploymentEndUpdater
from sidecar.aws_sandbox_start_time_updater import AwsSandboxStartTimeUpdater
from sidecar.aws_sandbox_terminating_query import AwsSandboxTerminatingQuery
from sidecar.aws_session import AwsSession
from sidecar.aws_status_maintainer import AWSStatusMaintainer
from sidecar.azure_clp.azure_sidecar_api_initializer import AzureSidecarApiInitializer
from sidecar.cloud_logger import FileLogger
from sidecar.cloud_logger.file_logger import FakeFileLogger, ICloudLogger
from sidecar.cloud_logger.logs import AppLogEntry
from sidecar.configuration_start_policy import ConfigurationStartPolicy
from sidecar.const import Const, DateTimeProvider, Signals
from sidecar.file_system import FileSystemService
from sidecar.filters import LoggingFilter
from sidecar.health_check.app_health_check_monitor import AppHealthCheckMonitor, AppHealthCheckConfiguration
from sidecar.health_check.app_health_check_state import AppHealthCheckState
from sidecar.health_check.app_instance_health_check_monitor import AppInstanceHealthCheckMonitor
from sidecar.health_check.health_check_executor import HealthCheckExecutor
from sidecar.health_check.health_check_executor_logger import AppHealthCheckExecutorLogger, \
    AppInstanceHealthCheckExecutorLogger
from sidecar.health_check.health_check_preparer import HealthCheckPreparer
from sidecar.kub_api_service import KubApiService
from sidecar.kub_app_instance_identifier_creator import KubAppInstanceIdentifierCreator
from sidecar.kub_app_instance_service import KubAppInstanceService
from sidecar.kub_sandbox_deployment_end_updater import KubSandboxDeploymentEndUpdater
from sidecar.kub_sandbox_start_time_updater import KubSandboxStartTimeUpdater
from sidecar.kub_token_provider import KubTokenProvider, FakeKubTokenProvider
from sidecar.messaging_service import MessagingService, MessagingConnectionProperties
from sidecar.model.converters import SidecarConfigurationFactory
from sidecar.model.objects import ISidecarConfiguration, KubernetesSidecarConfiguration, \
    AwsSidecarConfiguration, AzureSidecarConfiguration, SidecarApplication, EnvironmentType, SidecarTerraformService
from sidecar.request_logger import RequestLogger
from sidecar.sandbox_deployment_state_tracker import SandboxDeploymentStateTracker
from sidecar.sandbox_end_deployment_notifier import SandboxEndDeploymentNotifier
from sidecar.sandbox_start_time_updater import ISandboxStartTimeUpdater
from sidecar.services.deployment_outputs_service import DeploymentOutputsService

from sidecar.services.service_file_store import ServiceFileStore
from sidecar.services.service_status_state import ServiceStatusState
from sidecar.services.service_updater import K8SServiceUpdater, AzureServiceUpdater, AwsServiceUpdater, IServiceUpdater

from sidecar.utils import CallsLogger, Utils
from sidecar.const import AppInstanceConfigStatus
from sidecar.sandbox_error import SandboxError, ErrorCodes
from sidecar.kub_status_maintainer import KUBStatusMaintainer
from sidecar.errors_controller import ErrorsController

flask = Flask(__name__)
_logger = None  # type: Logger
cloud_logger = None  # type: ICloudLogger
_request_logger = None  # type: RequestLogger
_app_instance_health_check_monitor = None  # type: AppInstanceHealthCheckMonitor
_configuration_start_policy = None  # type: ConfigurationStartPolicy
_app_instance_identifier_creator = None  # type: IAppInstanceIdentifierCreator
_app_instance_event_handler = None  # type: AppInstanceEventHandler
_app_signals = Namespace()
_kub_token_provider = None  # type: KubTokenProvider
_start_time_updater = None  # type: ISandboxStartTimeUpdater
_app_health_check_state = None  # type: AppHealthCheckState
_apps_configuration_end_tracker = None  # type: AppsConfigurationEndTracker
_app_health_check_monitor = None  # type: AppHealthCheckMonitor
_app_status_maintainer = None  # type: AppStatusMaintainer
_app_instance_health_check_executor = None  # type: HealthCheckExecutor
_app_sandbox_end_deployment_notifier = None  # type: SandboxEndDeploymentNotifier
_config = None  # type: ISidecarConfiguration
_file_logger = None  # type: FileLogger
_service_file_store = None  # type: ServiceFileStore
_service_status_state = None  # type: ServiceStatusState
_service_updater = None  # type: IServiceUpdater
_app_service = None  # type: AppService
_deployment_outputs_service = None  # type: DeploymentOutputsService
_status_maintainer = None  # type: StatusMaintainer
_errors_controller = None  # type: ErrorsController


def get_status_updater(config: ISidecarConfiguration,
                       app_instance_event_handler: AppInstanceEventHandler,
                       aws_session: AwsSession,
                       own_public_ip: str) -> SandboxDeploymentStateTracker:
    global _kub_token_provider
    global _start_time_updater
    global _app_service
    global _app_health_check_state
    global _apps_configuration_end_tracker
    global _app_status_maintainer
    global _app_instance_identifier_creator
    global _configuration_start_policy
    global _service_file_store
    global _file_logger
    global _service_status_state
    global _service_updater
    global _deployment_outputs_service
    global _status_maintainer
    global _errors_controller

    _service_status_state = ServiceStatusState(services=config.services)

    app_instance_status_event_reporter = AppInstanceConfigStatusEventReporter(
        app_instance_event_handler=app_instance_event_handler, logger=_logger)
    time_provider = DateTimeProvider()

    _app_health_check_state = AppHealthCheckState(app_names=[app.name for app in config.apps], logger=_logger)
    if isinstance(config, KubernetesSidecarConfiguration):
        k8s_config = config  # type: KubernetesSidecarConfiguration
        if _kub_token_provider is None:
            _kub_token_provider = KubTokenProvider()

        kas = KubApiService(hostname=k8s_config.kub_api_address,
                            namespace=k8s_config.sandbox_id,
                            kub_token_provider=_kub_token_provider,
                            logger=_logger)

        _status_maintainer = KUBStatusMaintainer(logger=_logger, kub_api_service=kas)
        _errors_controller = ErrorsController(status_maintainer=_status_maintainer)

        _app_instance_service = KubAppInstanceService(logger=_logger, kub_api_service=kas)
        _apps_configuration_end_tracker = AppsConfigurationEndTracker(logger=_logger,
                                                                      apps=config.apps,
                                                                      app_instance_service=_app_instance_service)

        _configuration_start_policy = ConfigurationStartPolicy(app_health_check_state=_app_health_check_state,
                                                               apps_config_end_tracker=_apps_configuration_end_tracker,
                                                               apps=config.apps,
                                                               services=config.services,
                                                               service_status_state=_service_status_state)

        _app_instance_identifier_creator = KubAppInstanceIdentifierCreator(kub_api_service=kas, logger=_logger)

        sandbox_deployment_end_updater = KubSandboxDeploymentEndUpdater(
            kub_api_service=kas)

        sandbox_deployment_state_tracker = SandboxDeploymentStateTracker(
            logger=_logger,
            apps=config.apps,
            apps_configuration_end_tracker=_apps_configuration_end_tracker,
            sandbox_deployment_end_updater=sandbox_deployment_end_updater,
            space_id=k8s_config.space_id)

        _app_status_maintainer = AppStatusMaintainer(logger=_logger,
                                                     app_instance_service=_app_instance_service,
                                                     apps_configuration_end_tracker=_apps_configuration_end_tracker,
                                                     sandbox_deployment_state_tracker=sandbox_deployment_state_tracker,
                                                     app_instance_status_event_reporter=app_instance_status_event_reporter)

        _app_service = K8sAppService(api=kas, sandbox_id=k8s_config.sandbox_id, own_public_ip=own_public_ip,
                                     logger=_logger)
        _start_time_updater = KubSandboxStartTimeUpdater(
            app_health_check_state=_app_health_check_state,
            date_time_provider=time_provider,
            logger=_logger,
            kub_api_service=kas,
            apps_configuration_end_tracker=_apps_configuration_end_tracker)

        _service_updater = K8SServiceUpdater(kub_api_service=kas,
                                             service_status_state=_service_status_state,
                                             logger=_logger)

        _deployment_outputs_service = DeploymentOutputsService(_logger,
                                                               _app_instance_service,
                                                               _service_updater,
                                                               _config)

        _service_file_store = ServiceFileStore()

        return sandbox_deployment_state_tracker

    if isinstance(config, AwsSidecarConfiguration):
        aws_config = config  # type: AwsSidecarConfiguration

        aws_status_maintainer = AWSStatusMaintainer(aws_session,
                                                    sandbox_id=aws_config.sandbox_id,
                                                    logger=_logger,
                                                    default_region=aws_config.onboarding_region,
                                                    table_name=aws_config.data_table_name)

        _status_maintainer = aws_status_maintainer
        _errors_controller = ErrorsController(status_maintainer=_status_maintainer)

        _app_instance_service = AwsAppInstanceService(sandbox_id=aws_config.sandbox_id,
                                                      logger=_logger,
                                                      aws_session=aws_session,
                                                      aws_status_maintainer=aws_status_maintainer)
        _apps_configuration_end_tracker = AppsConfigurationEndTracker(logger=_logger,
                                                                      apps=config.apps,
                                                                      app_instance_service=_app_instance_service)

        terminating_query = AwsSandboxTerminatingQuery(aws_status_maintainer)

        _configuration_start_policy = ConfigurationStartPolicy(app_health_check_state=_app_health_check_state,
                                                               apps_config_end_tracker=_apps_configuration_end_tracker,
                                                               apps=config.apps,
                                                               services=config.services,
                                                               service_status_state=_service_status_state,
                                                               terminating_query=terminating_query)
        _app_instance_identifier_creator = AwsAppInstanceIdentifierCreator(logger=_logger)

        sandbox_deployment_end_updater = AwsSandboxDeploymentEndUpdater(aws_status_maintainer)

        sandbox_deployment_state_tracker = SandboxDeploymentStateTracker(
            logger=_logger,
            apps=config.apps,
            apps_configuration_end_tracker=_apps_configuration_end_tracker,
            sandbox_deployment_end_updater=sandbox_deployment_end_updater,
            space_id=aws_config.space_id)

        _app_status_maintainer = AppStatusMaintainer(logger=_logger,
                                                     app_instance_service=_app_instance_service,
                                                     apps_configuration_end_tracker=_apps_configuration_end_tracker,
                                                     sandbox_deployment_state_tracker=sandbox_deployment_state_tracker,
                                                     app_instance_status_event_reporter=app_instance_status_event_reporter)

        _service_updater = AwsServiceUpdater(status_maintainer=aws_status_maintainer,
                                             service_status_state=_service_status_state,
                                             logger=_logger)

        _deployment_outputs_service = DeploymentOutputsService(_logger,
                                                               _app_instance_service,
                                                               _service_updater,
                                                               _config)

        _start_time_updater = AwsSandboxStartTimeUpdater(app_health_check_state=_app_health_check_state,
                                                         sandbox_id=aws_config.sandbox_id,
                                                         aws_session=aws_session,
                                                         date_time_provider=time_provider,
                                                         logger=_logger,
                                                         apps_configuration_end_tracker=_apps_configuration_end_tracker,
                                                         aws_status_maintainer=aws_status_maintainer)

        _app_service = AWSAppService(session=aws_session,
                                     aws_status_maintainer=aws_status_maintainer,
                                     sandbox_id=aws_config.sandbox_id,
                                     production_id=aws_config.production_id,
                                     own_public_ip=own_public_ip,
                                     env_type=EnvironmentType.Sandbox,
                                     logger=_logger,
                                     default_region=aws_config.onboarding_region,
                                     table_name=aws_config.data_table_name)

        _service_file_store = ServiceFileStore()

        return sandbox_deployment_state_tracker

    if isinstance(config, AzureSidecarConfiguration):
        azure_config = config  # type: AzureSidecarConfiguration
        _app_status_maintainer, \
        _configuration_start_policy, \
        _app_instance_identifier_creator, \
        _apps_configuration_end_tracker, \
        _app_service, \
        sandbox_deployment_state_tracker, \
        _start_time_updater, \
        azure_status_maintainer, \
        app_instance_service = \
            AzureSidecarApiInitializer(config=azure_config,
                                       app_instance_status_event_reporter=app_instance_status_event_reporter,
                                       app_health_check_state=_app_health_check_state,
                                       service_execution_end_tracker=_service_status_state,
                                       logger=_logger).initialize()

        _status_maintainer = azure_status_maintainer
        _errors_controller = ErrorsController(status_maintainer=_status_maintainer)

        _service_updater = AzureServiceUpdater(status_maintainer=azure_status_maintainer,
                                               service_status_state=_service_status_state,
                                               logger=_logger)
        _service_file_store = ServiceFileStore()

        _deployment_outputs_service = DeploymentOutputsService(_logger,
                                                               app_instance_service,
                                                               _service_updater,
                                                               _config)

        return sandbox_deployment_state_tracker

    raise Exception('unknown provider {}'.format(config.provider))


@flask.route("/")
def hello():
    _logger.info("start")
    return "welcome cs18:sidecar-api", 200


@flask.route("/sandbox/public-address")
def get_sandbox_public_address():
    public_address = _app_service.get_sandbox_public_dns()
    return public_address, 200


@flask.route("/application/<string:app_name>/health-check", methods=['POST'])
def start_health_check(app_name: str):
    global _app_instance_identifier_creator
    global _app_instance_health_check_monitor

    ip_address = get_remote_address()
    req = safely_get_request_json(request=request)
    additional_data = req.get('additional_data')

    app_instance_identifier = _app_instance_identifier_creator.create(app_name=app_name,
                                                                      ip_address=ip_address,
                                                                      additional_data=additional_data)
    _app_instance_health_check_monitor.start(address=ip_address,
                                             identifier=app_instance_identifier)
    # fail here if validation fails ONLY
    return '', 202


@flask.route('/application/<app_name>/<instance_id>/logs/<topic>', methods=['POST'])
def write_log(app_name: str, instance_id: str, topic: str):
    items = safely_get_request_json(request=request)
    events = [(datetime.fromtimestamp(item["date"]), item["line"]) for item in items]
    log_entry = AppLogEntry(app_name, instance_id, topic, events, topic)
    cloud_logger.write(log_entry)

    return '', 200


@flask.route('/lazy_load_artifacts_waiting/<value>', methods=['GET'])
def set_lazy_load_artifact_waiting(value: str):
    global _status_maintainer

    try:
        _status_maintainer.update_lazy_load_artifacts_waiting(Utils.str_to_bool(value.lower()))
    except Exception as e:
        _logger.info(e)

    return '', 200


@flask.route('/start_lazy_load_artifacts_download', methods=['GET'])
def start_lazy_load_artifacts_download():
    global _status_maintainer

    try:
        _status_maintainer.update_lazy_load_artifacts_waiting(True)
    except Exception as e:
        _logger.info(e)

    return '', 200


@flask.route('/end_lazy_load_artifacts_download', methods=['POST'])
def end_lazy_load_artifacts_download():
    global _errors_controller
    global _status_maintainer

    req = safely_get_request_json(request=request)

    try:
        _status_maintainer.update_lazy_load_artifacts_waiting(False)
        _errors_controller.handle_artifacts_not_found(req["artifacts_not_found"])
    except Exception as e:
        _logger.info(e)

    return '', 200

# example to how to use "add-sandbox-error" from bash code:
#   wget -nv -O- {SIDECAR_HOST}/add-sandbox-error --header \'Content-Type: application/json\'
#   --post-data "{{\\"error\\":\\"file: $file_name not found\\",\\"code\\":\\"{error_code}\\"}}"',
@flask.route("/add-sandbox-error", methods=['POST'])
def add_sandbox_error():
    global _errors_controller
    req = safely_get_request_json(request=request)

    try:
        new_error = SandboxError(Utils.get_utc_now_in_isoformat(), req["code"], req["error"])
        _errors_controller.add_sandbox_error(new_error)
    except Exception as e:
        _logger.info(e)

    return '', 200


@flask.route('/application/<string:app_name>/<string:instance_id>/event', methods=['POST'])
def report_app_instance_event(app_name: str, instance_id: str):
    global _app_instance_identifier_creator
    global _app_instance_event_handler

    data_json = safely_get_request_json(request=request)
    event = data_json['event']
    if event not in AppInstanceEvents.ALL:
        error_message = "'{EVENT}' is not one of the known event types".format(EVENT=event)
        return error_message, 400

    app_instance_identifier = _app_instance_identifier_creator.create_from_instance_id(app_name=app_name,
                                                                                       instance_id=instance_id)
    _app_instance_event_handler.report_event(app_instance_identifier=app_instance_identifier,
                                             app_instance_event=event)
    return '', 200


@flask.route("/application/<string:app_name>/config-start-status", methods=['GET'])
def get_application_configuration_start_status(app_name: str):
    global _configuration_start_policy
    start_status = _configuration_start_policy.get_configuration_start_status(app_name)
    return start_status, 200


@flask.route("/is-api-alive", methods=['GET'])
def get_api_is_alive(app_name: str):
    return '', 200


@flask.route("/application/<string:app_name>/whoami", methods=['POST'])
def get_who_am_i(app_name: str):
    global _app_instance_identifier_creator

    ip_address = get_remote_address()
    req = safely_get_request_json(request=request)
    additional_data = req.get('additional_data')

    app_instance_identifier = _app_instance_identifier_creator.create(app_name=app_name,
                                                                      ip_address=ip_address,
                                                                      additional_data=additional_data)
    return app_instance_identifier.infra_id, 200


@flask.route("/services/<string:service>/config-start-status", methods=['GET'])
def config_start_status_service(service: str):
    start_status = _configuration_start_policy.get_configuration_start_status(name=service)
    return start_status, 200


@flask.route("/services/<string:service>/status", methods=['POST'])
def update_service_status(service: str):
    req = safely_get_request_json(request=request)
    _service_updater.update_status(name=service, status=req["status"])
    return '', 200


@flask.route("/services/<string:service>/<string:cmd>/save-output", methods=['POST'])
def save_service_execution_output(service: str, cmd: str):
    req = request  # type: Request
    _service_file_store.save_execution_output(name=service, cmd=cmd, output=req.data)
    return '', 200


@flask.route("/deployment_outputs_resolver", methods=['POST'])
def deployment_outputs_resolver():
    req = request  # type: Request
    content = req.data.decode(req.charset)
    outputs = content.split(' ')
    res = _deployment_outputs_service.get_deployment_outputs(outputs)
    return res, 200


@flask.route("/services/<string:name>/deployment_output", methods=['POST'])
def save_service_deployment_output(name: str):
    req = request  # type: Request
    try:
        output = req.get_json()
    except Exception:
        output = req.data.decode(req.charset)
        err = f"service '{name}' deployment output is not valid:\n{output}"
        _logger.exception(err)
        return err, 400
    _deployment_outputs_service.save_service_outputs(name, output)
    return '', 200


@flask.route("/application/<string:app_name>/deployment_output", methods=['POST'])
def save_application_deployment_output(app_name: str):
    req = request  # type: Request
    output = req.data.decode(req.charset)
    instance_id = req.args.get('instance-id', None)
    additional_data = None
    if instance_id:
        additional_data = {"instance-id": instance_id}
    ip_address = get_remote_address()

    app_instance_identifier = _app_instance_identifier_creator.create(app_name=app_name,
                                                                      ip_address=ip_address,
                                                                      additional_data=additional_data)
    _deployment_outputs_service.save_application_outputs(app_instance_identifier, output)
    return '', 200


@flask.errorhandler(Exception)
def unhandled_exception(e):
    status = e.code if isinstance(e, HTTPException) else 500
    _request_logger.log_request_failed(e, status)
    return str(e), status


def safely_get_request_json(request: Request):
    # will throw BadRequest if can't deserialize
    # currently, assuming that won't happen because the client is expected to properly encode the string values
    return request.get_json()


def on_instance_update_status(sender, **kwargs):
    global _app_health_check_monitor
    identifier = kwargs.get("identifier")
    _app_health_check_monitor.start(identifier=AppInstanceIdentifier(name=identifier.name,
                                                                     infra_id=identifier.infra_id))


def on_apps_deployment_complete(sender, **kwargs):
    global _start_time_updater
    global _app_sandbox_end_deployment_notifier

    _start_time_updater.on_app_instance_configuration_status_updated()
    _app_sandbox_end_deployment_notifier.notify_end_deployment()


def get_app_health_check_configuration(config: ISidecarConfiguration) -> AppHealthCheckConfiguration:
    app_health_check_configuration = AppHealthCheckConfiguration()
    for app in config.apps:
        app_health_check_configuration.add_app_healthcheck_info(app.name, app.healthcheck_script,
                                                                app.default_health_check_ports_to_test,
                                                                app.healthcheck_timeout)
    return app_health_check_configuration


def run_impl(config: ISidecarConfiguration, own_public_ip: str):
    global _app_instance_health_check_monitor
    global cloud_logger
    global _app_instance_event_handler
    global _app_health_check_monitor
    global _app_instance_health_check_executor
    global _app_sandbox_end_deployment_notifier
    global _app_status_maintainer
    global _app_health_check_state
    global _file_logger

    aws_session = None
    if isinstance(config, AwsSidecarConfiguration):
        aws_config = config  # type: AwsSidecarConfiguration
        aws_session = AwsSession(region_name=aws_config.region_name,
                                 aws_config=aws_config,
                                 logger=_logger)

    if _file_logger is None:
        _file_logger = FileLogger()
    cloud_logger = _file_logger

    _app_instance_event_handler = AppInstanceEventHandler(cloud_logger=cloud_logger,
                                                          date_time_provider=DateTimeProvider(),
                                                          logger=_logger)

    sandbox_deployment_state_tracker = get_status_updater(
        config=config,
        app_instance_event_handler=_app_instance_event_handler,
        aws_session=aws_session,
        own_public_ip=own_public_ip)

    health_check_configuration = get_app_health_check_configuration(config)

    preparer = HealthCheckPreparer(logger=_logger,
                                   health_check_configuration=health_check_configuration,
                                   file_system=FileSystemService())

    _app_instance_health_check_executor = HealthCheckExecutor(apps=config.apps,
                                                              executor_logger=AppInstanceHealthCheckExecutorLogger(
                                                                  cloud_logger=cloud_logger,
                                                                  logger=_logger),
                                                              logger=_logger)
    _app_instance_health_check_monitor = AppInstanceHealthCheckMonitor(
        executor=_app_instance_health_check_executor,
        preparer=preparer,
        logger=_logger,
        cloud_logger=cloud_logger,
        status_maintainer=_app_status_maintainer)

    executor = HealthCheckExecutor(apps=config.apps,
                                   executor_logger=AppHealthCheckExecutorLogger(cloud_logger=cloud_logger,
                                                                                logger=_logger),
                                   logger=_logger)

    _app_health_check_monitor = AppHealthCheckMonitor(apps=config.apps,
                                                      executor=executor,
                                                      preparer=preparer,
                                                      app_health_check_state=_app_health_check_state,
                                                      app_service=_app_service,
                                                      health_check_configuration=health_check_configuration,
                                                      apps_configuration_end_tracker=_apps_configuration_end_tracker,
                                                      logger=_logger)

    messaging_service = MessagingService(config.messaging, _logger)

    _app_sandbox_end_deployment_notifier = SandboxEndDeploymentNotifier(sandbox_deployment_state_tracker,
                                                                        messaging_service,
                                                                        _app_health_check_state,
                                                                        config.space_id,
                                                                        config.sandbox_id,
                                                                        config.production_id,
                                                                        config.env_type)

    on_instance_update_status_signal = signal(Signals.ON_INSTANCE_UPDATE_STATUS)
    on_instance_update_status_signal.connect(on_instance_update_status, sender=_app_status_maintainer)

    on_apps_deployment_complete_signal = signal(Signals.ON_APPS_DEPLOYMENT_COMPLETE)
    on_apps_deployment_complete_signal.connect(on_apps_deployment_complete, sender=_app_health_check_state)


def configure_debug():
    # # create log folder: ~/sidecar
    # api_log_folder = os.path.dirname(Const.get_log_file())
    # file_system = FileSystemService()
    # if not file_system.exists(api_log_folder):
    #     file_system.create_folders(api_log_folder)

    global _config

    properties = MessagingConnectionProperties(host="wombat.rmq.cloudamqp.com", user="rhpjvtoj",
                                               password="M7dZ2D5hWkIEOLPj6poiB4fF1t9cmNIf", queue="nefmwtza4r121",
                                               exchange="", routingkey="nefmwtza4r121", virtualhost="rhpjvtoj",
                                               port=5672, queuetype="fanout", expires=60000, usessl=False)

    application = SidecarApplication(name="fasty", instances_count=1, dependencies=[],
                                     env={"WELCOME_STRING": "Welcome to Quali Colony!", "PORT": "3001"},
                                     healthcheck_timeout=60, default_health_check_ports_to_test=[],
                                     healthcheck_script="fasty.sh", has_public_access=True, outputs=[])

    # _config = KubernetesSidecarConfiguration(environment="test",
    #                                          sandbox_id="8ffzw4jrfr00a1",
    #                                          kub_api_address="https://ci-aks-v2-8c5f4bd2.hcp.westeurope.azmk8s.io:443",
    #                                          space_id="d8fa32d9-7af3-4869-9b14-a00c0c488b0c",
    #                                          cloud_external_key="8f70be32-3041-4a00-b96e-29f7a79cc854",
    #                                          apps=[],
    #                                          services=[SidecarTerraformService(name="s3store",
    #                                                                            type=ServiceType.TerraForm,
    #                                                                            terraform_version="",
    #                                                                            dependencies=[],
    #                                                                            inputs=[],
    #                                                                            terraform_module=TerraformServiceModule(
    #                                                                                source="",
    #                                                                                version=""
    #                                                                            ),
    #                                                                            tfvars_file=Script(
    #                                                                                name="",
    #                                                                                path="",
    #                                                                                headers={}
    #                                                                            ))],
    #                                          env_type="sandbox",
    #                                          production_id="",
    #                                          messaging=properties)

    _config = AwsSidecarConfiguration(environment="test", sandbox_id="t7onu02wct02c1", region_name="eu-west-1",
                                      space_id="d8fa32d9-7af3-4869-9b14-a00c0c488b0c",
                                      cloud_external_key="8f70be32-3041-4a00-b96e-29f7a79cc854", apps=[application],
                                      services=[SidecarTerraformService(name='s3', type=None,
                                                                        terraform_module=None,
                                                                        terraform_version=None,
                                                                        tfvars_file=None,
                                                                        dependencies=[],
                                                                        outputs=["other_variable_value",
                                                                                 "other_variable_value2"])],
                                      messaging=properties,
                                      env_type="sandbox",
                                      production_id="",
                                      data_table_name="",
                                      )


def get_build_info_json():
    build_info = os.path.join(os.path.dirname(__file__), "..", "build_info.json")
    with open(build_info) as build_info_file:
        build_info_str = build_info_file.read().strip()
        build_info__json = json.loads(build_info_str)
        return build_info__json


def run():
    global _config
    global _logger
    global _request_logger

    dir_name = os.path.dirname(os.path.abspath(__file__))
    logging.config.fileConfig(os.path.join(dir_name, 'logzio.conf'))
    _logger = logging.getLogger("logger")

    try:
        if _config is None:
            with open(Const.get_config_file(), 'r') as conf:
                _config = SidecarConfigurationFactory.get(json.loads(conf.read()))

        _logger.addFilter(LoggingFilter(_config))
        _request_logger = RequestLogger(flask, _logger, [write_log])
        CallsLogger.set_logger(_logger)

        _logger.info('starting sidecar')
        _logger.info('build_info.json: {}'.format(json.dumps(get_build_info_json())))
        _logger.info('config.json: {}'.format(_config))

        run_impl(config=_config, own_public_ip=_get_own_ip())

        flask.run(host='0.0.0.0', port=4000)

    except Exception as exc:
        _logger.exception("sidecar failed to start")
        raise exc


def _get_own_ip() -> str:
    sources = (
        "http://icanhazip.com",
        "http://ident.me",
        "http://whatismyip.akamai.com",
        "http://ip.tyk.nu",
        "http://wgetip.com"
    )

    for source in sources:
        try:
            resp = requests.get(source)
            if resp.status_code == 200:
                return resp.text.replace(' ', '').replace('\n', '').replace('\t', '')
        except:
            pass

    raise ConnectionError("Could not retrieve own IP from defined sources.")


def get_remote_address():
    if isinstance(_kub_token_provider, FakeKubTokenProvider):  # debug mode
        return request.headers.getlist("X-Forwarded-For")[0]
    else:
        return request.remote_addr


if __name__ == "__main__":
    print("sidecar in debug mode")
    # Utils.stop_on_debug()
    _kub_token_provider = FakeKubTokenProvider()
    _file_logger = FakeFileLogger()
    configure_debug()
    run()
