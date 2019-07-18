import configparser
from bqmigratrr.commands.migrator import up
import os
from importlib.machinery import SourceFileLoader
import sys
from pathlib import Path

import coloredlogs
import logging

coloredlogs.install()

name = 'bqmigratrr'


current_dir = os.getcwd()
config = configparser.ConfigParser()

config_path = '{}/migrations.ini'.format(current_dir)

config_file = Path(config_path)
if not config_file.is_file:
    raise Exception("migrations.ini cannot be found")

config.read(config_path)
migrations_dir = config["DIRECTORIES"].get("migrations", "./migrations")


def run(migration_type: str):
    for filename in os.listdir(migrations_dir):
        # for file in files:
        if filename != "__init__.py" and filename.endswith(".py"):
            file_path = "{}/{}/{}".format(current_dir,
                                          migrations_dir, filename)
            migrationfile = SourceFileLoader(
                filename, file_path).load_module()

            if hasattr(migrationfile, "Migration"):
                logging.info("{} is a valid migration".format(filename))
                migration = migrationfile.Migration()
            
                if migration_type == "up":
                    up(migration, filename)
                # elif migration == "down":
                #     down(migration)
            else:
                logging.error("{} is not a valid migration".format(filename))


def init():
    migration_type = ""
    for index, arg in enumerate(sys.argv):
        if arg in ['--migrate']:
            migration_type = "up"
            del sys.argv[index]
            break

        if arg in ['--migrate:undo']:
            migration_type = "down"
            del sys.argv[index]
            break

        if arg in ['--migrate:test']:
            migration_type = 'test'
            del sys.argv[index]
            break

    if len(sys.argv) > 1:
        print(
            f'Usage: python {sys.argv[0]} [ --migrate|migrate:undo ]')
        raise Exception()

    run(migration_type)
