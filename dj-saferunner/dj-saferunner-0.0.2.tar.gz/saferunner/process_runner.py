from django.conf import settings
from django.core import mail
from django.core.cache import cache
from sentry_sdk import (
    capture_exception,
    push_scope
)

from collections import OrderedDict
import sys, json

TEST_MODE = sys.argv[1:2] == ['test']

def get_task_name(task):
    attrs_to_try = ['name', '__name__']
    for attr in attrs_to_try:
        task_name = getattr(task, attr, None)
        if task_name is not None: return task_name
    return str(task)

def store_test_debug_information(run_id, task, task_args, is_async):
    args_string = str(OrderedDict(task_args))
    task_name = get_task_name(task)
    task_signature = "{}:{}".format(
        task_name,
        args_string
    )
    meta = {
        "task_name": task_name,
        "task_args": args_string,
        "is_async": is_async
    }

    key = "calls:{}".format(run_id)
    call_list = cache.get(key)
    if call_list is None: call_list = []
    call_list.append(meta)
    cache.set(key, call_list)


def should_run(task):
    FORCE_RUN_SIDE_EFFECTS = getattr(settings, 'FORCE_RUN_SIDE_EFFECTS', False)
    if not TEST_MODE: return True

    # everything from here refers to test mode:
    # =====================================
    no_force_desired = FORCE_RUN_SIDE_EFFECTS == False
    if no_force_desired: return False

    if FORCE_RUN_SIDE_EFFECTS == '__all__': return True

    task_name = get_task_name(task)
    passthrough_desired_for_this_task = task_name in FORCE_RUN_SIDE_EFFECTS
    if passthrough_desired_for_this_task: return True

    return False

def run_task(task, task_args, is_async):
    if is_async:
        return task.delay(**task_args)
    else:
        return task(**task_args)

def safely_run_processes(run_id, task_list=[]):
    '''
    Run a list of tasks

    @params: run_id: an ID that can be used to identify this set of calls
    @params: task_list

    Usage:
    from .tasks import (
        ping,
        pong
    )
    task_list = [
        # task, args, async
        (ping, {"foo", "bar"}, True)
        (pong, {}, True)
    ]
    safely_run_processes(run_id='postsavesignals', task_list=task_list)
    '''
    results = []
    mocked = []
    for task, task_args, is_async in task_list:
        # is_async = getattr(task, 'delay', None) is not None
        if should_run(task):
            with_sentry = getattr(settings, 'SAFERUNNER_USE_SENTRY', False)
            if not with_sentry:
                results.append(run_task(task, task_args, is_async))
            else:
                try:
                    results.append(run_task(task, task_args, is_async))
                except Exception as e:
                    from sentry_sdk import configure_scope, push_scope
                    with push_scope() as scope:
                        scope.set_extra('Task', task)
                        scope.set_extra('task_args', task_args)
                        scope.set_extra('running async', is_async)
                        capture_exception(e)
        else:
            store_test_debug_information(run_id, task, task_args, is_async)
            mocked.append(get_task_name(task))
    return (results, mocked)