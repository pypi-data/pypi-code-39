#coding:utf-8
#
# PROGRAM/MODULE: Firebird Upkeep utility
# FILE:           /fbupkeep/tasks.py
# DESCRIPTION:    Standard tasks
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

"""Firebird Upkeep utility - Standard tasks
"""

from typing import List
import os
import argparse
import configparser
import fnmatch
import datetime
import fdb
from fbupkeep.base import Error, Task, TaskConfig

class TaskGstat(Task):
    """Task that collects gstat database statistics.
"""
    def __init__(self, executor):
        super().__init__(executor)
        self.name = 'gstat'
        self.description = "Save gstat statistics to file."
        self.config.add_option('database', str, "Database specification (path or alias)",
                               True)
        self.config.add_option('host', str, "Firebird server host")
        self.config.add_option('user', str, "User name to access Firebird service manager",
                               True, os.environ.get('ISC_USER', 'SYSDBA'))
        self.config.add_option('password', str, "Password to access Firebird service manager",
                               True, os.environ.get('ISC_PASSWORD', 'masterkey'))
        self.config.add_option('gstat_dir', str, "Directory for output files", True,
                               '${output_dir}/gstat', True)
        self.config.add_option('gstat_filename', str,
                               "Base filename template (supports strftime directives)",
                               True, '${filename}.gstat', True)
    def run(self) -> None:
        """Task execution.
"""
        filename = os.path.join(self.config.gstat_dir,
                                self.timestamp.strftime(self.config.gstat_filename))
        #
        if self.config.host:
            svc_host = self.config.host + ':service_mgr'
        else:
            svc_host = 'service_mgr'
        self.logger.debug("Connecting service (host:%s, user:%s, password:%s)" % (svc_host,
                                                                                  self.config.user,
                                                                                  self.config.password))
        svc = fdb.services.connect(host=svc_host, user=self.config.user,
                                   password=self.config.password)
        lines_written = 0
        bytes_written = 0
        output = self._open_file(filename)
        try:
            svc.get_statistics(self.config.database,
                               show_user_data_pages=1,
                               show_user_index_pages=1,
                               show_system_tables_and_indexes=1,
                               show_record_versions=1)
            for line in svc:
                lines_written += 1
                bytes_written += len(line) + len('\n')
                output.write(line)
                output.write('\n')
            output.close()
            if self.verbose:
                self.info("gstat statistics collected, %d bytes in %d lines" % (bytes_written,
                                                                                lines_written))
            self.logger.debug("gstat output file closed, %d bytes in %d lines" % (bytes_written,
                                                                                  lines_written))
        finally:
            svc.close()
            self.logger.debug("Service closed")

class TaskGbak(Task):
    """Task that creates logical (gbak) database backup.
"""
    def __init__(self, executor):
        super().__init__(executor)
        self.name = 'gbak'
        self.description = "Create logical (gbak) database backup."
        self.config.add_option('database', str, "Database specification (path or alias)",
                               True)
        self.config.add_option('host', str, "Firebird server host")
        self.config.add_option('user', str, "User name to access Firebird service manager",
                               True, os.environ.get('ISC_USER', 'SYSDBA'))
        self.config.add_option('password', str, "Password to access Firebird service manager",
                               True, os.environ.get('ISC_PASSWORD', 'masterkey'))
        self.config.add_option('gbak_dir', str, "Directory for backup files", True,
                               '${output_dir}/backup', True)
        self.config.add_option('gbak_filename', str,
                               "Backup filename template (supports strftime directives)",
                               True, '${filename}.fbk', True)
        self.config.add_option('gbak_gc', bool, "Whether backup should perform garbage collection",
                               False, True)
        self.config.add_option('gbak_logname', str,
                               "Backup log filename template (supports strftime directives)\n" \
                               "If not specified, backup log is not created.")
    def run(self) -> None:
        """Task execution.
"""
        filename = os.path.join(self.config.gbak_dir,
                                self.timestamp.strftime(self.config.gbak_filename))
        self._prepare_file(filename)
        #
        if self.config.host:
            svc_host = self.config.host + ':service_mgr'
        else:
            svc_host = 'service_mgr'
        self.logger.debug("Connecting service (host:%s, user:%s, password:%s)" % (svc_host,
                                                                                  self.config.user,
                                                                                  self.config.password))
        svc = fdb.services.connect(host=svc_host, user=self.config.user,
                                   password=self.config.password)
        if self.config.gbak_logname:
            logfilename = os.path.join(self.config.gbak_dir,
                                       self.timestamp.strftime(self.config.gbak_logname))
            lines_written = 0
            bytes_written = 0
            output = self._open_file(logfilename)
        try:
            svc.backup(self.config.database, filename,
                       collect_garbage=self.config.gbak_gc)
            if self.config.gbak_logname:
                for line in svc:
                    lines_written += 1
                    bytes_written += len(line) + len('\n')
                    output.write(line)
                    output.write('\n')
                output.close()
                if self.verbose:
                    self.info("gbak log saved, %d bytes in %d lines" % (bytes_written,
                                                                        lines_written))
                self.logger.debug("gbak log closed, %d bytes in %d lines" % (bytes_written,
                                                                             lines_written))
            else:
                svc.wait()
        finally:
            svc.close()
            self.logger.debug("Service closed")

class TaskGbakRestore(Task):
    """Task that restores database from logical (gbak) backup file.
"""
    def __init__(self, executor):
        super().__init__(executor)
        self.name = 'gbak_restore'
        self.description = "Restore database from logical (gbak) backup."
        self.config.add_option('database', str, "Database specification (path or alias)",
                               True)
        self.config.add_option('host', str, "Firebird server host")
        self.config.add_option('user', str, "User name to access Firebird service manager",
                               True, os.environ.get('ISC_USER', 'SYSDBA'))
        self.config.add_option('password', str, "Password to access Firebird service manager",
                               True, os.environ.get('ISC_PASSWORD', 'masterkey'))
        self.config.add_option('gbak_dir', str, "Directory for backup files", True,
                               '${output_dir}/backup')
        self.config.add_option('gbak_filename', str,
                               "Backup filename template (supports strftime directives)",
                               True, '${filename}.fbk', True)
        self.config.add_option('gbak_restore_dir', str, "Directory for restored databases",
                               True, '${output_dir}/restore', True)
        self.config.add_option('gbak_restore_filename', str,
                               "Restored database filename template (supports strftime directives)",
                               True, '${filename}.fdb', True)
        self.config.add_option('gbak_restore_logname', str,
                               "Restore log filename template (supports strftime directives)\n" \
                               "If not specified, restore log is not created.")
    def run(self) -> None:
        """Task execution.
"""
        backup_filename = os.path.join(self.config.gbak_dir,
                                       self.start.strftime(self.config.gbak_filename))
        if not os.path.exists(backup_filename):
            raise Error("Backup file '%s' not found" % backup_filename)
        database_filename = os.path.join(self.config.gbak_restore_dir,
                                         self.start.strftime(self.config.gbak_restore_filename))
        self._prepare_file(database_filename)
        #
        if self.config.host:
            svc_host = self.config.host + ':service_mgr'
        else:
            svc_host = 'service_mgr'
        self.logger.debug("Connecting service (host:%s, user:%s, password:%s)" % (svc_host,
                                                                                  self.config.user,
                                                                                  self.config.password))
        svc = fdb.services.connect(host=svc_host, user=self.config.user,
                                   password=self.config.password)
        if self.config.gbak_restore_logname:
            logfilename = os.path.join(self.config.gbak_restore_dir,
                                       self.start.strftime(self.config.gbak_restore_logname))
            lines_written = 0
            bytes_written = 0
            output = self._open_file(logfilename)
        try:
            svc.restore(backup_filename, database_filename)
            if self.config.gbak_restore_logname:
                for line in svc:
                    lines_written += 1
                    bytes_written += len(line) + len('\n')
                    output.write(line)
                    output.write('\n')
                output.close()
                if self.verbose:
                    self.info("gbak_restore log saved, %d bytes in %d lines" % (bytes_written,
                                                                                lines_written))
                self.logger.debug("gbak_restore log closed, %d bytes in %d lines" % (bytes_written,
                                                                                     lines_written))
            else:
                svc.wait()
        finally:
            svc.close()
            self.logger.debug("Service closed")

class TaskSweep(Task):
    """Task that performs database sweep.
"""
    def __init__(self, executor):
        super().__init__(executor)
        self.name = 'sweep'
        self.description = "Perform database sweep operation."
        self.config.add_option('database', str, "Database specification (path or alias)",
                               True)
        self.config.add_option('host', str, "Firebird server host")
        self.config.add_option('user', str, "User name to access Firebird service manager",
                               True, os.environ.get('ISC_USER', 'SYSDBA'))
        self.config.add_option('password', str, "Password to access Firebird service manager",
                               True, os.environ.get('ISC_PASSWORD', 'masterkey'))
    def run(self) -> None:
        """Task execution.
"""
        if self.config.host:
            svc_host = self.config.host + ':service_mgr'
        else:
            svc_host = 'service_mgr'
        self.logger.debug("Connecting service (host:%s, user:%s, password:%s)" % (svc_host,
                                                                                  self.config.user,
                                                                                  self.config.password))
        svc = fdb.services.connect(host=svc_host, user=self.config.user,
                                   password=self.config.password)
        try:
            svc.sweep(self.config.database)
        finally:
            svc.close()
            self.logger.debug("Service closed")

class TaskIndexRecompute(Task):
    """Task that recomputes database indices.
"""
    def __init__(self, executor):
        super().__init__(executor)
        self.name = 'idx_recompute'
        self.description = "Recompute statistics of all database indices."
        self.config.add_option('database', str, "Database specification (path or alias)",
                               True)
        self.config.add_option('host', str, "Firebird server host")
        self.config.add_option('user', str, "User name for database access",
                               True, os.environ.get('ISC_USER', 'SYSDBA'))
        self.config.add_option('password', str, "Password for database access",
                               True, os.environ.get('ISC_PASSWORD', 'masterkey'))
    def run(self) -> None:
        """Task execution.
"""
        def recompute(idx):
            if self.verbose:
                self.info("Recoputing index '%s'" % idx.name)
            try:
                sqlcmd = idx.get_sql_for('recompute')
                con.begin()
                cursor.execute(sqlcmd)
                con.commit()
            except Exception as exc:
                self.exception(str(exc))

        self.logger.debug("Connecting (database:%s, host:%s, user:%s, password:%s)" % (self.config.database,
                                                                                       self.config.host,
                                                                                       self.config.user,
                                                                                       self.config.password))
        con = fdb.connect(database=self.config.database, user=self.config.user,
                          password=self.config.password, host=self.config.host)
        cursor = con.cursor()
        try:
            for idx in con.schema.indices:
                recompute(idx)
            for idx in con.schema.sysindices:
                recompute(idx)
        finally:
            con.close()
            self.logger.debug("Database connection closed")

class TaskIndexRebuild(Task):
    """Task that recomputes database indices.
"""
    def __init__(self, executor):
        super().__init__(executor)
        self.name = 'idx_rebuild'
        self.description = "Rebuild all user indices in database."
        self.config.add_option('database', str, "Database specification (path or alias)",
                               True)
        self.config.add_option('host', str, "Firebird server host")
        self.config.add_option('user', str, "User name for database access",
                               True, os.environ.get('ISC_USER', 'SYSDBA'))
        self.config.add_option('password', str, "Password for database access",
                               True, os.environ.get('ISC_PASSWORD', 'masterkey'))
    def run(self) -> None:
        """Task execution.
"""
        def recompute(idx):
            if self.verbose:
                self.info("Rebuilding index '%s'" % idx.name)
            try:
                # deactivate
                sqlcmd = idx.get_sql_for('deactivate')
                con.begin()
                cursor.execute(sqlcmd)
                con.commit()
                # activate
                sqlcmd = idx.get_sql_for('activate')
                con.begin()
                cursor.execute(sqlcmd)
                con.commit()
            except Exception as exc:
                self.exception(str(exc))

        self.logger.debug("Connecting (database:%s, host:%s, user:%s, password:%s)" % (self.config.database,
                                                                                       self.config.host,
                                                                                       self.config.user,
                                                                                       self.config.password))
        con = fdb.connect(database=self.config.database, user=self.config.user,
                          password=self.config.password, host=self.config.host)
        cursor = con.cursor()
        try:
            for idx in con.schema.indices:
                recompute(idx)
        finally:
            con.close()
            self.logger.debug("Database connection closed")

class TaskRemoveOld(Task):
    """Task that removes old files.
"""
    def __init__(self, executor):
        super().__init__(executor)
        self.dir_configs: List[TaskConfig] = []
        self.name = 'remove_old'
        self.description = "Remove old files."
        self.config.add_option('remove_old_from', list, """Comma separated list of configuration
section names. Files are removed according to configuration sections.
Each section must have next options:
  path: Directory for processing
  files_expire_after: Number of days to keep files, older files could be removed

Optional options:
  pattern: Filename pattern (supports Unix shell-style wildcards), [default: *]
  recursive: yes/no, [default:no] """, True)
    def configure(self, config: configparser.ConfigParser, options: argparse.Namespace) -> None:
        """Task configuration.
"""
        result = super().configure(config, options)
        for section in self.config.remove_old_from:
            section = section.strip()
            if not config.has_section(section):
                raise Error("Configuration section [%s] not found" % section)
            dir_config = TaskConfig(section)
            dir_config.add_option('path', str, 'Directory for processing', True)
            dir_config.add_option('files_expire_after', int,
                                  'Number of days to keep files, older files could be removed',
                                  True)
            dir_config.add_option('pattern', str,
                                  'Filename pattern (supports Unix shell-style wildcards)',
                                  False, '*')
            dir_config.add_option('recursive', bool, 'Process path recursively')
            dir_config.configure(config, section)
            dir_config.validate()
            self.dir_configs.append(dir_config)
            result.append(dir_config)
        return result
    def run(self) -> None:
        """Task execution.
"""
        for dir_config in self.dir_configs:
            for dirpath, _, filenames in os.walk(dir_config.path):
                for filename in fnmatch.filter(filenames, dir_config.pattern):
                    try:
                        filespec = os.path.join(dirpath, filename)
                        age = self.timestamp - datetime.datetime.fromtimestamp(os.path.getmtime(filespec))
                        if age.days > dir_config.files_expire_after:
                            os.remove(filespec)
                            self.info("Removed old file '%s'" % filespec)
                    except Exception as exc:
                        self.error(str(exc))
                if not dir_config.recursive:
                    break
