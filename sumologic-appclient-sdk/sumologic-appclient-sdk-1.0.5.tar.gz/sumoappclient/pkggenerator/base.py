import shutil
import subprocess
from common.config import Config
from string import Template
import os


class PkgGenerator(object):

    RESOURCE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources")

    def get_config(self, configpath):
        cfg = Config()
        collection_config = cfg.read_config(configpath)
        deploy_metadata = collection_config["DeployMetaData"]
        deploy_config = {
            "APPNAME": deploy_metadata["APPNAME"],
            "PACKAGENAME": deploy_metadata["PACKAGENAME"],
            "SRC_FOLDER_NAME": deploy_metadata["SRC_FOLDER_NAME"],
            "COLLECTION_CONFIG": os.path.basename(configpath),
            "APPNAME_SINGLE": deploy_metadata["APPNAME"].replace(" ", '').replace("_", "")
        }

        return collection_config, deploy_config

    def remove_unwanted_files(self, PROJECT_DIR):
        print("removing build directories")

        for dirname in ["target"]:
            dirpath = os.path.join(PROJECT_DIR, dirname)
            if os.path.isdir(dirpath):
                shutil.rmtree(dirpath)

        print("removing pyc/pycache files")
        for dirpath, dirnames, filenames in os.walk(PROJECT_DIR):

            for file in filenames:
                if file.endswith("pyc") or file.endswith(".db"):
                    os.remove(os.path.join(dirpath, file))
            for dirname in dirnames:
                if dirname.startswith("__pycache__"):
                    shutil.rmtree(os.path.join(dirpath, dirname))

        print("removing zip/db files")

    def generate_file(self, basefilepath, params, target_filepath):
        with open(basefilepath) as fin:
            body = fin.read()
        sam_template = Template(body)
        sam_body = sam_template.substitute(**params)
        with open(target_filepath, "w") as fout:
            fout.write(sam_body)

    def run_command(self, cmdargs):
        self.log.debug(f"Running cmd: {' '.join(cmdargs)}")
        subprocess.run(cmdargs)

