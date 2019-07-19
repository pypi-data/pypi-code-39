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
import argparse

from future.builtins import object

from neptune.internal.cli.enums import MLFramework
from neptune.internal.common.config.job_config import ConfigKeys
from neptune.internal.common.models.key_value_property_param import KeyValuePropertyParam
from neptune.internal.common.parsers.type_mapper import TypeValidators
from neptune.internal.common.utils.paths import normalize_path
from neptune.internal.common.utils.str import to_unicode
from neptune.internal.common.utils.version_utils import cli_major_version
from neptune.internal.common.values import Tag
from neptune.version import __version__ as cli_version


class CommonParametersConfigurator(object):
    DEBUG_PARAMETER = 'debug'

    DOCKER_IMAGE_PARAMETER = 'docker-image'
    INSIDE_DOCKER_PARAMETER = 'inside-docker'
    INSIDE_GCP_PARAMETER = 'inside-gcp'
    COPY_SOURCES_PARAMETER = 'copy-sources'
    TOKEN_FILE_PARAMETER = 'token-file'
    PROFILE_PARAMETER = 'profile'

    GLOBAL_OPTIONS_GROUP = 'Global Options'

    DESIRED_NEPTUNE_VERSION_PARAMETER = 'neptune-version'
    UMASK_ZERO_PARAMETER = 'umask-zero'

    # Neptune connection configuration
    OPEN_WEBBROWSER_PARAMETER = ConfigKeys.OPEN_WEBBROWSER

    NAME_PARAMETER = ConfigKeys.NAME
    DESCRIPTION_PARAMETER = ConfigKeys.DESCRIPTION
    PROJECT_PARAMETER = ConfigKeys.PROJECT
    TAG_PARAMETER = 'tag'
    LOG_CHANNEL = 'log-channel'
    LOG_CHANNELS_DEPRECATED = 'log-channels'
    REQUIREMENTS_PARAMETER = ConfigKeys.REQUIREMENTS
    PROPERTY_PARAMETER = 'property'
    EXCLUDE_PARAMETER = '--' + ConfigKeys.EXCLUDE
    BACKUP_PARAMETER = '--' + ConfigKeys.BACKUP
    SNAPSHOT_PARAMETER = 'snapshot'

    EXPERIMENT_PARAMETER = 'experiment'

    ENVIRONMENT = 'environment'
    WORKER = 'worker'

    EXEC_OPTIONS = [EXPERIMENT_PARAMETER]

    SIMPLE_EXPERIMENT_CONFIGURATION_PARAMETERS = [
        NAME_PARAMETER,
        DESCRIPTION_PARAMETER,
        PROJECT_PARAMETER]

    DOCS_ENVIRONMENTS = "https://docs.neptune.ml/advanced-topics/environments/"
    DOCS_AVAILABLE_WORKERS = DOCS_ENVIRONMENTS + "#available-workers"
    DOCS_AVAILABLE_ENVIRONMENTS = DOCS_ENVIRONMENTS + "#available-environments"

    DEFAULT_PROFILE = "default"
    PROFILE_DIRECTORY = "profiles"
    NEPTUNE_DIRECTORY = ".neptune"

    def __init__(self, parser):
        self._parser = parser

    def add_project_param(self, group):
        group.add_argument(
            '--' + self.PROJECT_PARAMETER,
            type=to_unicode,
            help=(
                "Your project's name.\n"
                "You can set this globally using the `neptune project activate` command."))

    def add_debug_param(self, group=None):
        if group is None:
            group = self._parser
        group.add_argument(
            '--' + self.DEBUG_PARAMETER,
            dest=self.DEBUG_PARAMETER,
            action='store_true',
            help="Run command with additional debug-level logging.")

    def add_global_options(self):
        global_options = self._parser.add_argument_group(self.GLOBAL_OPTIONS_GROUP)

        global_options.add_argument(
            '--config',
            dest='config',
            type=normalize_path,
            required=False,
            metavar='CONFIG-FILE',
            help="Path to a Neptune CLI configuration file.")

        global_options.add_argument(
            '-h', '--help',
            action='help',
            default=argparse.SUPPRESS,
            help='Show this help message and exit.')

        global_options.add_argument(
            '-v', '--version',
            action='version',
            version='{}'.format(cli_version),
            help="Show Neptune CLI version and exit.")

        global_options.add_argument(
            '--' + CommonParametersConfigurator.PROFILE_PARAMETER,
            dest=ConfigKeys.PROFILE,
            type=str,
            required=False,
            default='default',
            help='Set user profile to use.'

        )

        self.add_debug_param(global_options)

    def add_experiment_id_positional_param(self):
        self._parser.add_argument('experiment_id', type=TypeValidators.uuid4_type, help='Experiment id.')

    def add_seq_experiment_id_positional_param(self):
        self._parser.add_argument(
            'experiment_ids',
            type=str,
            nargs="+",
            help="Sequence of experiments' identifiers.")

    def add_pip_requirements_param(self, group):
        group.add_argument(
            '--' + ConfigKeys.PIP_REQUIREMENTS_FILE,
            help=(
                "A file containing a list of Python packages that your experiment needs.\n"
                "Requirements file format with an example file can be found here: "
                "http://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format"
            ),
            metavar='PIP-REQUIREMENTS-FILE',
            dest=ConfigKeys.PIP_REQUIREMENTS_FILE
        )

    def add_snapshot_param(self, group):
        group.add_argument(
            '--' + self.SNAPSHOT_PARAMETER,
            dest=self.SNAPSHOT_PARAMETER,
            action='store_true',
            help=(
                'If present, Neptune will make a snapshot of your sources in `~/.neptune/experiments/<experiment id>` '
                'and run the experiment in this directory. This option is useful if you want to change your code '
                'while running an experiment.'
            )
        )

    def add_copy_sources_param(self):
        self._add_named_argument(
            self.COPY_SOURCES_PARAMETER,
            help='If present, neptune exec will copy sources from directory passed as an argument to workdir.',
            metavar='SOURCE-DIRECTORY'
        )

    def add_token_file_param(self):
        self._add_named_argument(
            self.TOKEN_FILE_PARAMETER,
            help='If present, neptune exec will copy given token file to ~/.neptune/tokens.',
            metavar='TOKEN-FILE'
        )

    def add_open_webbrowser_param(self, group=None):
        name = self.OPEN_WEBBROWSER_PARAMETER
        if group is None:
            group = self._parser
        group.add_argument('--' + name, dest=name, metavar='true|false', nargs='?', const='true', default='true',
                           help='Automatically open browser when a new experiment is started.')

    def add_exclude_param(self, group):
        group.add_argument(
            '-x', self.EXCLUDE_PARAMETER,
            type=str,
            action='append',
            help="Files and directories that Neptune should leave out when uploading "
                 "snapshot of your code to the storage.\n"
                 "\n"
                 "Wildcards are supported.\n"
                 "\n"
                 "Example:\n"
                 "    --exclude .git --exclude service/*.log"
        )

    def add_backup_param(self, group):
        group.add_argument(
            '-b', self.BACKUP_PARAMETER,
            type=str,
            action='append',
            help=(
                "Files and directories that should be uploaded to Neptune's storage after the experiment ends."
            ),
            metavar="FILE-OR-DIR"
        )

    def add_log_channels_parameter(self, group):
        group.add_argument(
            '--' + self.LOG_CHANNEL, '-l', '--' + self.LOG_CHANNELS_DEPRECATED,
            dest=ConfigKeys.LOG_CHANNELS,
            action='append',
            help=(
                "List of prefixes based on which Neptune will build numeric channels.\n"
                "\n"
                "Syntax:\n"
                "   --log-channel prefix[:channel_name]\n"
                "\n"
                "Example:\n"
                "Let's assume that an experiment prints:\n"
                "   loss 0.5\n"
                "   loss 0.6\n"
                "   ...\n"
                "In the example above using `--log-channel loss` will build a numeric `loss` channel with "
                "values parsed from stdout/stderr. You can customize the channel's name "
                "with `--log-channel loss:regularization_loss`."
            ),
            metavar="PREFIX[:CHANNEL_NAME]"
        )

    def add_ml_framework_parameter(self, group):

        frameworks = MLFramework.__members__.values()  # pylint:disable=no-member

        group.add_argument(
            '--' + ConfigKeys.ML_FRAMEWORK,
            dest=ConfigKeys.ML_FRAMEWORK,
            choices=frameworks,
            help=(
                "Integrate your experiment's machine learning framework with Neptune.\n"
                "Supported choices are: [`keras`, `tensorflow`]."
            ),
            metavar='ML_FRAMEWORK'
        )

    def add_neptune_global_params(self, group=None):
        self.add_open_webbrowser_param(group)

    def add_docker_image_param(self):
        self._add_named_argument(
            self.DOCKER_IMAGE_PARAMETER,
            type=to_unicode,
            help=argparse.SUPPRESS
        )

    def add_inside_docker_param(self):
        self._add_boolean_flag_argument(self.INSIDE_DOCKER_PARAMETER, help=argparse.SUPPRESS)

    def add_inside_gcp_param(self):
        self._add_boolean_flag_argument(self.INSIDE_GCP_PARAMETER, help=argparse.SUPPRESS)

    def add_umask_zero_param(self):
        self._add_boolean_flag_argument(self.UMASK_ZERO_PARAMETER, help=argparse.SUPPRESS)

    def add_disable_stdout_channel_param(self, group):
        group.add_argument(
            '--' + ConfigKeys.DISABLE_STDOUT_CHANNEL,
            dest=ConfigKeys.DISABLE_STDOUT_CHANNEL,
            action='store_true',
            default=None,
            help='Do not create text channel based on stdout.')

    def add_disable_stderr_channel_param(self, group):
        group.add_argument(
            '--' + ConfigKeys.DISABLE_STDERR_CHANNEL,
            dest=ConfigKeys.DISABLE_STDERR_CHANNEL,
            action='store_true',
            default=None,
            help='Do not create text channel based on stderr.')

    def add_desired_neptune_version_param(self):
        self._add_named_argument(self.DESIRED_NEPTUNE_VERSION_PARAMETER, type=to_unicode,
                                 help=argparse.SUPPRESS, default=cli_major_version())

    def add_experiment_arguments(self, group):
        self.add_docker_image_param()
        self.add_experiment_configuration_arguments(group)

    def add_experiment_configuration_arguments(self, group):

        group.add_argument(
            '--' + self.NAME_PARAMETER,
            type=to_unicode,
            help="Experiment's name.")
        group.add_argument(
            '--' + self.DESCRIPTION_PARAMETER,
            type=to_unicode,
            help=(
                "Experiment's description.\n"
                "Giving a detailed description is often extremely useful when coming back "
                "to the experiment after some time."
            ))
        group.add_argument(
            '--' + self.TAG_PARAMETER,
            dest=ConfigKeys.TAGS,
            type=tag,
            action='append',
            help=(
                "Experiment's tags.\n"
                "Use tags to quickly filter experiments."),
            metavar='TAG')
        group.add_argument(
            '--' + self.PROPERTY_PARAMETER,
            dest=ConfigKeys.PROPERTIES,
            type=self._check_key_value_pair,
            action='append',
            help=(
                "Key-value pairs containing information you wish to associate with the "
                "experiment.\n"
                "\n"
                "Syntax:\n"
                "    --properties key:value [key:value ...]\n"
                "\n"
                "Example:\n"
                "    --properties model-type:svm dataset:my-data-v3\n"
            ),
            metavar='PROPERTY')

    def add_parameter_arguments(self, group):
        _help = (
            "A parameter passed to your code (available via `ctx.params`) tracked by Neptune.\n"
            "\n"
            "Explore more of parameters' syntax here:\n"
            "https://docs.neptune.ml/advanced-topics/experiments/#parameters\n"
            "\n"
            "Read about how to use parameters to optimize your hyperparameter search here:\n"
            "https://docs.neptune.ml/advanced-topics/hyperparameter-optimization/\n"
            "\n"
            "Basic syntax:\n"
            "    -p <name>:<value/values>:<description>\n"
            "\n"
            "Example:\n"
            "    -p 'learning_rate:0.1:Learning rate'\n"
            "The parameter defined in the example above can be accessed from the code with 'ctx.params.learning_rate'"
        )
        group.add_argument(
            '-p', '--parameter',
            type=to_unicode,
            help=_help,
            action='append'
        )

    def add_optional_recursive_parameters(self, group, help_msg):
        group.add_argument(
            '-r', '--recursive',
            help=help_msg,
            action='store_true'
        )

    def add_remote_invocation_arguments(self, group):
        self.add_worker_argument(group)
        self.add_input_argument(group)

    def add_worker_argument(self, group):
        group.add_argument(
            '-w', '--' + self.WORKER,
            type=to_unicode,
            help=(
                "A virtual machine type to run your experiment on. Visit\n"
                "{doc_workers}\n"
                "for a list of Neptune's worker types.\n"
                "\n"
                "You can use `--worker local` to run your experiment locally.".format(
                    doc_workers=self.DOCS_AVAILABLE_WORKERS)
            ),
        )

    def add_input_argument(self, group):
        group.add_argument(
            '-i', '--input',
            type=to_unicode,
            action='append',
            help=(
                "A file or directory in Neptune's storage that should be made accessible "
                "to the experiment in the `/input` directory. You can use this option "
                "multiple times to pass multiple inputs.\n"
                "\n"
                "This option is available only for experiments executed in the cloud, i.e. "
                "it's incompatible with `--worker local`.\n"
                "\n"
                "Syntax:\n"
                "   -i path_on_storage[:name_visible_to_experiment]\n"
                "   --input path_on_storage[:name_visible_to_experiment]\n"
                "\n"
                "Example:\n"
                "   --input my_input.txt:renamed_input.txt\n"
                "The experiment's code can access the file at /input/renamed_input.txt\n"
                "\n"
                "   --input my_input.txt\n"
                "The experiment's code can access the file at /input/my_input.txt"
            )
        )

    def add_environment_argument(self, group):

        _help = (
            'A machine learning environment. Visit\n'
            '{doc_env} \n'
            'for a list of environments supported by Neptune.'.format(doc_env=self.DOCS_ENVIRONMENTS)
        )

        group.add_argument(
            '-e', '--' + self.ENVIRONMENT,
            type=to_unicode,
            help=_help
        )

    def _add_named_argument(self, name, *args, **kwargs):
        self._parser.add_argument('--' + name, dest=name, *args, **kwargs)

    def _add_boolean_flag_argument(self, name, *args, **kwargs):
        self._add_named_argument(name, action='store_true', *args, **kwargs)

    @staticmethod
    def _check_key_value_pair(value):
        value = to_unicode(value)
        split = value.split(":")
        if len(split) != 2:
            raise argparse.ArgumentTypeError(
                u"{} has invalid format. Correct format: key:value".format(value))
        return KeyValuePropertyParam(split[0].strip(), split[1].strip())

    @staticmethod
    def in_debug_mode(command_line_args):
        parser = argparse.ArgumentParser()
        params_parser = CommonParametersConfigurator(parser)
        params_parser.add_debug_param()
        debug_arg, _ = parser.parse_known_args(command_line_args)
        return debug_arg.debug

    @staticmethod
    def append_debug_param(command_line_args, debug):
        if debug:
            command_line_args.append('--' + CommonParametersConfigurator.DEBUG_PARAMETER)


def tag(string):
    try:
        return Tag.create_from(to_unicode(string))
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error))
