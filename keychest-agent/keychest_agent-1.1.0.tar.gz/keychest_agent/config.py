#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***
Module:
***

 Copyright (C) Smart Arcs Ltd, registered in the United Kingdom.
 This file is owned exclusively by Smart Arcs Ltd.
 Unauthorized copying of this file, via any medium is strictly prohibited
 Proprietary and confidential
 Written by Dan Cvrcek <support@smartarchitects.co.uk>, May 2018
"""
import os
import sys
import json
import collections
import errno
from datetime import datetime
from keychest_agent.core import Core

from keychest_agent.logger import logger

__copyright__ = 'Smart Arcs Ltd'
__email__ = 'support@smartarchitects.co.uk'
__status__ = 'Development'


class KCConfig(object):
    """Configuration object, handles file read/write"""

    # let's create a static version - default file
    config = None

    CONFIG_FILE = 'agent_config.json'

    # noinspection PyUnusedLocal
    def __init__(self, json_db=None, *args, **kwargs):
        self.json = json_db

    def ensure_config(self):
        if self.json is None:
            self.json = collections.OrderedDict()
        if 'config' not in self.json:
            self.json['config'] = collections.OrderedDict()

    def has_nonempty_config(self):
        return self.json is not None and 'config' in self.json and len(self.json['config']) > 0

    def get_config(self, key, default=None):
        if not self.has_nonempty_config():
            logger.warning("Request for non-existent configuration option, returning default value",
                           name=key, value=default)
            return default
        return self.json['config'][key] if key in self.json['config'] else default

    @classmethod
    def get_static_config(cls, key, default=None):
        if KCConfig.config is None:
            return default
        return KCConfig.config.json['config'][key] if key in KCConfig.config.json['config'] else default

    # @staticmethod
    # def init_log(idx=None, level=logging.DEBUG):
    #     """
    #     Initializes logging
    #     :return:
    #     """
    #     log_folder = KCConfig.get_custom_config_file_path('var/log/keychest')
    #     util.make_or_verify_dir(log_folder)
    #
    #     if idx is not None:
    #         file_name = 'server_%d.log' % idx
    #     else:
    #         file_name = 'server.log'
    #     _logger = QueueHandler.set_logger(os.path.join(log_folder, file_name))
    #     _logger.setLevel(level)
    #     return _logger

    def set_config(self, key, val):
        self.ensure_config()
        self.json['config'][key] = val

    def to_string(self):
        return json.dumps(self.json, indent=2) if self.has_nonempty_config() else ""

    @property
    def logging_usage_sampling(self):
        return self.get_config("logging_usage_sampling", 1)

    @property
    def logging_server(self):  # this points to Laravel
        return self.get_config('logging_server', 'https://keychest.net/api/v1.0/agent/log')

    @logging_server.setter
    def logging_server(self, value):
        self.set_config('logging_server', value)

    @property
    def agent_name(self):
        return self.get_config('agent_name', "KEYCHEST_" + datetime.utcnow().strftime("%Y%m%d%H%M"))

    @agent_name.setter
    def agent_name(self, value):
        self.set_config('agent_name', value)

    @property
    def logging_params(self):
        return self.get_config('logging_params', {})

    @property
    def control_server(self):  # this points to Engine's RESTful server
        return self.get_config('control_server', 'http://keychest.net:8443/api/v1.0/agent/control')

    @control_server.setter
    def control_server(self, value):
        self.set_config('control_server', value)

    @property
    def agent_email(self):
        return self.get_config('agent_email', "dummy@keychest.net")

    @agent_email.setter
    def agent_email(self, value):
        self.set_config('agent_email', value)

    @property
    def logging_remote(self):
        return self.get_config('logging_remote', ["ERROR", "INFO", "CRITICAL", "WARNING", "DEBUG", "USE"])

    @logging_remote.setter
    def logging_remote(self, value):
        self.set_config('logging_remote', value)

    @property
    def logging_local(self):
        return self.get_config('logging_local', ["ERROR", "INFO", "CRITICAL", "WARNING", "DEBUG", "USE", "TRACE"])

    @logging_local.setter
    def logging_local(self, value):
        self.set_config('logging_local', value)

    # The number of processes for audit engine
    @property
    def agent_processes(self):
        return self.get_config('agent_processes', 1)

    @agent_processes.setter
    def agent_processes(self, value):
        if isinstance(value, int) and (value > 0):
            self.set_config('agent_processes', value)

    @property
    def simple_tls(self):
        return self.get_config('simple_tls', True)

    @simple_tls.setter
    def simple_tls(self, value):
        if isinstance(value, bool):
            self.set_config('simple_tls', value)

    @property
    def git_version(self):
        return self.get_config('git_version', "")

    @git_version.setter
    def git_version(self, value):
        if isinstance(value, bytes):
            value = value.decode().strip()
        self.set_config('git_version', value)

    # The max time for each process to run
    @property
    def process_running_time(self):
        return self.get_config('process_running_time', 0)

    # API key for master
    @property
    def agent_apikey(self):
        return self.get_config('agent_apikey', None)

    @agent_apikey.setter
    def agent_apikey(self, val):
        self.set_config('agent_apikey', val)

    @property
    def max_process_memory(self):
        return self.get_config('max_process_memory', 200)

    @max_process_memory.setter
    def max_process_memory(self, value):
        if isinstance(value, int):
            self.set_config('max_process_memory', value)

    @property
    def local_config(self):
        return self.get_config('local_config', False)

    @local_config.setter
    def local_config(self, value):
        if isinstance(value, bool):
            self.set_config('local_config', value)

    @property
    def reverse_proxy(self):
        return self.get_config('reverse_proxy', True)

    @reverse_proxy.setter
    def reverse_proxy(self, value):
        if isinstance(value, bool):
            self.set_config('reverse_proxy', value)

    @property
    def dns_server(self):
        temp = self.get_config('dns_server', None)
        if (temp is None) or (len(temp) < 1):
            return None
        else:
            return temp

    @dns_server.setter
    def dns_server(self, value):
        if isinstance(value, str) or (value is None):
            self.set_config('dns_server', value)

    @property
    def upstream_permitted_host(self):
        temp = self.get_config('upstream_permitted_host', None)
        if (temp is None) or (len(temp) < 1):
            return None
        else:
            return temp

    @upstream_permitted_host.setter
    def upstream_permitted_host(self, value):
        if isinstance(value, str) or (value is None):
            self.set_config('upstream_permitted_host', value)

    @property
    def agent_proxy_ports(self):
        return self.get_config('agent_proxy_ports', "10001")

    @agent_proxy_ports.setter
    def agent_proxy_ports(self, value):
        if isinstance(value, str):
            parts = value.split('-')
            if len(parts) > 3:
                err = False
                for x in parts:
                    try:
                        v = int(x)
                        if (v < 1023) or (v > 65535):
                            err = True
                            break
                    except ValueError:
                        err = True
                        break
                if not err:
                    self.set_config('agent_proxy_ports', value)
        elif value is None:
            self.set_config('agent_proxy_ports', value)

    @property
    def audit_server_port(self):
        return self.get_config('audit_server_port',  10000)

    @audit_server_port.setter
    def audit_server_port(self, value):
        self.set_config('audit_server_port', value)

    @property
    def upstream_host(self):
        return self.get_config('upstream_host', 'keychest.net')

    @upstream_host.setter
    def upstream_host(self, value):
        self.set_config('upstream_host', value)

    @property
    def agent_command_list(self):
        return self.get_config('agent_command_list', None)

    @agent_command_list.setter
    def agent_command_list(self, value):
        self.set_config('agent_command_list', value)

    @property
    def control_schedule(self):
        return self.get_config('control_schedule', 20)

    @control_schedule.setter
    def control_schedule(self, value):
        if isinstance(value, int) and (value >= 20) and (value <= 36000):
            self.set_config('control_schedule', int(value))

    @property
    def discovery_schedule(self):
        return self.get_config('discovery_schedule', 86400)

    @discovery_schedule.setter
    def discovery_schedule(self, value):
        if isinstance(value, int) and (value >= 60) and (value <= 604800):
            self.set_config('discovery_schedule', int(value))

    @property
    def permitted_space(self):
        return self.get_config('permitted_space', "0.0.0.0/0:0")

    @permitted_space.setter
    def permitted_space(self, value):
        self.set_config('permitted_space', value)

    @property
    def banned_space(self):
        return self.get_config('banned_space', '')

    @banned_space.setter
    def banned_space(self, value):
        self.set_config('banned_space', value)

    @property
    def throttling(self):
        return self.get_config('throttling')

    @throttling.setter
    def throttling(self, value):
        self.set_config('throttling', value)

    @property
    def piddir(self):
        return KCConfig.get_custom_config_file_path('var/run/keychest')

    @property
    def logdir(self):
        return KCConfig.get_custom_config_file_path('var/log/keychest')

    @property
    def sockdir(self):
        return KCConfig.get_custom_config_file_path('var/sock')

    @property
    def discovery_threads(self):
        return self.get_config('discovery_threads', 1)

    @discovery_threads.setter
    def discovery_threads(self, value):
        if isinstance(value, int) and 0 < value < 100:
            self.set_config("discovery_threads", value)

    @property
    def default_port(self):
        return self.get_config("default_port", 443)

    @property
    def internal_socket(self):
        return self.get_config("internal_socket", 9999)

    @default_port.setter
    def default_port(self, value):
        if isinstance(value, int) and 0 < value < 65536:
            self.set_config('default_port', value)

    @property
    def connect_timeout(self):
        return self.get_config("connect_timeout", 4)

    @connect_timeout.setter
    def connect_timeout(self, value):
        if isinstance(value, int) and value > 0:
            self.set_config("connect_timeout", value)

    @property
    def ad_password(self):
        return self.get_config('ad_password', "")

    @property
    def ad_user(self):
        return self.get_config('ad_user', "")

    @classmethod
    def mask_local_item(cls,  key, value):
        local_items = {
            'ad_user': "<set locally>",
            'ad_password': "<set locally>",
            'agent_apikey': "%5.5s  ..."
        }

        if key in local_items:
            # noinspection PyBroadException
            try:
                return local_items[key] % value
            except:
                return local_items[key]
        else:
            return value

    @classmethod
    def create_config_dict(cls, config, hide_local=True):

        result = None
        try:
            result = json.loads(json.dumps(config))
            if hide_local:
                for item, value in result.items():
                    # noinspection PyBroadException
                    try:
                        result[item]  =  KCConfig.mask_local_item(item, value)
                    except Exception:
                        pass
        except Exception as ex:
            logger.error("Exception when loading the agent configuration", cause=str(ex))

        return result

    @classmethod
    def default_config(cls):
        def_cfg = collections.OrderedDict()

        def_cfg['agent_name'] = "KEYCHEST" + datetime.utcnow().strftime("%Y%m%d%H%M")
        def_cfg['agent_apikey'] = ""
        def_cfg['agent_email'] = "dummy@keychest.net"
        def_cfg['logging_server'] = 'https://keychest.net/api/v1.0/agent/log'
        def_cfg['logging_params'] = {}
        def_cfg['control_server'] = 'http://keychest.net:8443/api/v1.0/agent/control'
        def_cfg['audit_server_port'] = 10000
        def_cfg['upstream_host'] = 'keychest.net'
        def_cfg['local_config'] = False  # when True, KeyChest pulls config, otherwise it pushes it to agents
        def_cfg['reverse_proxy'] = True  # when True, audits are done via a reverse proxy
        def_cfg['dns_server'] = ""  # when an IP address / domain name is provided it has to be used
        #  it can contain IP range / domain mask & port, eg 10.0.0.1-10.0.0.3:443
        def_cfg['upstream_permitted_host'] = ""  # if set, only requests from those IP addresses are allowed
        def_cfg['agent_processes'] = 1  # limits the number of concurrent proxies
        def_cfg['agent_proxy_ports'] = 10001  # the starting port that the agent will use for proxies to listen on
        def_cfg['agent_cmd_list'] = ""  # if set, it limits the commands it's allowed to proxy
        def_cfg['max_process_memory'] = 200
        def_cfg['logging_remote'] = ["ERROR", "INFO", "CRITICAL", "WARNING", "DEBUG", "USE"]
        def_cfg['logging_local'] = ["ERROR", "INFO", "CRITICAL", "WARNING", "DEBUG", "TRACE", "USE"]
        def_cfg['simple_tls'] = True
        def_cfg['control_schedule'] = 5
        def_cfg['discovery_schedule'] = 7200
        def_cfg['permitted_space'] = "0.0.0.0/0:0"
        def_cfg['banned_space'] = ""
        def_cfg['throttling'] = 0
        def_cfg['discovery_threads'] = 1
        def_cfg['default_port'] = 443
        def_cfg['ad_password'] = ""
        def_cfg['ad_user'] = ""
        def_cfg['discovery_threads'] = 10
        def_cfg['connect_timeout'] = 3
    # def_cfg['agent_running_time'] = 0  # it will restart when the time limit is reached

        root = collections.OrderedDict()
        root['config'] = def_cfg
        return cls(json_db=root)

    @classmethod
    def get_config_file_path(cls):
        """Returns basic configuration file"""
        return os.path.join(Core.CONFIG_DIR, KCConfig.CONFIG_FILE)

    @classmethod
    def config_file_exists(cls):
        conf_name = KCConfig.get_config_file_path()
        return os.path.exists(conf_name) and os.path.isfile(conf_name)

    @classmethod
    def is_configuration_nonempty(cls):
        return KCConfig.config is not None and KCConfig.config.has_nonempty_config()

    @classmethod
    def read_configuration(cls, force=False):
        if KCConfig.config and (force is not True):
            return KCConfig.config
        else:
            if not KCConfig.config_file_exists():
                return None

            conf_name = KCConfig.get_config_file_path()
            KCConfig.config = KCConfig.from_file(conf_name)
            return KCConfig.config

    @classmethod
    def write_configuration(cls, cfg):

        try:
            os.makedirs(Core.CONFIG_DIR, mode=0o755)
        except OSError as exception:
            if exception.errno == errno.EEXIST:
                pass
            else:
                raise

        conf_name = KCConfig.get_config_file_path()
        with os.fdopen(os.open(conf_name, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), 'w') as config_file:
            config_file.write('// \n')
            config_file.write('// Agent config file generated: %s\n' % datetime.utcnow().strftime("%Y-%m-%d %H:%M"))
            config_file.write('// \n')
            config_file.write(cfg.to_string() + "\n\n")
        KCConfig.config = cfg
        return conf_name

    @classmethod
    def from_json(cls, json_string):
        return cls(json_db=json.loads(json_string, object_pairs_hook=collections.OrderedDict))

    @classmethod
    def from_file(cls, file_name):
        with open(file_name, 'r') as f:
            read_lines = [x.strip() for x in f.read().split('\n')]
            lines = []
            for line in read_lines:
                if line.startswith('//'):
                    continue
                lines.append(line)

            my_config = None
            try:
                my_config = KCConfig.from_json('\n'.join(lines))
            except Exception as ex:
                logger.error("Error parsing configuration file", query=file_name, cause=str(ex))
                sys.stdout.write("Error parsing configuration file: " + str(ex))
                sys.stdout.flush()
                exit(-1)

            return my_config
        pass

    @classmethod
    def get_custom_config_file_path(cls, filename):
        """Returns configuration file for my own file"""
        return os.path.join(Core.CONFIG_DIR, filename)
