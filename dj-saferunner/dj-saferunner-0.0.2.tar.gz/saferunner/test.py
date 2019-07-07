from django.test import TestCase, override_settings
from django.core import mail

from .tasks import do_something_slowly, ping, hello
from .process_runner import safely_run_processes
from .assertions import (
    assert_call_count,
    get_all_task_calls,
    count_task_calls,
    clear_run_cache
)

from collections import OrderedDict
from unittest import mock
import json


class RunProcessInTestModeTestCase(TestCase):

    def test_run_tasks(self):
        clear_run_cache()
        run_id = 'this_is_a_test'
        task_list = [
            (hello, {"msg": "hi"} , False),
            (do_something_slowly, {"sleep": 10}, True),
        ]
        safely_run_processes(
            run_id = run_id,
            task_list = task_list
        )
        assert_call_count(run_id, 2)

class AssertionsTestCase(TestCase):

    def setUp(self):
        clear_run_cache()
        self.run_id = 'this_is_a_test'
        task_list = [
            (hello, {"msg": "hi"} , False),
            (do_something_slowly, {"sleep": 10}, True),
            (hello, {"msg": "hi"} , False),
        ]
        safely_run_processes(
            run_id = self.run_id,
            task_list = task_list
        )

    def test_can_assert_call_count(self):
        assert_call_count(self.run_id, 3)

    def test_can_get_details_for_a_task(self):
        calls = get_all_task_calls(self.run_id, 'saferunner.tasks.hello')
        self.assertEqual(len(calls), 2)
        for call in calls:
            self.assertEqual(
                call.get('task_name'),
                'saferunner.tasks.hello'
            )

    def test_can_assert_call_count_for_task(self):
        count_task_calls(self.run_id, 'saferunner.tasks.hello', 2)


class RunProcessInForceModeTestCase(TestCase):

    @mock.patch('saferunner.tasks.ping.delay')
    @override_settings(CELERY_ALWAYS_EAGER=True)
    @override_settings(FORCE_RUN_SIDE_EFFECTS='__all__')
    def test_run_tasks_async(self, test_ping):
        res = safely_run_processes(
            'test_run',
            [(ping, {"foo": "bar"}, True)])
        self.assertEqual(test_ping.call_count, 1)

    @override_settings(FORCE_RUN_SIDE_EFFECTS='__all__')
    def test_run_tasks_sync(self):
        results, mocked = safely_run_processes(
            'test_run',
            [(ping, {"foo": "bar"}, False)])
        self.assertEqual(results, ['pong'])

    @override_settings(FORCE_RUN_SIDE_EFFECTS='__all__')
    def test_can_run_multiple_tasks(self):
        results, mocked = safely_run_processes(
            'test_run',
            [
                (ping, {"foo": "bar"}, False),
                (hello, {"msg": "hello world"}, False)
            ]
        )
        self.assertEqual(
            results,
            ['pong', 'hello world']
        )

    @override_settings(FORCE_RUN_SIDE_EFFECTS=['saferunner.tasks.hello'])
    def test_run_only_specific_task(self):
        results, mocked = safely_run_processes(
            'test_run',
            [
                (ping, {"foo": "bar"}, False),
                (hello, {"msg": "hello world"}, False)
            ]
        )
        self.assertEqual(results, ['hello world'])
        self.assertEqual(mocked, ['saferunner.tasks.ping'])