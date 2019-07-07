from django.core.cache import cache

def clear_run_cache():
    cache.clear()

def get_process_run(run_id):
    key = "calls:{}".format(run_id)
    return cache.get(key)

def assert_call_count(run_id, expected_call_count):
    actual_call_count = len(get_process_run(run_id))
    assertion_message = 'Actual call count ({}) does not equal expected call count: {}'.format(
        actual_call_count,
        expected_call_count
    )
    assert actual_call_count == expected_call_count, assertion_message

def get_all_task_calls(run_id, task_name):
    calls = []
    run = get_process_run(run_id)
    for call in run:
        # sprint(call.get('task_name'), task_name)
        if call.get('task_name') == task_name:
            calls.append(call)
    return calls

def count_task_calls(run_id, task_name, expected_count):
    calls = get_all_task_calls(run_id, task_name)
    call_count = len(calls)
    assert call_count == expected_count, 'Actual call count for {} ({}) does not equal expected call count: {}.\nHere are the calls that were made:\n{}'.format(
        task_name,
        call_count,
        expected_count,
        calls
    )
