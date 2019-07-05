import unittest
from lmctllib.project.lifecycle.tasks import *
from lmctllib.pipeline import *
from lmctllib.journal import *
from lmctllib.project.structure import *

class TestExampleTask(unittest.TestCase):

    def test(self):
        task = ExampleTask("Test")
        tools = TaskTools({"EventLog": Journal(), "ProjectTree": ProjectTree("./hello")})
        task.execute(tools, TaskProducts())
