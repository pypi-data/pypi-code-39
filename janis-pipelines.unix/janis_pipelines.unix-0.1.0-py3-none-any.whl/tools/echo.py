from janis_core import String, ToolInput, ToolOutput, Stdout
from .unixtool import UnixTool


class Echo(UnixTool):
    @staticmethod
    def tool():
        return "echo"

    def friendly_name(self):
        return "Echo"

    @staticmethod
    def base_command():
        return "echo"

    def inputs(self):
        return [ToolInput("inp", String(), position=0)]

    def outputs(self):
        return [ToolOutput("out", Stdout())]
