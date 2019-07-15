'''
Preprocessor for Foliant documentation authoring tool.
Allows to run arbitrary external commands.
'''

import re
from subprocess import run, PIPE, STDOUT, CalledProcessError

from foliant.utils import output
from foliant.preprocessors.base import BasePreprocessor


class Preprocessor(BasePreprocessor):
    defaults = {
        'commands': [],
        'targets': [],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('runcommands')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

    def apply(self):
        self.logger.info('Applying preprocessor')

        self.logger.debug(f'Allowed targets: {self.options["targets"]}')
        self.logger.debug(f'Current target: {self.context["target"]}')

        if not self.options['targets'] or self.context['target'] in self.options['targets']:
            if self.options['commands']:
                for command in self.options['commands']:
                    command = command.replace(
                        '${PROJECT_DIR}',
                        f'{self.project_path.absolute().as_posix()}'
                    )

                    command = command.replace(
                        '${SRC_DIR}',
                        f'{(self.project_path / self.config["src_dir"]).absolute().as_posix()}'
                    )

                    command = command.replace(
                        '${WORKING_DIR}',
                        f'{self.working_dir.absolute().as_posix()}'
                    )

                    command = command.replace(
                        '${BACKEND}',
                        f'{self.context["backend"]}'
                    )

                    command = command.replace(
                        '${TARGET}',
                        f'{self.context["target"]}'
                    )

                    try:
                        self.logger.debug(f'Running command: {command}')

                        command_output = run(command, shell=True, check=True, stdout=PIPE, stderr=STDOUT)

                        if command_output.stdout:
                            command_output_decoded = command_output.stdout.decode('utf8', errors='ignore')

                            output(command_output_decoded, self.quiet)

                            self.logger.debug(f'Output of the command: {command_output_decoded}')

                    except CalledProcessError as exception:
                        self.logger.error(str(exception))

                        raise RuntimeError(f'Failed: {exception.output.decode()}')

        self.logger.info('Preprocessor applied')
