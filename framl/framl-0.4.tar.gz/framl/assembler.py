import os
import shutil
from typing import Pattern, Optional, Union


class Assembler:

    def __init__(self, destination: str, settings: dict = {}):
        self.skeleton_path: str = os.path.dirname(os.path.realpath(__file__)) + "/skeleton"
        self.work_directory: str = destination
        self.destination: Union[str, None] = None
        self.model_name: Union[str, None] = None
        pass

    def create_workspace(self, model_name: str):
        self.model_name = model_name

        os.mkdir(self.work_directory + "/" + self.model_name)
        self.destination = self.work_directory + "/" + self.model_name

    def copy_base(self) -> None:
        if self.destination is None:
            raise Exception("destination path is not defined")

        for item in os.listdir(self.skeleton_path):
            s = os.path.join(self.skeleton_path, item)
            d = os.path.join(self.destination, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

    def add_file(self, content: str, destination_relative_path: str) -> None:
        pass
