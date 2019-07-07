from cnvrg.modules.base_module import CnvrgBase
import cnvrg.helpers.apis_helper as apis_helper
from cnvrg.modules.errors import CnvrgError
import cnvrg.helpers.spawn_helper as spawn_helper
from cnvrg.modules.project import Project
from cnvrg.helpers.param_build_helper import LIBRARY, PROJECT, parse_params
from cnvrg.helpers.url_builder_helper import url_join
from cnvrg.modules.experiment import Experiment
import os
import re
DEFAULT_WORKING_DIR = os.path.expanduser("~/cnvrg_libraries")
class Library(CnvrgBase):
    def __init__(self, library, project=None, working_dir=None):
        owner, library = parse_params(library, LIBRARY)
        self.__working_dir = working_dir or DEFAULT_WORKING_DIR
        try:
            self.project = Project(project)
        except CnvrgError as e:
            self.project = None

        self.__library = library
        self.__owner = apis_helper.credentials.owner
        self.__info = None
        self.__path = None
        self.__cloned = self.__lib_loaded()

    def __base_url(self):
        return url_join("users", self.__owner, "libraries", self.__library)


    @staticmethod
    def list():
        owner = apis_helper.credentials.owner
        return apis_helper.get(url_join("users", owner, "libraries")).get("libraries")


    def info(self, force=False):
        """
        get info about this library
        :param force: to force api fetching
        :return: dict represent the library
        {clone_cmd: string,
        command: string,
        arguments: list of key: values(list),
        number_of_experiments: integer,
        description: string}
        """
        if self.__info and not force:
            return self.__info
        self.__info = self.__fetch_info()
        return self.info()


    def __fetch_info(self):
        resp = apis_helper.get(self.__base_url())
        return resp.get("library")



    def load(self):
        """
        load library to your local directory
        :param working_dir: path to clone the library to
        """
        if self.__lib_loaded():
            self.__path = self.__lib_path()
            return self.__path
        info = self.info()
        lib_dir = self.__lib_path()
        cmds = [
            "mkdir -p {working_dir}".format(working_dir=lib_dir),
            "cd {working_dir}".format(working_dir=lib_dir),
            info.get("clone_cmd"),
        ]
        cmds = " && ".join(cmds)

        #run the commands
        returncode = os.system(cmds)
        if returncode != 0:
            raise CnvrgError("Cant clone library")
        self.__path = lib_dir
        return lib_dir

    def __default_args(self):
        return {
            "project_dir": os.path.abspath(self.project.get_working_dir()),
            "output_dir": os.path.abspath(self.project.get_output_dir())
        }
    def __add_args(self, args=None):
        command = self.info().get("command")
        args = args or {}
        library_args = self.info().get("arguments") or []
        merged_args = {x["key"]:x["value"] for x in library_args}
        merged_args = {**merged_args, **args, **self.__default_args()}
        string_args = " ".join(map(lambda x: "--{key}={value}".format(key=x[0], value=x[1]), merged_args.items()))
        return "{cmd} {args}".format(cmd=command, args=string_args)

    def run(self, templates=None, datasets=None, image=None, commit=None, title=None, local=True, args=None):
        if local: return self.run_local(args=args)
        if not self.project: raise CnvrgError("You should specify Project on the library constructor")
        exp = self.project.run_experiment(cmd=self.info().get("command"), templates=templates, datasets=datasets, image=image, commit=commit, title=title)
        return exp


    def run_local(self, args=None):
        if not self.project:
            raise CnvrgError("Cant run a library not in a project context, please cd into cnvrg project")
        if not self.__lib_loaded(): self.load()
        raw_script = self.__add_args(args)
        script = " && ".join(["cd {working_dir}".format(working_dir=self.__lib_path()), raw_script])
        command = "cnvrg run -l --sync_before=false --sync_after=false '{command}'".format(command=script)
        pid = spawn_helper.run_async(command)
        e = None
        while e == None:
            line = pid.stdout.readline()
            line = line.decode('utf-8')
            g = re.search(r"/experiments/(.+)", line)
            if g: e = Experiment(g[1])
        return e


    def __lib_loaded(self, working_dir=None):
        return os.path.exists(os.path.join(self.__lib_path(), ".cnvrg", "config.yml"))


    def __lib_path(self):
        working_dir = self.__working_dir
        return os.path.join(working_dir, self.info().get("title"))








