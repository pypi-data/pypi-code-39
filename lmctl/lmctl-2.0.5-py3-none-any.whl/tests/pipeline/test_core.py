import unittest
import unittest.mock as mock
from lmctllib.pipeline import *

class TestResultCode(unittest.TestCase):

    def test_order(self):
        self.assertGreater(ResultCode.FAILED.value, ResultCode.SKIPPED.value)
        self.assertGreater(ResultCode.SKIPPED.value, ResultCode.PASSED.value)

class TestTaskResult(unittest.TestCase):

    def test_no_name(self):
        with self.assertRaises(ValueError) as context:
            result = TaskResult(None, None)
        self.assertTrue("Task name not defined" in str(context.exception)) 

    def test_no_code(self):
        with self.assertRaises(ValueError) as context:
            result = TaskResult("Test", None)
        self.assertTrue("Code not defined" in str(context.exception))

    def test_task_name(self):
        result = TaskResult("Testing", ResultCode.PASSED)
        self.assertEqual(result.task_name, "Testing")

    def test_code(self):
        result = TaskResult("Testing", ResultCode.SKIPPED)
        self.assertEqual(result.code, ResultCode.SKIPPED)

    def test_remarks(self):
        result = TaskResult("Testing", ResultCode.SKIPPED, ["Remark1", "Remark2"])
        self.assertEqual(len(result.remarks), 2)
        self.assertEqual(result.remarks[0], "Remark1")
        self.assertEqual(result.remarks[1], "Remark2")

    def test_passed_report(self):
        result = TaskResult("TestTask", ResultCode.PASSED)
        report = result.report()
        self.assertEqual(report, "TestTask - PASSED")

    def test_skipped_report(self):
        result = TaskResult("TestTask", ResultCode.SKIPPED)
        report = result.report()
        self.assertEqual(report, "TestTask - SKIPPED")

    def test_failed_report(self):
        result = TaskResult("TestTask", ResultCode.FAILED)
        report = result.report()
        self.assertEqual(report, "TestTask - FAILED")

    def test_remarks_in_report(self):
        result = TaskResult("TestTask", ResultCode.FAILED, ["Remark1", "Remark2"])
        report = result.report()
        self.assertEqual(report, "TestTask - FAILED: \n    Remark1\n    Remark2")

    def test_remarks_in_report_with_indent(self):
        result = TaskResult("TestTask", ResultCode.FAILED, ["Remark1", "Remark2"])
        report = result.report(2)
        self.assertEqual(report, "        TestTask - FAILED: \n            Remark1\n            Remark2")

    def test_failed_creator(self):
        result = TaskResult.failed("TestTask", ["Made up error"])
        self.assertEqual(result.task_name, "TestTask")
        self.assertEqual(result.code, ResultCode.FAILED)
        self.assertEqual(len(result.remarks), 1)
        self.assertEqual(result.remarks[0], "Made up error")
 
    def test_failed_creator_no_reasons(self):
        result = TaskResult.failed("TestTask", None)
        self.assertEqual(result.task_name, "TestTask")
        self.assertEqual(result.code, ResultCode.FAILED)
        self.assertEqual(len(result.remarks), 1)
        self.assertEqual(result.remarks[0], "Failure reason not given")

    def test_skipped_creator(self):
        result = TaskResult.skipped("TestTask", ["Made up reason"])
        self.assertEqual(result.task_name, "TestTask")
        self.assertEqual(result.code, ResultCode.SKIPPED)
        self.assertEqual(len(result.remarks), 1)
        self.assertEqual(result.remarks[0], "Made up reason")

    def test_skipped_creator_no_reasons(self):
        result = TaskResult.skipped("TestTask", None)
        self.assertEqual(result.task_name, "TestTask")
        self.assertEqual(result.code, ResultCode.SKIPPED)
        self.assertEqual(len(result.remarks), 0)

    def test_passed_creator(self):
        result = TaskResult.passed("TestTask")
        self.assertEqual(result.task_name, "TestTask")
        self.assertEqual(result.code, ResultCode.PASSED)

    def test_passed_creator_with_remarks(self):
        result = TaskResult.passed("TestTask", ["Remark1", "Remark2"])
        self.assertEqual(result.task_name, "TestTask")
        self.assertEqual(result.code, ResultCode.PASSED)
        self.assertEqual(len(result.remarks), 2)
        self.assertEqual(result.remarks[0], "Remark1")
        self.assertEqual(result.remarks[1], "Remark2")


class TestTaskProducts(unittest.TestCase):

    def test_set_value(self):
        products = TaskProducts()
        products.set_value("A", 1)
        self.assertEqual(products.get_value("A"), 1)

    def test_set_replaces_value(self):
        products = TaskProducts()
        products.set_value("A", 1)
        products.set_value("A", 2)
        self.assertEqual(products.get_value("A"), 2)

    def test_get_value_not_exists(self):
        products = TaskProducts()
        with self.assertRaises(ValueError) as context:
            products.get_value("A")
        self.assertTrue("No value found with key: A" in str(context.exception)) 

    def test_get_optional_value(self):
        products = TaskProducts()
        products.set_value("A", 1)
        self.assertEqual(products.get_optional_value("A"), 1)
    
    def test_get_optional_value_not_exists(self):
        products = TaskProducts()
        self.assertIsNone(products.get_optional_value("A"))

    def test_has_value(self):
        products = TaskProducts()
        self.assertFalse(products.has_value("A"))
        products.set_value("A", None)
        self.assertFalse(products.has_value("A"))
        products.set_value("A", 123)
        self.assertTrue(products.has_value("A"))

class TestTaskTools(unittest.TestCase):

    def test_define_with_no_tools(self):
        tools = TaskTools()

    def test_get_tool(self):
        tools = TaskTools({"testtool": "Just a string"})
        self.assertEqual(tools.get_tool("testtool"), "Just a string")

    def test_get_tool_not_exists(self):
        tools = TaskTools({"testtool": "Just a string"})
        with self.assertRaises(ValueError) as context:
            tools.get_tool("not_a_tool")
        self.assertTrue("No task tool found with name: not_a_tool" in str(context.exception)) 

class TestWorkerTask(unittest.TestCase):

    def test_task_name(self):
        worker_task = WorkerTask("WorkA", mock.MagicMock(name="work"))
        self.assertEqual(worker_task.task_name, "WorkA")

    def test_no_work(self):
        with self.assertRaises(ValueError) as context:
            worker_task = WorkerTask("WorkA", None)
        self.assertTrue("A work function must be provided to a Worker Task" in str(context.exception))
  
    def test_work_not_a_function(self):
        with self.assertRaises(ValueError) as context:
            worker_task = WorkerTask("WorkA", "not a function")
        self.assertTrue("Work function provided to Worker Task must be a callable function but got a: str" in str(context.exception))

    def test_calls_work_on_execute(self):
        mock_work = mock.MagicMock(name="work")
        mock_work.return_value = None
        worker_task = WorkerTask("WorkA", mock_work)
        tools = TaskTools()
        products = TaskProducts()
        worker_task.execute(tools, products)
        mock_work.assert_called_once_with("WorkA", tools, products)

    def test_return_passed_when_work_returns_nothing(self):
        mock_work = mock.MagicMock(name="work")
        mock_work.return_value = None
        worker_task = WorkerTask("WorkA", mock_work)
        tools = TaskTools()
        products = TaskProducts()
        result = worker_task.execute(tools, products)
        self.assertEqual(result.code, ResultCode.PASSED)

    def test_return_result_returned_by_work(self):
        mock_work = mock.MagicMock(name="work")
        mock_work.return_value = TaskResult.skipped("WorkA")
        worker_task = WorkerTask("WorkA", mock_work)
        tools = TaskTools()
        products = TaskProducts()
        result = worker_task.execute(tools, products)
        self.assertEqual(result, mock_work.return_value)

    def test_return_result_from_work_must_have_task_name(self):
        mock_work = mock.MagicMock(name="work")
        mock_work.return_value = TaskResult.skipped("Some other task")
        worker_task = WorkerTask("WorkA", mock_work)
        tools = TaskTools()
        products = TaskProducts()
        with self.assertRaises(ValueError) as context:
            worker_task.execute(tools, products)
        self.assertTrue("Worker Task functions should not return a TaskResult with an alternative task name: expected=WorkA, got=Some other task" in str(context.exception))

    def test_return_failed_result_on_exception(self):
        mock_work = mock.MagicMock(name="work", side_effect=Exception("Made up exception"))
        worker_task = WorkerTask("WorkA", mock_work)
        tools = TaskTools()
        products = TaskProducts()
        result = worker_task.execute(tools, products)
        self.assertEqual(result.code, ResultCode.FAILED)
        self.assertEqual(len(result.remarks), 1)
        self.assertEqual(result.remarks[0], "Made up exception")


class FixedTask(Task):

    def __init__(self, return_value: TaskResult):
        self.__return_value = return_value
        super().__init__(self.__return_value.task_name)

    def execute(self, tools: TaskTools, products: TaskProducts=TaskProducts()):
        return self.__return_value


class testPipeline(unittest.TestCase):

    def test_task_name(self):
        pipeline = Pipeline("Test Pipeline", [])
        self.assertEqual(pipeline.task_name, "Test Pipeline")
    
    @mock.patch("lmctllib.pipeline.Task")
    @mock.patch("lmctllib.pipeline.Task")
    def test_execute(self, mock_task_a, mock_task_b):
        mock_task_a.task_name.return_value = "TaskA"
        mock_task_a.execute.return_value = TaskResult.passed("TaskA")
        mock_task_b.task_name.return_value = "TaskB"
        mock_task_b.execute.return_value = TaskResult.passed("TaskB")
        pipeline = Pipeline("Test Pipeline", [mock_task_a, mock_task_b])
        tools = TaskTools()
        products = TaskProducts()
        result = pipeline.execute(tools, products)
        self.assertEqual(result.code, ResultCode.PASSED)
        self.assertEqual(result.task_name, "Test Pipeline")
        mock_task_a.execute.assert_called_once_with(tools, products)
        mock_task_b.execute.assert_called_once_with(tools, products)
    
    @mock.patch("lmctllib.pipeline.Task")
    @mock.patch("lmctllib.pipeline.Task")
    def test_execute_ignore_skipped(self, mock_task_a, mock_task_b):
        mock_task_a.task_name.return_value = "TaskA"
        mock_task_a.execute.return_value = TaskResult.skipped("TaskA")
        mock_task_b.task_name.return_value = "TaskB"
        mock_task_b.execute.return_value = TaskResult.passed("TaskB")
        pipeline = Pipeline("Test Pipeline", [mock_task_a, mock_task_b])
        tools = TaskTools()
        products = TaskProducts()
        result = pipeline.execute(tools, products)
        self.assertEqual(result.code, ResultCode.PASSED)
        self.assertEqual(result.task_name, "Test Pipeline")
        mock_task_a.execute.assert_called_once_with(tools, products)
        mock_task_b.execute.assert_called_once_with(tools, products)
 
    @mock.patch("lmctllib.pipeline.Task")
    @mock.patch("lmctllib.pipeline.Task")
    def test_execute_fail_on_failed_task(self, mock_task_a, mock_task_b):
        mock_task_a.task_name.return_value = "TaskA"
        mock_task_a.execute.return_value = TaskResult.failed("TaskA", ["Made up failure reason"])
        mock_task_b.task_name.return_value = "TaskB"
        mock_task_b.execute.return_value = TaskResult.passed("TaskB")
        pipeline = Pipeline("Test Pipeline", [mock_task_a, mock_task_b])
        tools = TaskTools()
        products = TaskProducts()
        result = pipeline.execute(tools, products)
        self.assertEqual(result.code, ResultCode.FAILED)
        self.assertEqual(result.task_name, "Test Pipeline")
        self.assertEqual(len(result.remarks), 1)
        self.assertEqual(result.remarks[0], mock_task_a.execute.return_value.report())
        mock_task_a.execute.assert_called_once_with(tools, products)
        mock_task_b.execute.assert_not_called()
