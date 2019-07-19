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
from future.builtins import object

from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.data.download import DataDownload
from neptune.internal.cli.commands.data.list import DataList
from neptune.internal.cli.commands.data.remove import DataRemove
from neptune.internal.cli.commands.data.upload import DataUpload
from neptune.internal.cli.commands.experiment.ls.formatting import RowFactory
from neptune.internal.cli.commands.experiment.ls.ls_command import NeptuneExperimentLs
from neptune.internal.cli.commands.framework import (
    CommandExecutionContext,
    HandleCommandErrors,
    NeptuneCommandAdapter
)
from neptune.internal.cli.commands.listing.table_formatting import (
    AsciiTableFactory,
    ENTRY_DEFAULT_FIELDS,
    LeaderboardRowFormatter
)
from neptune.internal.cli.commands.experiment.abort.abort_command import NeptuneExperimentAbort
from neptune.internal.cli.commands.project_activate import ProjectActivate
from neptune.internal.cli.commands.session import (
    NeptuneLocalLogin,
    NeptuneLogout,
    NeptuneManualLogin,
    NeptuneApiToken)
from neptune.internal.common.api.keycloak_api_service import KeycloakApiConfig, KeycloakApiService
from neptune.internal.common.api.short_id_converter import ShortIdConverter
from neptune.internal.common.config.job_config import ConfigKeys
from neptune.internal.common.config.neptune_config import load_bool_env
from neptune.internal.common.parsers.common_parameters_configurator import CommonParametersConfigurator
from neptune.internal.common.parsers.type_mapper import TypeMapper
from neptune.internal.common.utils.browser import (
    NullBrowser,
    SilentBrowser,
    is_able_to_open_socket,
    is_webbrowser_operable
)


class NeptuneCommandFactory(object):

    def __init__(self, config, api_service, keycloak_api_service,
                 neptune_exec_factory, neptune_run_factory, neptune_notebook_factory,
                 utilities_service, offline_token_storage_service, session):

        self._config = config
        self._api_service = api_service
        self._keycloak_api_service = keycloak_api_service

        self._neptune_exec_factory = neptune_exec_factory
        self._neptune_notebook_factory = neptune_notebook_factory
        self._neptune_run_factory = neptune_run_factory

        self._utilities_service = utilities_service
        self._offline_token_storage_service = offline_token_storage_service
        self.session = session

    def create_command(self, arguments):

        known_args = arguments.known_args
        name = known_args.command_to_run

        subcommand_name = known_args.subcommand if 'subcommand' in known_args else None

        if name == CommandNames.ACCOUNT and subcommand_name == CommandNames.LOGIN:

            keycloak_api_config = KeycloakApiConfig(
                auth_url=known_args.url if known_args.url else 'https://auth.neptune.ml'
            )

            open_webbrowser = getattr(known_args, "open-webbrowser", None)
            should_open_browser = TypeMapper.to_bool(open_webbrowser if open_webbrowser is not None else "true")
            if not load_bool_env('NEPTUNE_MANUAL_LOGIN', default=False) and \
                    is_webbrowser_operable() and \
                    is_able_to_open_socket() and \
                    should_open_browser:

                return NeptuneLocalLogin(
                    self._config,
                    KeycloakApiService(keycloak_api_config),
                    self._offline_token_storage_service,
                    self._api_service,
                    webbrowser=SilentBrowser())
            else:
                if load_bool_env('NEPTUNE_OPEN_AUTH_URL') and is_webbrowser_operable() and should_open_browser:
                    webbrowser = SilentBrowser()
                else:
                    webbrowser = NullBrowser()

                _login_address = keycloak_api_config.manual_login_url

                return NeptuneManualLogin(
                    config=self._config,
                    auth_code_url=_login_address,
                    keycloak_service=KeycloakApiService(keycloak_api_config),
                    token_storage=self._offline_token_storage_service,
                    api_service=self._api_service,
                    webbrowser=webbrowser)

        elif name == CommandNames.ACCOUNT and subcommand_name == CommandNames.LOGOUT:
            return NeptuneLogout(token_storage=self._offline_token_storage_service)
        elif name == CommandNames.ACCOUNT and subcommand_name == CommandNames.API_TOKEN:
            subcommand_subname = known_args.subsubcommand if 'subsubcommand' in known_args else None
            if subcommand_subname in [CommandNames.GET]:
                return NeptuneApiToken(config=self._config, api_service=self._api_service)

        ctx = CommandExecutionContext(
            api_service=self._api_service,
            config=self._config,
            session=self.session)

        if name == CommandNames.EXEC:
            return self._neptune_exec_factory.create(experiment_id=known_args.experiment_id,
                                                     environment=self._config.environment)

        elif name in CommandNames.EXPERIMENT_CMDS and subcommand_name == CommandNames.SEND_NOTEBOOK:
            return self._neptune_notebook_factory.create(inputs=self._config.input,
                                                         environment=self._config.environment,
                                                         worker=self._config.worker)

        elif (name in CommandNames.EXPERIMENT_CMDS and subcommand_name == CommandNames.SEND)\
                or name == CommandNames.SEND:
            return self._neptune_run_factory.create(
                is_local=False,
                inputs=self._config.input,
                neptune_exec_factory=self._neptune_exec_factory,
                environment=self._config.environment,
                worker=self._config.worker
            )

        elif (name in CommandNames.EXPERIMENT_CMDS and subcommand_name == CommandNames.RUN)\
                or name == CommandNames.RUN:
            return self._neptune_run_factory.create(
                is_local=True,
                inputs=self._config.input,
                neptune_exec_factory=self._neptune_exec_factory,
                environment=self._config.environment,
                worker=None
            )

        elif name in CommandNames.EXPERIMENT_CMDS and subcommand_name == CommandNames.ABORT:
            return NeptuneExperimentAbort(
                config=self._config,
                api_service=self._api_service,
                short_id_converter=ShortIdConverter(self._api_service),
                organization_name=self._config.organization_name,
                project_name=self._config.project_name
            )

        elif name in CommandNames.EXPERIMENT_CMDS and subcommand_name == CommandNames.LIST:
            return NeptuneCommandAdapter(
                HandleCommandErrors(
                    NeptuneExperimentLs(
                        row_factory=RowFactory(
                            formatter=LeaderboardRowFormatter(),
                            fields=ENTRY_DEFAULT_FIELDS,
                            table_factory=AsciiTableFactory)
                    )
                ),
                ctx=ctx)

        elif name == CommandNames.DATA and subcommand_name == CommandNames.UPLOAD:
            return DataUpload(
                config=self._config,
                api_service=self._api_service,
                organization_name=self._config.organization_name,
                project_name=self._config.project_name,
                path=known_args.path,
                recursive=known_args.recursive,
                destination=known_args.destination)
        elif name == CommandNames.DATA and subcommand_name == CommandNames.LS:
            return DataList(
                config=self._config,
                api_service=self._api_service,
                organization_name=self._config.organization_name,
                project_name=self._config.project_name,
                path=known_args.path,
                recursive=known_args.recursive)
        elif name == CommandNames.DATA and subcommand_name == CommandNames.RM:
            return DataRemove(
                config=self._config,
                api_service=self._api_service,
                organization_name=self._config.organization_name,
                project_name=self._config.project_name,
                path=known_args.path,
                recursive=known_args.recursive)
        elif name == CommandNames.DATA and subcommand_name == CommandNames.DOWNLOAD:
            return DataDownload(
                config=self._config,
                api_service=self._api_service,
                session=self.session,
                organization_name=self._config.organization_name,
                project_name=self._config.project_name,
                path=known_args.path,
                recursive=known_args.recursive,
                destination=known_args.destination)
        elif name == CommandNames.PROJECT and subcommand_name == CommandNames.ACTIVATE:
            profile = getattr(arguments.known_args,
                              ConfigKeys.PROFILE,
                              CommonParametersConfigurator.DEFAULT_PROFILE)
            return NeptuneCommandAdapter(
                HandleCommandErrors(
                    ProjectActivate(
                        api_service=self._api_service,
                        organization_name=self._config.organization_name,
                        project_name=self._config.project_name,
                        profile=profile
                    )
                ),
                ctx)
        else:
            raise ValueError(u'Unknown command: neptune {}'.format(name))
