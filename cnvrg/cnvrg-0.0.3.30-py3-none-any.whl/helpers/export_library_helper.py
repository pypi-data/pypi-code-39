import yaml
import os
import tempfile
import tarfile
import cnvrg.modules.errors as errors
import cnvrg.actions.project_actions as project_actions
import cnvrg.helpers.apis_helper as apis_helper

DEFAULT_WORKING_DIR = os.path.expanduser("~/cnvrg_libraries")

class LibraryConfig():
    def __init__(self, working_dir):
        working_dir = working_dir or os.curdir
        self.working_dir = working_dir
        self.config_path = os.path.join(working_dir, 'library.yml')
        if not os.path.exists(self.config_path): raise errors.CnvrgError("Cant find library in directory.")
        with open(self.config_path, 'r') as f:
            self.config_yaml = yaml.load(f)
            self.__load_fields()


    def __load_fields(self):
        self.__inflate_defaults()
        self.__verify_key_exists("command", "Please enter your library command")
        self.__inflate_file("requirements.txt", "requirements")
        self.__inflate_file("readme.me", "documentation")

    def __inflate_file(self, file, key):
        fpath = os.path.join(self.working_dir, file)
        if os.path.exists(fpath):
            self.config_yaml[key] = open(fpath, 'r').read()

    def __inflate_defaults(self):
        self.config_yaml = {**{
            "title": os.path.basename(self.working_dir),
            "description": "Cnvrg Library",
            "icon": None,
            "version": "1",
            "key": os.path.basename(self.working_dir)
        }, **self.config_yaml}

    def __verify_key_exists(self, key, prompt_message=None, alternative=None):
        if key not in self.config_yaml: self.__prompt_for_key(key, prompt_message)

    def __prompt_for_key(self,key, question=None):
        answer = input(question)
        self.config_yaml[key] = answer

    def getter(self):
        return self.config_yaml



def get_config(working_dir=None):
    return LibraryConfig(working_dir).getter()



def export_library(working_dir=None):
    working_dir = working_dir or os.curdir
    config = get_config(working_dir=working_dir)
    tar_path = os.path.join(working_dir, "{key}.{version}.tar".format(key=config.get("key"), version=config.get("version")))
    with tarfile.open(tar_path, "w:gz") as tar_handle:
        for root, dirs, files in os.walk(working_dir):
            for file in files:
                file_fullpath = os.path.join(root, file)
                tar_handle.add(file_fullpath, arcname=os.path.join(os.path.relpath(file_fullpath, working_dir)))

    file = {"file": open(tar_path, "rb")}
    apis_helper.send_file(apis_helper.url_join("users", apis_helper.credentials.owner, "libraries"), files=file, data=config)


def load_library(tar_url, library_dest):
    f = apis_helper.download_raw_file(tar_url)
    with tempfile.NamedTemporaryFile() as tfile:
        tfile.write(f)
        tfile.seek(0)
        with tarfile.open(tfile.name, "r:gz") as tar_handle:
            tar_handle.extractall(library_dest)