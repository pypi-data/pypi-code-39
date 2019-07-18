import configparser
from bqmigratrr.commands.migrator import up
import os
from importlib.machinery import SourceFileLoader
import sys
name = 'bqmigratrr'


current_dir = os.getcwd()

config = configparser.ConfigParser()
config.read('{}/migrations.ini'.format(current_dir))

migrations_dir = config["DIRECTORIES"].get("migrations", "./migrations")


def run(migration_type: str):
    for filename in os.listdir(migrations_dir):
        # for file in files:
        if filename != "__init__.py" and filename.endswith(".py"):
            file_path = "{}/{}/{}".format(current_dir,
                                          migrations_dir, filename)
            migrationfile = SourceFileLoader(
                filename, file_path).load_module()
            migration = migrationfile.Migration()
            if migration_type == "up":
                up(migration)
            # elif migration == "down":
            #     down(migration)


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

    if len(sys.argv) > 1:
        print(
            f'Usage: python {sys.argv[0]} [ --migrate|migrate:undo ]')
        raise Exception()

    run(migration_type)
