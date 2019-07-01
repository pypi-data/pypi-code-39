import os

import configparser

class GeneralConfig(object):

    """
    Quick module to handle a normalized config pull. Will search environment sections. To use environment varibles
    for invidual settings, the ENV should be named with {SECTION}_{KEY}. So for google apikey, you should set a
    variable GOOGLE_APIKEY={some apikey}
    """

    def __init__(self, config_section, defaults=None, config_path=None, secrets_dir=None, throw_exception=False):
        """
        Config files will be checked in ~/.config/general default. If a GENERAL_CONFIG env exists, it will pull the path from
        there When setting variable values, make sure that you can have an ALL_CAPS setting that will work without
        colliding in an environment variable Settings and sections should be lower_case_underscore

        """
        if defaults is None:
            defaults = {}

        if not secrets_dir and 'SECRETS_DIR' in os.environ:
            secrets_dir = os.environ.get("SECRETS_DIR")

        self.secrets_dir = secrets_dir

        self.parser = configparser.ConfigParser(defaults=defaults)

        if not config_path and 'GENERAL_CONFIG' in os.environ:
            config_path = os.environ.get('GENERAL_CONFIG')

        if not config_path:
            for known_path in [os.path.expanduser("~") + "/.config/general", "/opt/.config/general", "/etc/general/config"]:
                if os.path.isfile(known_path):
                    config_path = known_path
                    break

        self.config_path = config_path

        if self.config_path:
            self.parser.read(os.path.expanduser(config_path))

        # We'll stub out a blank section in case it doesn't exist, this prevents exceptions from being thrown
        if not self.parser.has_section(config_section):
            self.parser.add_section(config_section)

        self.config_section = config_section

        self.throw_exception = throw_exception

    def get(self, *args, **kwargs):
        """ Returns raw value

            Returns:
                str: raw value from env variable or config file
        """
        return self.get_setting(*args, **kwargs)

    def get_int(self, *args, **kwargs):
        """ Cast raw value to int

            Returns:
                int: value cast to int
        """
        return int(self.get_setting(*args, **kwargs))

    def getint(self, *args, **kwargs):
        """ backwards compatibility with configparser """
        return self.get_int(*args, **kwargs)

    def get_boolean(self, *args, **kwargs):
        """ Returns boolean for parsed value. Parsed value must be one of

            ["1", "yes", "on", "true", "0", "no", "off", "false"]

            Returns:
                bool: boolean value representation of provided value

            Raises:
                ValueError: value provided was not a known boolean string value.
        """

        value = self.get_setting(*args, **kwargs)

        if isinstance(value, int):
            return bool(value)
        elif isinstance(value, bool):
            return value
        elif isinstance(value, str):
            value = value.lower()
            if value in ["1", "yes", "on", "true"]:
                return True
            elif value in ["0", "no", "off", "false"]:
                return False
            else:
                raise ValueError("unexpected value '%s' provided" % value)
        else:
            raise ValueError("unexpected value '%s' provided" % value)

    def getboolean(self, *args, **kwargs):
        """ backwards compatibility with configparser """
        return self.get_boolean(*args, **kwargs)

    def get_setting(self, name, section=None, throw_exception=None):
        """
            Setting names should always be lower_case_underscore
            Well check the config and environment variables for the name. Environment variables will be made all caps
            when checked

            Args:
                name (str): attribute name to get
                section (Optional[str]): section name to retrieve attribute from, will default to self.config_section
                throw_exception (Optional[bool]): throw exceptions or not if invalid, default to self.throw_exception

        """

        if not section:
            section = self.config_section

        env_key = section.upper() + "_" + name.upper()
        if env_key in os.environ:
            return os.environ.get(env_key)

        if self.secrets_dir:
            if os.path.isfile(self.secrets_dir + section + "_" + name):
                with open(self.secrets_dir + name, "r") as fh:
                    return "".join(fh.readlines()).rstrip("\r\n").rstrip("\n")

        if throw_exception is None:
            throw_exception = self.throw_exception

        # ensure section exists - needed here in addition to init for cases where user specifies section in
        # `get_setting()`
        if not self.parser.has_section(section):
            self.parser.add_section(section)

        if throw_exception:
            return self.parser.get(section, name)

        return self.parser.get(section, name, fallback=None)
