#core.py
#Author: Willem Hunt, whunt1@uvm.edu

import os
import sys
import csv
import argparse

from . import fetch
from . import logger
from . import config as cfg

class Core():

    def __init__(self):
        self.download_results = {}

        self.parser = argparse.ArgumentParser(description="Batch-download files from the internet", prog="Snag")
        loudness = self.parser.add_mutually_exclusive_group()
        loudness.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode.", default=False)
        loudness.add_argument("-q", "--quiet", action="store_true", help="Enable quiet mode.", default=False)
        self.parser.add_argument("-c", "--chars", type=int, help="Maximum characters to print to screen per log entry.", default=0)
        self.parser.add_argument("-l", "--log", help="Enable logging at specified location", default="")
        self.parser.add_argument("-o", "--out", help="Specify output directory", default=os.getcwd())
        
        config = self.parser.add_mutually_exclusive_group()
        config.add_argument("-e", "--example", help="Use example config.", action="store_true", default=False)
        config.add_argument("config", nargs="?", help="File to read download data from.", default="")
        
        args = self.parser.parse_args()

        if not args.log == "":
            self.log = True
            self.log_file = args.log
        else:
            self.log = False
            self.log_file = ""

        self.quiet          = args.quiet
        self.verbose        = args.verbose
        self.echo_limit     = args.chars
        self.config_file    = args.config
        self.out_dir        = args.out
        self.use_example    = args.example

        log_folder = os.path.join(os.getcwd(), self.log_file)[:self.log_file.rfind("/")+1]
        if self.log and not os.path.exists(log_folder):
            os.makedirs(log_folder)    

        #Initialize Logger object
        self.logger = logger.Logger(self.log, self.quiet, self.verbose,self.echo_limit, self.log_file)           
        self.logger.start()

        self.logger.log("Using the following options:")
        self.logger.log("Logging: " + str(self.log))
        self.logger.log("Verbose Mode: " + str(self.verbose))
        self.logger.log("Quiet Mode: " + str(self.quiet))
        if self.echo_limit > 0:
            self.logger.log("Message Character Limit: " + self.echo_limit)

        #Read programs from config
        self.programs = self.read_config()

    def download(self, programs):

        if not self.programs:
            return False

        for program in programs:
            name    = program[0] + "." + program[3]
            url     = program[1]
            locator = program[2]
            folder  = program[4]
            success = fetch.download(self.out_dir, name, url, locator, folder, self.logger)
            print("Status: " + success)
            self.download_results[name] = success
        return True

    def read_config(self):
        programs = []
        if not self.config_file == "":
            self.logger.log("# Reading config file  at: " + self.config_file)
            try:
                with open(self.config_file) as config:
                    lines = csv.reader(config, delimiter=',')
                    for line in lines:
                        if not line[0][0] == "#":
                            programs.append(line)
            except:
                self.logger.log("Unable to find config file at: " + self.config_file, True)
                self.logger.log("Please specify config file location with \"config=\" option.")
                return False
        elif self.use_example:
            self.logger.log("# Using example config")
            programs = cfg.example_config
        else:
            self.parser.print_help()

        self.logger.log("\n\nFiles to download:")
        for program in programs:
            self.logger.log(program[0] + "." + program[3] + " - " + program[1])

        return programs
    
    def log_results(self):
        self.logger.log("\nDownload Results:", True)
        for download, result in self.download_results.items():
            self.logger.log(("{:40s} {:10s}".format(download+":", result)))


