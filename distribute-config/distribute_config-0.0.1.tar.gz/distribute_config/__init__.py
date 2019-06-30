import os
import sys
import argparse
import yaml
from typing import Dict

from .variable import Variable


class Config:
    class __Config:
        def __init__(self):
            # variables maps the "path" of a variable to an instance of class Variable
            self.variables = {}
            self.namespace = ""
            self.parser = argparse.ArgumentParser(description='Arguments')
            self.parser.add_argument("-c", type=str, default="config.yml", help="relative path to config file")

        def define_var(self, name, default, description, type, is_list=False):
            if self.namespace:
                name = self.namespace + "." + name
            variable = Variable(name, default, description, type, is_list)
            self.__add_variables(variable)

            self.parser.add_argument("--" + variable.name, type=type, help=variable.description)

        def __add_variables(self, variable: Variable):
            """add variable to variables dict and create path corresponding with the variable name. 

            Args:
                variable (Variable): variable to add
            """
            splited_path = variable.name.split(".")
            variables_sub_group = self.variables
            for sub_path in splited_path[:-1]:
                if not sub_path in variables_sub_group:
                    variables_sub_group[sub_path] = {}
                variables_sub_group = variables_sub_group[sub_path]
            if splited_path[-1] not in variables_sub_group:
                variables_sub_group[splited_path[-1]] = variable
            else:
                raise KeyError("variable already defined")

        def convert_to_dict(self):
            return self._convert_to_dict(self.variables)

        @classmethod
        def _convert_to_dict(cls, variables):
            out_dict = {}
            for key in variables:
                if type(variables[key]) == Variable:
                    out_dict[key] = variables[key].get_value()
                else:
                    out_dict[key] = cls._convert_to_dict(variables[key])
            return out_dict

    __instance = None

    def __init__(self):
        if not Config.__instance:
            Config.__instance = Config.__Config()

    @classmethod
    def clear(cls):
        cls.__instance = Config.__Config()

    @classmethod
    def _set_namespace(cls, name):
        cls.__instance.namespace = name

    @classmethod
    def define_int(cls, var_name, default, description):
        cls.__instance.define_var(var_name, default, description, int)

    @classmethod
    def define_float(cls, var_name, default, description):
        cls.__instance.define_var(var_name, default, description, float)

    @classmethod
    def define_str(cls, var_name, default, description):
        cls.__instance.define_var(var_name, default, description, str)

    @classmethod
    def define_str_list(cls, var_name, default, description):
        cls.__instance.define_var(var_name, default, description, str, is_list=True)

    @classmethod
    def define_int_list(cls, var_name, default, description):
        cls.__instance.define_var(var_name, default, description, int, is_list=True)

    @classmethod
    def define_float_list(cls, var_name, default, description):
        cls.__instance.define_var(var_name, default, description, float, is_list=True)

    @classmethod
    def get_var(cls, name):
        path = name.split(".")
        variables = cls.__instance.variables
        for sub_path in path:
            variables = variables[sub_path]

        if type(variables) == Variable:
            return variables.get_value()
        else:
            return variables

    @classmethod
    def set_var(cls, name, val):
        path = name.split(".")
        variables = cls.__instance.variables
        for sub_path in path:
            variables = variables[sub_path]

        assert type(variables) == Variable
        variables.set_value(val)

    @classmethod
    def get_dict(cls):
        return cls.__instance.convert_to_dict()

    @classmethod
    def write_conf(cls, file_path):
        with open(file_path, "w") as f:
            yaml.dump(cls.get_dict(), f, default_flow_style=False)

    @classmethod
    def load_conf(cls):
        """This method load the conf in 3 steps:
        1. Load the config.yml file if exist, or load a file specified by -c option when starting the program
        2. Load the env variables 
        3. parse the python commande line
        """
        args = cls.__instance.parser.parse_args()

        config_file_name = args.c
        if not os.path.exists(config_file_name):
            print("Create config file", config_file_name, "with default value")
            cls.write_conf(config_file_name)
            print("Please update config file and restart")
            print("You can find information on all parameters by running with --help")

        # 1
        with open(config_file_name, 'r') as stream:
            yml_content = yaml.safe_load(stream)
        cls.load_dict(yml_content, cls.__instance.variables)

        # 2
        for var in os.environ:
            path = ".".join(var.lower().split("__"))
            try:
                cls.set_var(path, os.environ[var])
                print("Load env variable", var)
            except KeyError:
                pass

        # 3
        print(vars(args))
        for key in vars(args):
            if key == "c":
                continue
            cls.set_var(key, vars(args)[key])

    @staticmethod
    def load_dict(loading_dict, variables):
        for key in loading_dict:
            if type(loading_dict[key]) == dict:
                Config.load_dict(loading_dict[key], variables[key])
            else:
                variables[key].set_value(loading_dict[key])

    @classmethod
    def _append_namespace(cls, name):
        if cls.__instance.namespace == "":
            cls._set_namespace(name)
        else:
            cls._set_namespace(cls.__instance.namespace + "." + name)

    @classmethod
    def _pop_namespace(cls):
        cls._set_namespace(".".join(cls.__instance.namespace.split(".")[:-1]))

    @classmethod
    def namespace(cls, name):
        class _ConfigNamespace:
            def __init__(self, name):
                cls._append_namespace(name)

            def __enter__(self):
                return self

            def __exit__(self, type, value, traceback):
                cls._pop_namespace()

        return _ConfigNamespace(name)


Config()
