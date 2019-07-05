import unittest
import uuid
import lmctllib.pipeline as pipeline
import lmctllib.journal as journal
import lmctllib.project.lifecycle.tasks as lifecycle_tasks
import lmctllib.project.structure as project_struct
import lmctllib.project.model as project_model

class ProjectLifecycleTaskTest(unittest.TestCase):

    def setUp(self):
        self._set_up_default_tools()
        self._set_up_default_products()

    def _set_up_default_products(self):
        self._products = pipeline.TaskProducts()

    def _set_up_default_tools(self):
        self._tools = self._build_tools()

    def _build_tools(self, **kwargs):
        project_tree_builder = kwargs.get('project_tree_builder', self._default_project_tree_builder)
        project_builder = kwargs.get('project_builder', self._default_project_builder)
        journal_builder = kwargs.get('journal_builder', self._default_journal_builder)
        init_tools = {lifecycle_tasks.TOOL_PROJECT_TREE: project_tree_builder(), lifecycle_tasks.TOOL_PROJECT: project_builder(), lifecycle_tasks.TOOL_EVENT_LOG: journal_builder()}
        return pipeline.TaskTools(init_tools)

    def _default_project_builder(self):
        return project_model.Project('TestProject', project_model.Vnfcs())

    def _default_journal_builder(self):
        return journal.Journal()

    def _default_project_tree_builder(self):
        return project_struct.ProjectTree('testing/{0}'.format(uuid.uuid1()))
