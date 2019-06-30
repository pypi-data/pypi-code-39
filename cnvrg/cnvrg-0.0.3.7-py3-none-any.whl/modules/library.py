from cnvrg.modules.base_module import CnvrgBase
import cnvrg.helpers.apis_helper as apis_helper
from cnvrg.modules.errors import CnvrgError
from cnvrg.helpers.config_helper import config_type, CONFIG_TYPE_PROJECT
from cnvrg.modules.project import Project
import os
import re
class Library(CnvrgBase):
    def __init__(self, library):
        self.__cloned = False
        self.__library = library
        self.__owner = apis_helper.credentials.owner
        self.__info = None
        self.__path = None

    def __base_url(self):
        return os.path.join("users", self.__owner, "libraries", self.__library)


    @staticmethod
    def list():
        owner = apis_helper.credentials.owner
        return apis_helper.get(os.path.join("users", owner, "libraries")).get("libraries")


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



    def load(self, working_dir=None):
        """
        load library to your local directory
        :param working_dir: path to clone the library to
        """
        working_dir = working_dir or os.curdir
        if self.__lib_loaded(working_dir=working_dir):
            self.__path = self.__lib_path(working_dir=working_dir)
            return self.__path
        info = self.info()
        lib_dir = self.__lib_path(working_dir=working_dir)
        cmds = [
            "mkdir -p {working_dir}".format(working_dir=lib_dir),
            "cd {working_dir}".format(working_dir=lib_dir),
            info.get("clone_cmd"),
        ]
        if config_type(working_dir) == CONFIG_TYPE_PROJECT:
            ## if inside project, add the file to the gitignore
            cmds.append("echo 'libraries/**' >> .cnvrgignore")

        cmds = " && ".join(cmds)

        #run the commands
        returncode = os.system(cmds)
        if returncode != 0:
            raise CnvrgError("Cant clone library")
        self.__path = lib_dir
        return lib_dir

    def __add_args(self, args=None):
        command = self.info().get("command")
        args = args or {}
        library_args = self.info().get("arguments") or []
        merged_args = {x["key"]:x["value"] for x in library_args}
        merged_args = {**merged_args, **args}
        string_args = " ".join(map(lambda x: "--{key}={value}".format(key=x[0], value=x[1]), merged_args.items()))
        return "{cmd} {args}".format(cmd=command, args=string_args)

    def run(self, templates=None, datasets=None, image=None, commit=None, title=None, project_url=None, local=True, args=None):
        if local: return self.run_local(args=args)
        project = Project(project_url=project_url)
        exp = project.run_experiment(cmd=self.info().get("command"), templates=templates, datasets=datasets, image=image, commit=commit, title=title)
        return exp




    def run_local(self, working_dir=None, args=None):
        working_dir = working_dir or self.__path
        if config_type(os.curdir) != CONFIG_TYPE_PROJECT:
            raise CnvrgError("Cant run a library not in a project context, please cd into cnvrg project")
        raw_script = self.__add_args(args)
        script = re.sub(self.info().get("file"), os.path.join(os.path.realpath(working_dir), self.info().get("file")), raw_script)
        commands = " && ".join([
            "cnvrg run -l {script}".format(script=script)
        ])
        os.system(commands)

    def __lib_loaded(self, working_dir=None):
        return os.path.exists(os.path.join(self.__lib_path(working_dir=working_dir), ".cnvrg", "config.yml"))


    def __lib_path(self, working_dir=None):
        working_dir = working_dir or os.curdir
        return os.path.join(working_dir, "libraries", self.info().get("title"))








