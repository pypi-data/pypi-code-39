"Hanlder of the services management:  config files templating, service reload..."
import logging
import subprocess
import hashlib
import os
import jinja2

class DaemonConfig:
    "Daemon config manager"
    def __init__(self, name, config_check, config_file, template_file):
        self._name = name
        self._config_check = config_check
        self._config_file = config_file
        self._template_file = template_file
        self._reload_command = ['sudo', 'systemctl', 'reload-or-restart', self._name]

    def _test_config(self):
        "launch command to parse config file"
        res = subprocess.run(self._config_check)
        return res.returncode == 0

    def _reload_config(self):
        "restart/reloead service"
        res = subprocess.run(self._reload_command)
        return res.returncode == 0

    def _get_previous_config_sha256(self):
        "get current config file fingerprint"
        if not os.path.exists(self._config_file):
            return 'An impossible digest'
        with open(self._config_file, "rb") as f_handle:
            read_bytes = f_handle.read()
            return hashlib.sha256(read_bytes).hexdigest()

    def _templatize_config(self, env, cache, config):
        "regenerate config and return True if fiel has changed"
        previous_sha256 = self._get_previous_config_sha256()
        tmpl = env.get_template(self._template_file)
        new_content = tmpl.render(svcs=cache.svcs, hosts=cache.nodes, config=config)
        current_sha256 = hashlib.sha256(new_content.encode('utf-8')).hexdigest()
        if current_sha256 == previous_sha256:
            logging.debug('Config %s file for %s unchanged', self._config_file, self._name)
            return False
        logging.debug('Config %s file for %s is different from existing one', self._config_file,
                      self._name)
        with open(self._config_file, 'w') as output_file:
            output_file.write(new_content)
        logging.debug('Config %s file for %s written', self._config_file, self._name)
        return True

    def update_config(self, env, cache, config):
        "refresh config"
        logging.debug('Generating config %s file for %s', self._config_file, self._name)
        if self._templatize_config(env, cache, config):
            if self._test_config():
                logging.info('Config file %s for %s is valid, reloading service',
                             self._config_file, self._name)
                if self._reload_config():
                    logging.debug('Reloading service for %s succeeded', self._name)
                else:
                    logging.error('Reloading service for %s failed', self._name)
            else:
                logging.error('Config file %s for %s is not valid!!', self._config_file,
                              self._name)

class DaemonController:
    "Class tha wrap all daemon management"
    def __init__(self, cache, config):
        self._cache = cache
        self._daemon_config = []
        for (key, item) in config['daemon_config'].items():
            logging.info('Preparing daemon configuration for %s', key)
            self._daemon_config.append(DaemonConfig(key,
                                                    item['check_command'],
                                                    item['generated_config_file'],
                                                    item['template_file']))
        self._config = config
        self._env = jinja2.Environment(loader=jinja2.FileSystemLoader(config['templates']))

    @property
    def keep_going(self):
        return True

    def sync_config(self):
        "Ensure all Daemons config files are up2date"
        for daemon in self._daemon_config:
            daemon.update_config(self._env, self._cache, self._config)
