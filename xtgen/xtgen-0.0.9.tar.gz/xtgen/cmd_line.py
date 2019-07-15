# cmd_line.py: implements the command line version of the XTGen tool
import os
import sys
import json
import math
import time
import arrow
import shutil
import socket
import argparse
import platform
import datetime
import subprocess
import numpy as np

from time import sleep
from fnmatch import fnmatch
from collections import OrderedDict


from . import help
from . import utils as utils 
from .config import Config
from .scanner import Scanner
from .pytorch_gen import PytorchGenerator
from .keras_gen import KerasGenerator


USER_SETTINGS = "~/.xt/user_settings.json"

class CmdLine():
    def __init__(self):
        self.explicit_options = {}
        self.core = None
        self.client = None

    def build_default_options(self):
        # xt options are 1 of 4 types:
        #   flag, boolean, number, string
        # flags and booleans don't require an "=value" after then, the others do.
        bool_options = [
            "help", "zap", "timing", "diagnostics", "raise"]

        other_options = [
            "framework", "dataset", "model"]

        opt1 = {opt:True for opt in bool_options }
        opt2 = {opt:False for opt in other_options }
        options = {**opt1, **opt2}

        # define all options in self.config (if not already defined there)
        for key, value in options.items():
            if (not self.config.name_exists("core", key)) and (not self.config.name_exists("general", key)):
                #print("set option only config: key=", key, ", value=", None)
                self.config.set("general", key, value=None, suppress_warning=True)

        self.bool_options = bool_options
        self.options = options

    def is_boolean_value(self, option, tok):
        value = tok
        is_bool = False
        if tok and tok in self.bool_options:
            is_bool = tok.lower() in ["true", "false", "on", "off", "0", "1"]
            if is_bool:
                value = (tok.lower() in ["true", "on", "1"])
        
        return is_bool, value

    def set_option_value(self, option, value):
        #print("setting option=", option, ", to value=", value)

        # convert strings to numbers, when possible
        if isinstance(value, str):
            value = utils.make_numeric_if_possible(value)

        # record as an explicit option
        self.explicit_options[option] = value

        # merge with config info (look in core, reports, then general)
        groups = ["features", "internal"]
        found = False

        for group in groups:
            if self.config.name_exists(group, option):
                self.config.set(group, option, value=value)
                found = True
                break

        if not found:
            self.config.set("general", option, value=value)

    def parse_option(self, tok):
        options = self.options

        #print("option=", option)
        option = tok[2:]     # stip off "--"

        match = self.match(option, options)
        if not match:
            utils.user_error(f"unrecognized option: --{option}")

        option = match
        #print("option=", option)
        #print("options[option]=", options[option])

        tok = self.scanner.scan()        # skip over option name
        optional_value = (options[option] == True)
        #print("option=", option, ", optional_value=", optional_value)

        # the "=" is optional, skip over it if it exists
        if tok == "=":
            tok = self.scanner.scan()
            optional_value = False

        is_bool, value = self.is_boolean_value(option, tok)
        #print("option=", option, ", is_bool=", is_bool, ", value=", value)

        if optional_value:
            # parse optional boolean value
            if is_bool:
                self.set_option_value(option, value)
                tok = self.scanner.scan()       
            else:
                # mentioning a flag/bool without a value sets it to True
                self.set_option_value(option, True)
        else:
            # parse a rquired boolean/string/number value
            if is_bool:
                self.set_option_value(option, value)
            else:
                if not value and option == "workspace":
                    utils.user_error("--ws option must be set to a workspace name; value=" + str(value))
                self.set_option_value(option, tok)
            tok = self.scanner.scan()               

            #options[option] = value  

        return tok

    def edit_config_file(self):
        # let user edit the CONFIG file
        fn = utils.get_config_fn()
        print(f"invoking your default .toml editor on: {fn}")
        utils.open_file_with_default_app(fn)


    def is_option(self, tok):
        ''' return True if tok is the name of an option
        '''
        found = False

        if tok:
            if tok.startswith("--"):
                found = True
            else:
                for option in self.options:
                    if self.match(tok, option):
                        found = True
                        break

        return found

    def process_named_options(self, tok):
        '''
        now that cmd keywords and main value have been processed, parse any remaining
        named options and store in config data, for cmd to access as it runs.
        '''
        while tok:
            if tok.startswith("--"):
                # remove optional "--"
                tok = tok[2:]

            #print("tok=", tok)
            match = False

            for option in self.options:
                match = self.match(tok, option)
                if match:
                    break

            if not match:
                utils.user_error("unrecognized command option: {}".format(tok))

            tok = self.scanner.scan()       # skip over "match" keyword
            #print("match=", match, ", next tok=", tok)

            if not tok:
                self.set_option_value(match, True)
            elif (tok == "="):
                value = self.scanner.scan()     # skip over "="
                is_bool, value = self.is_boolean_value(match, value)
                #print("option=", option, ", is_bool=", is_bool, ", value=", value)

                self.set_option_value(match, value)
                tok = self.scanner.scan()             # skip over option value
            elif not self.is_option(tok):
                # not a recognized option name, assume it is a value 
                self.set_option_value(match, tok)
                tok = self.scanner.scan()             # skip over option value

        # now that options have been updated, should update our cached options
        self.on_options_changed()


    def match(self, tok, keywords):
        match = None
        if tok:
            tok = tok.lower()
            if isinstance(keywords, str):
                keywords = [ keywords ]

            for kw in keywords:
                if kw.startswith(tok) and len(tok) >= min(4, len(kw)):
                    match = kw
                    break
        return match


    def parse_optional_value(self, tok):
        value = None
        if (tok == "="):
            value = self.scanner.scan()     # skip over optional "="
            tok = self.scanner.scan()     # skip over value
        elif tok and not self.is_option(tok):
            value = tok
            tok = self.scanner.scan()     # skip over value

        return value, tok

    def generate(self, tok):

        utils.diag("initializing")

        # parse output directory
        output_dir = tok
        if not output_dir:
            utils.user_error("output directory must be specified")        

        self.scanner.scan()     # skip over output directory

        if self.scanner.token != None:
            utils.user_error("unexpected text after output directory: " + self.scanner.token)

        if os.path.exists(output_dir):
            zap = self.config.get("general", "zap")
            if zap:
                shutil.rmtree(output_dir)
            else:
                utils.user_error("output directory already exists (use --zap to override)")

        fw = self.config.get("general", "framework")
        dataset = self.config.get("general", "dataset")
        model = self.config.get("general", "model")

        if fw == "pytorch":
            generator = PytorchGenerator()
            count = generator.generate(output_dir, dataset, model)
        elif fw == "keras":
            generator = KerasGenerator()
            count = generator.generate(output_dir, dataset, model)
        else:
            utils.user_error("unrecognized framework: " + str(fw))

        print("fw={}, data={}, model={}: {} files generated to: {}".format(fw, dataset, model, count, output_dir))

    def print_cmd_help(self):
        utils.enable_ansi_escape_chars_on_windows_10()
        text = help.get_cmd_help()
        print(text)

    def parse_cmdline_args(self):
        # first, handle commands that do not require XTClient 
        self.verb = "start" if sys.platform == "win32" else "open"

        tok = self.scanner.token
        #print("first command tok=", tok)
        
        is_help = self.match(tok, "help")
        if is_help or self.config.get("general", "help"):
            if is_help:
                tok = self.scanner.scan()

            if not tok or self.match(tok, "about"):
                text = help.get_about_help()
                print(text)
            elif self.match(tok, "api"):
                text = help.get_api_help()
                print(text)
            elif self.match(tok, ["cmds", "commands"]):
                self.print_cmd_help()
            else:
                utils.user_error("unrecognized help argument: " + tok)
        elif self.match(tok, ["version", "build"]):
            print(utils.BUILD)
        elif self.match(tok, "configuration"):
            self.edit_config_file()
        else:
            self.generate(tok)

    def parse_cmdline_options(self, args):
        self.build_default_options()

        cmd = " ".join(args)
        self.scanner = Scanner(cmd)
        tok = self.scanner.scan()
        #print("first tok=", tok)

        # parse options
        while tok and tok.startswith("--"):
            tok = self.parse_option(tok)
            #print("tok=", tok)

    def init_config_settings_and_options(self, args):
        # load config file
        self.config = Config()

        # apply cmdline options
        self.parse_cmdline_options(args)

        self.on_options_changed()
        timing_enabled = self.config.get("internal", "timing")
        utils.set_timing_data(self.started, timing_enabled)
        utils.timing("started")

    def on_options_changed(self):
        # now that config, settings, and options are loaded, its safe to cache
        # some settings to make the code cleaner

        utils.diagnostics = self.config.get("internal", "diagnostics")

    def run_core(self):
        error = False

        # wrap all COMMAND PROCESSING in a try/except
        try:
            cmd_args = self.args

            # handle short and long help functions before initializing the XT Client 
            if len(cmd_args) == 0:
                text = help.get_about_help()
                print(text)
            elif cmd_args[0] == "--help":
                self.print_cmd_help()
            else:
                # start parsing commands 
                self.init_config_settings_and_options(cmd_args)
                self.parse_cmdline_args()
        except BaseException as ex:
            print(ex)
            error = True

            # does user want a stack-trace?
            if self.config.get("internal", "raise", suppress_warning=True):
                raise ex

        return error

    def add_quotes_to_string_args(self):
        for i, arg in enumerate(self.args):

            # don't process an app's args
            # if arg in ["run", "python"]:
            #     break

            if " " in arg:  
                if arg.startswith("--"):
                    # --option=value
                    parts = arg.split("=")
                    assert(len(parts)==2)
                    arg = parts[0] + '="' + parts[1] + '"'
                else:
                    arg = '"' + arg + '"'
                self.args[i] = arg

    def run(self, cmd=None):
        self.started = time.time() - .8   # we lose about .8 secs from xt.bat
        #utils.feedback("starting", is_first=True)

        #print("cmd=", cmd)
        #print("xtgen: sys.argv=", sys.argv)

        # command can be passed or taken from command line
        if cmd:
            self.args = cmd.split(" ")
        else:
            self.args = sys.argv[1:]
        
        self.add_quotes_to_string_args()
        #print("self.args=", self.args)

        error = self.run_core()

        utils.timing("exiting")
        #print("exiting with exit(0)")
        if error:
            sys.exit(1)     # signal to caller (quick-test.py) that we aborted
        else:
            sys.exit(0)     # exit cleanly, even if we caught a ctrl-C while waiting for experiment to complete
