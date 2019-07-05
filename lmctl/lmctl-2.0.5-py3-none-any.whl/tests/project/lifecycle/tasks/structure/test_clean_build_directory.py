import unittest
from unittest.mock import patch
import lmctllib.pipeline as pipeline
import lmctllib.project.lifecycle.tasks as lifecycle_tasks
import tests.project.lifecycle.tasks.task_testing_utils as task_testing_utils
import lmctllib.project.lifecycle.tasks.structure as structure_tasks

class TestCleanBuildDirectory(task_testing_utils.ProjectLifecycleTaskTest):

    @patch('lmctllib.project.lifecycle.tasks.structure.clean_build_directory.os.path')
    @patch('lmctllib.project.lifecycle.tasks.structure.clean_build_directory.os')
    def test_directory_created(self, mock_os, mock_os_path):
        mock_os_path.exists.return_value = False
        test_task = structure_tasks.CleanBuildDirectory()
        result = test_task.execute(self._tools, self._products)
        project_tree = self._tools.get_tool(lifecycle_tasks.TOOL_PROJECT_TREE)
        mock_os_path.exists.assert_called_with(project_tree.build().directory())
        mock_os.makedirs.assert_called_with(project_tree.build().directory())
        self.assertEqual(result.code, pipeline.ResultCode.PASSED)

    @patch('lmctllib.project.lifecycle.tasks.structure.clean_build_directory.shutil')
    @patch('lmctllib.project.lifecycle.tasks.structure.clean_build_directory.os.path')
    @patch('lmctllib.project.lifecycle.tasks.structure.clean_build_directory.os')
    def test_existing_directory_removed(self, mock_os, mock_os_path, mock_shutil):
        mock_os_path.exists.return_value = True
        test_task = structure_tasks.CleanBuildDirectory()
        result = test_task.execute(self._tools, self._products)
        project_tree = self._tools.get_tool(lifecycle_tasks.TOOL_PROJECT_TREE)
        mock_os_path.exists.assert_called_with(project_tree.build().directory())
        mock_shutil.rmtree.assert_called_with(project_tree.build().directory())
        mock_os.makedirs.assert_called_with(project_tree.build().directory())
        self.assertEqual(result.code, pipeline.ResultCode.PASSED)

