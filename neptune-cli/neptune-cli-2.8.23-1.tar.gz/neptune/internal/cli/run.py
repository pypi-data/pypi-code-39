# -*- coding: utf-8 -*-
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
from __future__ import print_function

from distutils.version import LooseVersion  # pylint: disable=no-name-in-module, import-error
from logging import getLogger
import os
import shutil
import sys

import requests
from requests import RequestException

from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.executing.experiment_executor_factory import JobExecutorFactory
from neptune.internal.cli.commands.neptune_command_factory import NeptuneCommandFactory
from neptune.internal.cli.commands.neptune_exec import NeptuneExecFactory
from neptune.internal.cli.commands.neptune_notebook import (
    NeptuneNotebookFactory
)
from neptune.internal.cli.commands.neptune_run import NeptuneRunFactory
from neptune.internal.cli.commands.parsers.root_parser import NeptuneRootCommandParser
from neptune.internal.cli.commands.parsers.utils.autocompletion import autocomplete
from neptune.internal.cli.commands.utils.urls import Urls
from neptune.internal.cli.helpers import should_retry_api_calls
from neptune.internal.cli.processes.job_spawner import JobSpawner
from neptune.internal.cli.signal_handlers import setup_signal_handlers
from neptune.internal.cli.tracking import Timer, provide_default_user_identity_function, report_tracking_metrics
from neptune.internal.common import \
    NeptuneException
from neptune.internal.common.api.api_service_factory import ApiServiceFactory, LOG_IN_MESSAGE, \
    create_analytics_service, install_analytics_sys_hook, send_neptune_crash, setup_offline_token_storage_service
from neptune.internal.common.api.check_api_version import CheckApiVersion
from neptune.internal.common.api.keycloak_api_service import KeycloakApiConfig, KeycloakApiService
from neptune.internal.common.config import neptune_config
from neptune.internal.common.config.connection_info import ConnectionInfo
from neptune.internal.common.config.job_config import ConfigKeys
from neptune.internal.common.config.neptune_config import (
    ConfigSingleton,
    EmptyConfig,
    NeptuneConfig,
    load_global_config
)
from neptune.internal.common.exceptions.keycloak_exceptions import KeycloakException
from neptune.internal.common.local_storage.local_storage import LocalStorage
from neptune.internal.common.parsers.common_parameters_configurator import \
    CommonParametersConfigurator
from neptune.internal.common.parsers.exec_args_formatter import ExecArgsFormatter
from neptune.internal.common.parsers.tracked_parameter_parser import TrackedParameterParser
from neptune.internal.common.sentry import get_sentry_client_instance, install_sentry_sys_hook
from neptune.internal.common.utils.browser import NullBrowser, WebBrowser
from neptune.internal.common.utils.logging_utils import OfflineNeptuneLogger, OnlineNeptuneLogger
from neptune.internal.common.utils.version_utils import cli_major_version
from neptune.version import __version__

logger = getLogger(__name__)

_neptune_production = False


def initial_setup(local_storage):
    try:
        global _neptune_production  # pylint:disable=global-statement
        offline_token_storage_service = setup_offline_token_storage_service(local_storage)
        token = offline_token_storage_service.load()
        host = "https://app.neptune.ml"

        if token and token.access_token and token.access_token.neptune_host:
            host = token.access_token.neptune_host

        from neptune.internal.common import sentry
        if "app.neptune.ml" in host or os.getenv("USE_EXTERNAL_APIS", None) is not None:
            _neptune_production = True
            sentry._DSN = "https://e65fb67552774747858e862e3e29f81e:8b36637a79f04f56a7e68d71f8b19ce8@sentry.io/209354"  # pylint:disable=protected-access
            install_sentry_sys_hook(local_storage)
            install_analytics_sys_hook(local_storage)
        else:
            sentry._DSN = None  # pylint:disable=protected-access
    except BaseException:
        logger.debug("Unable to setup Neptune reporting")


def run(command_line_args, version_update_suggestion_on=False):

    try:
        sys.exit(_run(command_line_args, version_update_suggestion_on))
    except NeptuneException as error:
        sys.exit(str(error))
    except Exception as error:
        local_storage = LocalStorage.profile()
        send_neptune_crash(exc=sys.exc_info()[1], local_storage=local_storage)
        get_sentry_client_instance(local_storage).send_exception()
        sys.exit(str(error))


def _create_local_storage(arguments):
    return LocalStorage.profile(getattr(arguments.known_args,
                                        ConfigKeys.PROFILE,
                                        CommonParametersConfigurator.DEFAULT_PROFILE))


def _run(command_line_args, version_update_suggestion_on=False):
    root_command_parser = NeptuneRootCommandParser()
    autocomplete(root_command_parser.argparse_parser,
                 always_complete_options='long',
                 default_completer=None)

    try:
        arguments = root_command_parser.get_arguments(command_line_args)
    except SystemExit:
        try:
            # At this point we may not have a token / local storage
            offline_token_storage_service = setup_offline_token_storage_service(LocalStorage.profile())
            analytics_service = create_analytics_service(offline_token_storage_service)
            if analytics_service is not None:
                analytics_service.send_cli_usage_event(
                    command_name=sys.argv[1] if len(sys.argv) > 1 else "",
                    correct_usage=False,
                    full_command=" ".join(sys.argv),
                    has_local_config=not isinstance(neptune_config.load_local_config(None), EmptyConfig)
                )
        except Exception as e:
            logger.debug("Unable to send analytics: %s", str(e))
        raise

    local_storage = _create_local_storage(arguments)

    initial_setup(local_storage)

    if version_update_suggestion_on and _neptune_production:
        _suggest_version_update_if_cli_is_outdated()

    umask_zero = getattr(
        arguments.known_args, CommonParametersConfigurator.UMASK_ZERO_PARAMETER, False)
    if umask_zero:
        os.umask(0)
    major_version = cli_major_version()
    desired_neptune_version = getattr(
        arguments.known_args,
        CommonParametersConfigurator.DESIRED_NEPTUNE_VERSION_PARAMETER,
        major_version
    ) or major_version
    if desired_neptune_version != major_version:
        print('Wrong CLI version, required: {}, actual: {}'.format(
            desired_neptune_version, major_version))
        return 1

    root_command_parser.validate(arguments, command_line_args)

    main_command = arguments.known_args.command_to_run
    subcommand_name = arguments.known_args.subcommand if 'subcommand' in arguments.known_args else None
    if main_command in [CommandNames.ACCOUNT] and subcommand_name not in [CommandNames.API_TOKEN]:
        return _run_without_context(arguments, local_storage)
    elif getattr(arguments.known_args, "offline", False):
        return _run_offline(arguments)
    else:
        return _run_online(command_line_args, arguments, local_storage)


def _suggest_version_update_if_cli_is_outdated():
    try:
        latest_version = _latest_version_from_pypi()
        if LooseVersion(__version__) < LooseVersion(latest_version):
            print(
                u'WARNING: Your version of Neptune CLI ({}) is outdated.\n'
                u'         We recommend an update to the latest version ({}):\n'
                u'           pip install neptune-cli --upgrade\n'.format(
                    __version__,
                    latest_version))
    except (RequestException, KeyError):
        pass


def _latest_version_from_pypi():
    release_info = requests.get('https://pypi.python.org/pypi/neptune-cli/json').json()
    return release_info['info']['version']


def _create_config(arguments, address, username, frontend_address):
    config_path = getattr(arguments.known_args, "config", None)
    connection_info = ConnectionInfo(address=address,
                                     username=username,
                                     frontend_address=frontend_address)
    profile = getattr(arguments.known_args,
                      ConfigKeys.PROFILE,
                      CommonParametersConfigurator.DEFAULT_PROFILE)

    config = NeptuneConfig(connection_info=connection_info,
                           commandline_args=arguments,
                           local_config=neptune_config.load_local_config(config_path),
                           global_config=load_global_config(profile),
                           show_deprecated_config_keys_warnings=True)

    ConfigSingleton.set(config)
    return config


def _create_offline_config(arguments):
    return _create_config(arguments, address=None, username=None, frontend_address=None)


def _run_offline(arguments):
    config = _create_offline_config(arguments)
    OfflineNeptuneLogger.configure_offline_logging()
    logger.info(config.pretty_info())

    if config.executable is None:
        raise NeptuneException(config.NO_EXECUTABLE_MESSAGE)

    return JobSpawner.execute(script=config.executable, params=config.cmd_args)


def _run_online(command_line_args, arguments, local_storage):

    if arguments.known_args.command_to_run == CommandNames.EXEC:
        inside_docker = getattr(
            arguments.known_args, CommonParametersConfigurator.INSIDE_DOCKER_PARAMETER, False)
        inside_gcp = getattr(
            arguments.known_args, CommonParametersConfigurator.INSIDE_GCP_PARAMETER, False)
        sources_dir_to_copy = getattr(arguments.known_args, CommonParametersConfigurator.COPY_SOURCES_PARAMETER, None)
        token_file = getattr(arguments.known_args, CommonParametersConfigurator.TOKEN_FILE_PARAMETER, None)
        if token_file:
            if inside_gcp:
                shutil.copy2(token_file, local_storage.tokens_directory.absolute_path)
            elif inside_docker:
                shutil.copy2(token_file, LocalStorage(path=u'/root').tokens_directory.absolute_path)
    else:
        inside_docker = False
        inside_gcp = False
        sources_dir_to_copy = None
        token_file = None

    keycloak_api_service = KeycloakApiService(KeycloakApiConfig())

    offline_token_storage_service = setup_offline_token_storage_service(local_storage)
    token = offline_token_storage_service.load()

    if not token:
        print(LOG_IN_MESSAGE)
        return

    try:
        token = keycloak_api_service.request_token_refresh(token.refresh_token)
        offline_token_storage_service.save(token)
    except KeycloakException as exc:
        print(exc.message + ' Please log in using `neptune account login`.')  # pylint:disable=superfluous-parens
        return

    try:
        analytics_service = create_analytics_service(offline_token_storage_service)
        if analytics_service:
            analytics_service.send_cli_usage_event_async(
                command_name=sys.argv[1] if len(sys.argv) > 1 else "",
                correct_usage=True,
                full_command=" ".join(sys.argv),
                has_local_config=not isinstance(neptune_config.load_local_config(None), EmptyConfig)
            )
    except Exception as e:
        logger.debug("Unable to send analytics: %s", str(e))

    neptune_host = token.access_token.neptune_host

    if not neptune_host:
        offline_token_storage_service.clear()
        print(LOG_IN_MESSAGE)
        return

    config = _create_config(address=neptune_host,
                            username=token.access_token.preferred_username,
                            frontend_address=neptune_host,
                            arguments=arguments)
    logger.info(config.pretty_info())

    api_service_factory = ApiServiceFactory(
        urls=Urls(config.rest_url),
        offline_token_storage_service=offline_token_storage_service,
        with_retries=should_retry_api_calls()
    )

    services = api_service_factory.create_services()

    api_service = services.api_service
    utilities_service = services.utilities_service
    session = services.session

    CheckApiVersion.for_service(utilities_service, config)

    OnlineNeptuneLogger.configure_online_logging(command_line_args, inside_container=inside_gcp or inside_docker)

    tracked_parameter_parser = TrackedParameterParser()
    exec_args_formatter = ExecArgsFormatter(tracked_parameter_parser)

    experiment_executor_factory = JobExecutorFactory(
        config=config,
        api_service_factory=api_service_factory,
        api_service=api_service,
        inside_docker=inside_docker,
        offline_token_storage_service=offline_token_storage_service,
        keycloak_api_service=keycloak_api_service,
        utilities_service=utilities_service,
        exec_args_formatter=exec_args_formatter,
        pip_requirements_file=config.pip_requirements_file,
        inside_gcp=inside_gcp,
        sources_dir_to_copy=sources_dir_to_copy,
        local_storage=local_storage
    )

    if config.open_webbrowser is True:
        web_browser = WebBrowser()
    else:
        web_browser = NullBrowser()

    neptune_exec_factory = NeptuneExecFactory(
        api_service=api_service,
        config=config,
        experiment_executor_factory=experiment_executor_factory)

    neptune_notebook_factory = NeptuneNotebookFactory(
        api_service=api_service,
        config=config,
        local_storage=local_storage,
        tracked_parameter_parser=tracked_parameter_parser,
        web_browser=web_browser,
        experiment_executor_factory=experiment_executor_factory)

    neptune_run_factory = NeptuneRunFactory(
        api_service=api_service,
        config=config,
        local_storage=local_storage,
        tracked_parameter_parser=tracked_parameter_parser,
        web_browser=web_browser,
        experiment_executor_factory=experiment_executor_factory
    )

    command_factory = NeptuneCommandFactory(
        config,
        api_service,
        keycloak_api_service,
        neptune_exec_factory,
        neptune_run_factory,
        neptune_notebook_factory,
        utilities_service,
        offline_token_storage_service,
        session
    )

    command = command_factory.create_command(arguments)
    setup_signal_handlers(command)

    if config.tracking and _neptune_production:
        run_command_with_tracking(
            command,
            arguments,
            provide_default_user_identity_function(offline_token_storage_service)
        )
    else:
        command.run(arguments)

    return command.exit_code


def run_command_with_tracking(command, arguments, get_identity_func):
    try:
        with Timer() as t:
            command.run(arguments)

    except BaseException as err:
        result, error = u'failure', str(err)
        raise

    else:
        result, error = u'success', None

    finally:
        identity = get_identity_func()
        if identity:
            report_tracking_metrics(
                event='CLI_Command: ' + command.name,
                identity=identity,
                exit_code=command.exit_code,
                error=error,
                execution_status=result,
                execution_time=t.elapsed)


def _run_without_context(arguments, local_storage):
    # Do not create log file during account login / logout
    OnlineNeptuneLogger.configure_logging(create_logs_file=False)

    offline_token_storage_service = setup_offline_token_storage_service(local_storage)
    command_factory = NeptuneCommandFactory(
        config=None,
        api_service=None,
        keycloak_api_service=None,
        neptune_exec_factory=None,
        neptune_run_factory=None,
        neptune_notebook_factory=None,
        utilities_service=None,
        offline_token_storage_service=offline_token_storage_service,
        session=None
    )

    command = command_factory.create_command(arguments)
    setup_signal_handlers(command)

    identity_function = provide_default_user_identity_function(offline_token_storage_service)
    if arguments.known_args.command_to_run == CommandNames.LOGOUT:
        identity = provide_default_user_identity_function(offline_token_storage_service)()

        def provide_identity():
            return identity

        identity_function = provide_identity

    if _neptune_production:
        run_command_with_tracking(
            command, arguments, identity_function
        )
    else:
        command.run(arguments)

    return command.exit_code


if __name__ == '__main__':
    run(sys.argv[1:], version_update_suggestion_on=True)
