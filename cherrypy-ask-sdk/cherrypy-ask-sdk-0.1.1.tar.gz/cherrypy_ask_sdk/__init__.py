import cherrypy

from cherrypy_ask_sdk.ask_sdk_skill_tool import AskSdkSkillTool

__version__ = "0.1.1"


def add_in_toolbox(toolbox=cherrypy.tools, name="ask_sdk_skill", priority=50):
    ask_sdk_skill_tool = cherrypy._cptools.Tool(
        'before_handler', AskSdkSkillTool(), name, priority
    )
    setattr(toolbox, name, ask_sdk_skill_tool)
