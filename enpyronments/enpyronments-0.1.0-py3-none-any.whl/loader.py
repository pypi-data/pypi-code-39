import os
import re
from glob import glob
from importlib import import_module

from base import Settings
from utils import UsePath

default_prefix = "env"
default_ext = ".py"
default_sep = "_"
default_builtin_pattern = r"^__(.+)__$"
default_attribute_pattern = r"^[A-Z_0-9]+$"
default_root = os.getcwd()
LOCAL = "local"
MODE = "MODE"


def get_module_dict(module, attrs):
    """Given a module and a list of attributes to extract, return a dict of the
    attributes and their values
    
    Arguments:
        module {module} -- Module to extract attributes from
        attrs {iterable} -- Iterable of attribute names to extract
    """
    return dict((attr, getattr(module, attr)) for attr in attrs)


class Loader:
    """A loader that follows a set resolution order to determin which environment settings will be loaded"""

    def __init__(
        self,
        root=default_root,
        prefix=default_prefix,
        ext=default_ext,
        sep=default_sep,
        builtin_pattern=default_builtin_pattern,
        attribute_pattern=default_attribute_pattern,
    ):
        """The settings loader.

        Keyword Arguments:
            root {str} -- Path representing the root directory to start importing from (default: {os.getcwd()})
            prefix {str} -- Prefix environment settings files will have (default: {prefix})
            ext {str} -- Extension environment settings files will have (must be .py for now) (default: {ext})
            sep {str} -- Separator between environment specifiers (default: {sep})
            builtin_pattern {str} -- Regex pattern used to identify which attributes are builtins, which should be ignored (default: {builtin_pattern})
            attribute_pattern {str} -- Regex pattern used to identify which attributes should be included (default: {attribute_pattern})
        """
        self.root = root
        self.prefix = prefix
        self.ext = ext
        self.sep = sep
        self.builtin_pattern = builtin_pattern
        self.attribute_pattern = attribute_pattern

    def find_modules(self, package):
        """Searches for modules in package that match the glob pattern 
        {prefix}*{ext}
        
        Arguments:
            package {str} -- package from which to import modules
        """
        pattern = os.path.join(self.root, package, f"{self.prefix}*{self.ext}")
        with UsePath(self.root):
            for module_path in glob(pattern):
                module_name = module_path.split(os.path.sep)[-1].replace(self.ext, "")
                yield import_module(f"{package}.{module_name}")

    def get_module_attrs(self, module):
        """Given a module object, extract the names of all attributes that match attribute_pattern,
        excluding those that match bulitin_pattern.
        
        Arguments:
            module {module} -- The module to extract attributes of
        """
        keys = module.__dict__.keys()
        for key in keys:
            # skip over attributes that look like builtins
            if re.match(self.builtin_pattern, key):
                continue
            # skip any attributes that don't look like our regex
            if not re.match(self.attribute_pattern, key):
                continue
            yield key

    def get_mode(self, settings_by_module):
        """Given a dictionary of settings, determine what mode to extract settings from
        
        Arguments:
            settings_by_module {dict} -- settings dictionary
        """
        def get_mode_setting(name):
            """ Helper function to pull the mode setting from the settings dict """
            if name in settings_by_module:
                return settings_by_module[name].get(MODE)
            return None
            
        local_settings_module = f'{self.prefix}{self.sep}{LOCAL}'
        local_mode = get_mode_setting(local_settings_module)

        if local_mode:
            return local_mode

        global_settings_module = f'{self.prefix}'
        global_mode = get_mode_setting(global_settings_module)
        
        return global_mode

    def get_mode_settings(self, mode, settings_by_module):
        """Exclude settings for modes we're not using
        
        Arguments:
            mode {str} -- name of mode to load modules for
            settings_by_module {dict} -- settings dictionary
        """
        if not mode:
            return settings_by_module

        mode_settings = {}
        for key, val in settings_by_module.items():
            if (
                mode in key.split(self.sep)
                or key == self.prefix
                or key == self.sep.join([self.prefix, LOCAL])
            ):
                mode_settings[key] = val
        return mode_settings

    def get_load_order(self, mode):
        """ Defines the order in which settings are loaded. If needed, you can override this method in a subclass to
        define custom logic for your use case 
        
        Arguments:
            mode {str} -- name of mode to load
        """

        load_order = [
            self.sep.join([self.prefix]),
            self.sep.join([self.prefix, LOCAL]),
            self.sep.join([self.prefix, mode]),
            self.sep.join([self.prefix, mode, LOCAL]),
        ]
        return load_order

    def load_settings(self, package):
        """Load the settings files found in package, prioritizing local settings, then mode specific settings, then
        general settings (i.e. env_dev_local beats env_dev beats env_local beats env)
        
        Arguments:
            package {str} -- package name
        """
        modules = self.find_modules(package)

        settings_by_module = {}
        for module in modules:
            settings_by_module[module.__name__.split('.')[-1]] = get_module_dict(
                module, self.get_module_attrs(module)
            )
        
        mode = self.get_mode(settings_by_module)
        mode_settings = self.get_mode_settings(mode, settings_by_module)

        load_order = self.get_load_order(mode)

        settings = Settings()
        for key in load_order:
            new_settings = mode_settings.get(key)
            if new_settings:
                settings.update(new_settings)

        return settings
