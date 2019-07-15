# config.py: reads and writes the config.toml file, used to persist user settings for XTGen

import os
import toml
import shutil

from . import utils as utils 

class Config():

    def __init__(self, fn=None):
        self.data = self.read_config(fn)

    def name_exists(self, group, name):
        return group in self.data and name in self.data[group]
        
    def warning(self, *msg_args):
        msg = "WARNING: xtgen config file -"
        for arg in msg_args:
            msg += " " + str(arg)
        if self.get("general", "raise", suppress_warning=True):
            utils.user_error(msg)
        else:
            print(msg)

    # use "*" to require dict_key and default_value to be a named arguments
    def get(self, group, name=None, dict_key=None, default_value=None, suppress_warning=False, group_error=None, 
        prop_error=None, key_error=None):
        
        value = default_value

        if group in self.data:
            value = self.data[group]
            if name:
                if name in value:
                    value = value[name]
                    if dict_key:
                        if dict_key in value:
                            value = value[dict_key]
                        else:
                            if key_error:
                                utils.user_error(key_error)
                            if not suppress_warning:
                                self.warning("GET option dict_key not found: ", group, name, dict_key, default_value)
                            value = default_value
                else:
                    if prop_error:
                        utils.user_error(prop_error)
                    if not suppress_warning:
                        self.warning("GET option not found: ",  group, name, dict_key, default_value)
                    value = default_value
        else:
            if group_error:
                utils.user_error(group_error)
            if not suppress_warning:
                self.warning("GET option GROUP not found: ", group, name, dict_key, default_value)
            value = default_value
        return value

    # use "*" to require dict_key and value to be a named arguments
    def set(self, group, name, *, dict_key=None, value=None, suppress_warning=False):
        if group in self.data:
            gv = self.data[group]
            if name in gv:
                if dict_key:
                    obj = gv[name]
                    if not dict_key in obj:
                        if not suppress_warning:
                            self.warning("SET option dict_key not found: ", group, name, dict_key, value)
                    #print("set: obj=", obj, ", dict_key=", dict_key, ", value=", value)
                    obj[dict_key] = value
                    #print("set: post obj=", obj)
                else:
                    gv[name] = value
            else:
                if not suppress_warning:
                    self.warning("SET option name not found: ", group, name, dict_key, value)
                gv[name] = value
        else:
            raise Exception("SET option group not found: ", group, name, dict_key, value)
        
    def read_config(self, fn=None):
        if fn is None:
            config_dir = utils.get_xthome_dir() 
            utils.ensure_dir_exists(config_dir)
            fn = utils.get_config_fn()  

            if not os.path.exists(fn):
                print("XTGen config file not found; creating it from default settings...")
                file_dir = os.path.dirname(os.path.realpath(__file__))
                from_fn = file_dir + "/default_config.toml"
                shutil.copyfile(from_fn, fn)

        # read config file
        try:
            config = toml.load(fn)
        except Exception as e:
            raise Exception (f"The config file '{fn}' is not valid TOML, error: {e}")

        return config

