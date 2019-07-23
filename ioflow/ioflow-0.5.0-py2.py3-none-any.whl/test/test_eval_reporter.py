from ioflow.eval_reporter import get_eval_reporter


def test_eval_reporter():
    config = {
        'task_id': '5d30109d69d245705d0b4e42',
        'eval_reporter_scheme': 'http',
        'eval_reporter_url': 'http://10.43.10.20:25005/hdfs/uploadEvaluateFile'
    }

    eval_reporter = get_eval_reporter(config)

    for i in range(100):
        eval_reporter.record_x_and_y([i], [i*i])

    eval_reporter.submit()
