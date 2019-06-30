#coding:utf-8
#
# PROGRAM/MODULE: Firebird Upkeep utility
# FILE:           /fbupkeep/base.py
# DESCRIPTION:    Base classes
# CREATED:        24.6.2019
#
# The contents of this file are subject to the MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Copyright (c) 2019 IBPhoenix (www.ibphoenix.com)
# All Rights Reserved.
#
# Contributor(s): Pavel Císař (original code)
#                 ______________________________________.

"""Firebird Upkeep utility - Base classes and other definitions
"""

from typing import TextIO, Dict, List, Any
import sys
import os
import logging
from weakref import proxy
from datetime import datetime
import argparse
import configparser
from pkg_resources import iter_entry_points

__version__ = '1.0'

# Exceptions

class Error(Exception):
    "Base exception for this module."

class StopError(Error):
    "Error that should stop furter processing."

# Functions

def has_option(namespace, name: str):
    "Returns True if argparse.Namespace has an option."
    return name in vars(namespace)

# Classes

class ConfigOption:
    """Task configuration option.

Attributes:
    :name:        Option name.
    :datatype:    Option datatype [str, int, float, bool or list].
    :description: Option description. Can span multiple lines.
    :required:    True if option must have a value.
    :default:     Default value.
    :proposal:    Text with proposed configuration entry (if it's different from default).
    :value:       Current optin value.
"""
    def __init__(self, name: str, datatype: Any, description: str, required: bool = False,
                 default: Any = None, proposal: Any = None):
        self.name = name
        self.datatype = datatype
        self.description = description
        self.required = required
        self.default = default
        self.proposal = proposal
        self.value = default
    def configure(self, config: configparser.ConfigParser, section: str) -> None:
        """Update option value from configuration.

Arguments:
    :config:  ConfigParser instance with configuration values.
    :section: Name of ConfigParser section that should be used to get new configuration values.
"""
        if config.has_option(section, self.name):
            if self.datatype == bool:
                self.value = config.getboolean(section, self.name)
            elif self.datatype == float:
                self.value = config.getfloat(section, self.name)
            elif self.datatype == int:
                self.value = config.getint(section, self.name)
            elif self.datatype == list:
                self.value = [value.strip() for value in config.get(section, self.name).split(',')]
            else:
                self.value = config.get(section, self.name)
    def validate(self) -> None:
        """Checks whether required option has value other than None.

Raises:
    :Error: When required option does not have a value.
"""
        if self.required and self.value is None:
            raise Error("The configuration does not define a value for the required option '%s'"
                        % (self.name))
    def get_printout(self) -> str:
        "Return option printout in 'name = value' format."
        value = self.value
        if self.datatype == bool:
            value = 'yes' if self.value else 'no'
        elif self.datatype == list:
            value = ', '.join(self.value)
        return '%s = %s' % (self.name, value)
    def get_config(self) -> List:
        """Return list of text lines suitable for use in configuration file.

Each line starts comment marker ; and ends with newline. Last line is options definition.
"""
        lines = ['; %s\n' % self.name,
                 '; %s\n' % ('-' * len(self.name)),
                 ';\n',
                 '; data type: %s\n' % self.datatype.__name__,
                 ';\n']
        if self.required:
            description = '[REQUIRED] ' + self.description
        else:
            description = '[optional] ' + self.description
        #description = '[REQUIRED] ' + self.description if self.required else self.description
        for line in description.split('\n'):
            lines.append("; %s\n" % line)
        lines.append(';\n')
        if self.proposal:
            lines.append(";%s = <UNDEFINED>, proposed value: %s\n" % (self.name, self.proposal))
        else:
            default = self.default if self.default is not None else '<UNDEFINED>'
            if self.datatype == bool and self.default is not None:
                default = 'yes' if self.default else 'no'
            lines.append(";%s = %s\n" % (self.name, default))
        return lines


class TaskConfig:
    """Task configuration options.

Attributes:
    :name: Name associated with Task Configuration [default: 'main'].
"""
    def __init__(self, name: str = 'main'):
        self.name: str = name
        self.__options: Dict[str, ConfigOption] = {}
    def __getattr__(self, name) -> Any:
        "Maps options to attributes."
        if name in self.options:
            return self.options[name].value
        else:
            raise AttributeError("Option '%s' not found." % name)
    def add(self, option: ConfigOption) -> None:
        "Add configuration option."
        if option.name in self.options:
            raise StopError("Option '%s' already defined" % option.name)
        self.__options[option.name] = option
    def add_option(self, name: str, datatype: Any, description: str, required: bool = False,
                   default: bool = None, proposal: bool = False) -> None:
        """Add new configuration option."""
        if name in self.options:
            raise StopError("Option '%s' already defined" % name)
        if proposal:
            option = ConfigOption(name, datatype, description, required, None, default)
        else:
            option = ConfigOption(name, datatype, description, required, default, None)
        self.__options[name] = option
    def get_option(self, name: str) -> ConfigOption:
        """Return ConfigOption with specified name or None."""
        return self.__options.get(name)
    def has_option(self, name: str) -> bool:
        """Return True if option with specified name is defined."""
        return name in self.__options
    def configure(self, config: configparser.ConfigParser, section: str) -> None:
        """Update configuration.

Arguments:
    :config:  ConfigParser instance with configuration values.
    :section: Name of ConfigParser section that should be used to get new configuration values.
"""
        for option in self.__options.values():
            option.configure(config, section)
    def validate(self) -> None:
        """Checks whether all required options have value other than None.

Raises:
    :Error: When required option does not have a value.
"""
        for option in self.__options.values():
            option.validate()
    def get_printout(self) -> List[str]:
        "Return list of text lines with printout of current configuration"
        lines = [option.get_printout() for option in self.options.values()]
        if self.name != 'main':
            lines.insert(0, "Configuration [%s]:" % self.name)
        return lines
    options = property(lambda self: self.__options,
                       doc="Options dictionary (name,ConfigOption).")

class LoggedObject:
    """Object with logging support.

Attributes:
    :logger:   logging.Logger instance.
    :mute:     If True, only errors and exceptions are printed (to stderr).
    :log_only: If True, all console output is suppressed.
"""
    def __init__(self):
        self.__logger: logging.Logger = None
        self.mute: bool = False
        self.log_only: bool = False
    def __get_logger(self):
        if self.__logger is None:
            self.__logger = self._create_logger()
        return self.__logger
    def _create_logger(self) -> logging.Logger:
        """Returns logging.Loger instance. Default implementation return root logger.
Descendant classes could override it to return different logger.
"""
        return logging.getLogger()
    def info(self, message: str = '', end: str = '\n') -> None:
        """Log INFO message (if present) and print the message to stdout if not suppressed."""
        if message:
            self.logger.info(message)
            if not self.mute and not self.log_only:
                print(message, end=end)
                sys.stdout.flush()
        else:
            if not self.mute and not self.log_only:
                print()
                sys.stdout.flush()
    def error(self, message: str) -> None:
        """Log ERROR message and print it to stderr if not suppressed."""
        self.logger.error(message)
        if not self.log_only:
            print(message, file=sys.stderr)
    def exception(self, message: str) -> None:
        """Log ERROR message with exception information and print it to stderr if not suppressed."""
        self.logger.exception(message)
        if not self.log_only:
            print(message, file=sys.stderr)
    def print(self, message: str = '') -> None:
        """Print the message to stdout if not suppressed."""
        if not self.mute and not self.log_only:
            print(message)
    logger = property(__get_logger, doc="Logger instance")

class Task(LoggedObject):
    """Base task.

Attributes:
    :executor:    TaskExecutor that owns this Task instance.
    :name:        Task name [default: "Task"].
    :description: Short task description [default: None]. Should NOT span multiple lines.
    :config:      TaskConfig instance.
    :verbose:     Verbose output flag [default: False].
    :report:      List of text lines with execution report [default: Empty list].
    :errors:      List of text lines with execution errors [default: Empty list].
    :timestamp:   Timestamp used for filename interpolation.
    :start:       Timestamp when task execution started (set by executor) [default: None].
    :stop:        Timestamp when task execution ended (set by executor) [default: None].
"""
    def __init__(self, executor):
        super().__init__()
        self.executor: TaskExecutor = proxy(executor)
        self.name: str = 'task'
        self.description: str = None
        self.config: TaskConfig = TaskConfig()
        self.verbose: bool = False
        self.report: List[str] = []
        self.errors: List[str] = []
        self.timestamp: datetime = None
        self.start: datetime = None
        self.stop: datetime = None
    def _create_logger(self) -> logging.Logger:
        """Returns 'fbupkeep.task' logging.Loger."""
        return logging.getLogger('fbupkeep.%s' % self.name)
    def _rename_file(self, filename: str) -> None:
        """Rename file by adding numeric suffix starting from 1. Increments suffix until
file with specified name does not exists, then renames the file.
"""
        if os.path.exists(filename):
            i = 1
            while os.path.exists('%s.%02d' % (filename, i)):
                i += 1
            self.logger.debug("Renaming logfile %s to %s", filename,
                              '%s.%02d' % (filename, i))
            os.rename(filename, '%s.%02d' % (filename, i))
    def _prepare_file(self, filename: str) -> None:
        """Prepare file for write. Creates target directory if required. If file already
exists, it's renamed using `_rename_file()`.
"""
        fdir = os.path.split(filename)[0]
        if not os.path.isdir(fdir):
            os.makedirs(fdir)
        self._rename_file(filename)
    def _open_file(self, filename: str) -> TextIO:
        """Open file for write. First prepares the file using `_prepare_file()`.
"""
        self._prepare_file(filename)
        try:
            self.logger.debug("Opening file '%s' for output", filename)
            return open(filename, mode='w')
        except Exception as exc:
            raise Error("Can't open file '%s'" % filename) from exc
    def configure(self, config: configparser.ConfigParser,
                  options: argparse.Namespace) -> List[TaskConfig]:
        """Task configuration.

Returns:
    List of TaskConfig instances used by task.

Updates the `config` attribute from `upkeep_<options.job_name>` config section.
Validates the `config`.
"""
        self.config.configure(config, 'upkeep_%s' % options.job_name)
        self.config.validate()
        return [self.config]
    def run(self) -> None:
        """Task execution. Default implementation does nothing.
"""

class TaskExecutor(LoggedObject):
    """Base task executor.

Attributes:
    :config:  TaskConfig instance.
    :verbose: Verbose output flag [default: False].
    :tasks:   List of Task instances with all installed tasks.
"""
    def __init__(self):
        super().__init__()
        self.verbose: bool = False
        self.tasks: List[Task] = []
        self.config: TaskConfig = TaskConfig()
        self.config.add_option('tasks', list,
                               "Which tasks should be executed for this job.\n" \
                               "Tasks are executed in specified order.", True)
        self.config.add_option('stop_on_error', bool,
                               "Abort execution on any error (yes) or skip the "\
                               "failing task and continue running (no).",
                               False, True)
        self.config.add_option('use_batch_time', bool,
                               "Time used for filename interpolation, batch start "\
                               "time (yes) or task start time (no).",
                               False, True)
    def _create_logger(self) -> logging.Logger:
        """Returns 'fbupkeep.executor' logging.Loger."""
        return logging.getLogger('fbupkeep.executor')
    def get_task(self, name: str) -> Task:
        """Return task with specified name or None."""
        for task in self.tasks:
            if task.name == name:
                return task
        return None
    def load_tasks(self) -> None:
        """Load all registered tasks."""
        option = self.config.get_option('tasks')
        option.description += "\n\nInstalled tasks:"
        for task_entry in iter_entry_points('fbupkeep_tasks'):
            try:
                task_class = task_entry.load()
                task = task_class(self)
                self.tasks.append(task)
                option.description += "\n  %s = %s" % (task.name, task.description)
            except Exception:
                self.exception("Can't load task '%s'" % task_entry)
    def run(self, config: configparser.ConfigParser, options: argparse.Namespace) -> None:
        """Run tasks.

Recognized argument options:
    :log_only: Suppress all screen output.
    :quiet:    Suppress informational screen output, errors are still print out to stderr.
    :verbose:  Additional informational screen output.
    :dry_run:  Prepare execution but do not run tasks. Print used configuration as verbose
               output.
"""
        start = datetime.now()
        task_config = {}
        # process configuration
        if has_option(options, 'log_only'):
            self.log_only = options.log_only
            for task in self.tasks:
                task.log_only = options.log_only
        if has_option(options, 'quiet'):
            self.mute = options.quiet
            for task in self.tasks:
                task.mute = options.quiet
        if has_option(options, 'verbose'):
            self.verbose = options.verbose
            for task in self.tasks:
                task.verbose = options.verbose
        if has_option(options, 'dry_run'):
            dry_run = options.dry_run
        section = 'upkeep_%s' % options.job_name
        self.config.configure(config, section)
        self.config.validate()
        # collect tasks for execution
        tasks_to_run = []
        for task_name in self.config.tasks:
            task_name = task_name.strip()
            task = self.get_task(task_name)
            if task:
                tasks_to_run.append(task)
            else:
                raise StopError("Unknown task '%s'." % task_name)
        # configure tasks for execution
        final_list = []
        for task in tasks_to_run:
            self.logger.debug("Configuring task '%s'", task.name)
            try:
                task_config[task.name] = task.configure(config, options)
                final_list.append(task)
            except Error as exc:
                if not self.config.stop_on_error:
                    self.error(str(exc))
                else:
                    raise StopError(str(exc)) from exc
        # Execute tasks
        if dry_run and self.verbose:
            self.print("Task executor configuration:")
            for line in self.config.get_printout():
                self.print(line)
            self.print()
        for task in final_list:
            if not dry_run:
                self.info("Running task '%s'" % task.name)
                try:
                    task.start = datetime.now()
                    task.timestamp = start if self.config.use_batch_time else task.start
                    try:
                        task.run()
                    finally:
                        task.stop = datetime.now()
                except Error as exc:
                    if not self.config.stop_on_error:
                        self.error(str(exc))
                    else:
                        raise StopError(str(exc)) from exc
            else:
                if self.verbose:
                    self.print("Task '%s' configuration:" % task.name)
                    for cfg in task_config[task.name]:
                        for line in cfg.get_printout():
                            self.print(line)
                        self.print()
        self.info("Finished %d task(s), execution time %s" % (len(final_list),
                                                              datetime.now() - start))
    def write_default_config(self, cfg_file: TextIO) -> None:
        """Write default configuration for all known tasks into file.

Arguments:
    :cfg_file: Openned file-like object.
"""
        # Write list of tasks
        cfg_file.write("""; ---------------------------
; Task executor configuration
; ---------------------------
""")
        for option in self.config.options.values():
            cfg_file.writelines(option.get_config())
            cfg_file.write("\n")
        #
        seen_options = {}
        multi_used = {}
        # collect all options from tasks
        for task in self.tasks:
            for name in task.config.options:
                seen_options.setdefault(name, list()).append(task.name)
        # Options used by multiple tasks
        for name, tasks in seen_options.items():
            if len(tasks) > 1:
                multi_used[name] = tasks
        cfg_file.write("; ------------------------------\n")
        cfg_file.write("; Options used by multiple tasks\n")
        cfg_file.write("; ------------------------------\n\n")
        for name, tasks in multi_used.items():
            task = self.get_task(tasks[0])
            option = task.config.get_option(name)
            lines = option.get_config()
            lines.insert(len(lines)-1, "; Used by tasks: %s\n" % ', '.join(tasks))
            lines.insert(len(lines)-1, ";\n")
            cfg_file.writelines(lines)
            cfg_file.write("\n")
        # Options used by only one task
        for task in self.tasks:
            title = "Task '%s'" % task.name
            cfg_file.write("; %s\n" % ('-' *len(title)))
            cfg_file.write("; %s\n" % title)
            cfg_file.write("; %s\n\n" % ('-' *len(title)))
            has_options = False
            for name, option in task.config.options.items():
                if name not in multi_used:
                    has_options = True
                    cfg_file.writelines(option.get_config())
                    cfg_file.write("\n")
            if not has_options:
                if task.config.options:
                    cfg_file.write("; This task has no private options (not shared with other tasks).\n")
                else:
                    cfg_file.write("; This task has no configuration options.\n")
                cfg_file.write("\n")
