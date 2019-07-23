import time

import numpy as np

from ioflow.performance_metrics import get_performance_metrics
from test.utils import LogisticFunction


def test_HttpPerformanceMetrics():
    config = {
        'task_id': '5d005b6cb775fa16367a2f74',
        'metrics_report_scheme': 'http',
        'metrics_report_url': 'http://10.43.17.53:25005/savedrawingdata'
    }
    pm = get_performance_metrics(config)
    pm.send_metrics(
        {
            "trainLoss": "2",
             "trainAccuray": "3",
             "testLoss": "4",
             "testAccuray": "66"
        },
        step=1
    )


def test_HttpPerformanceMetrics_all_data():
    config = {
        'task_id': '5d030495b775fa16367a2f88',
        'metrics_report_scheme': 'http',
        'metrics_report_url': 'http://10.43.17.53:25005/savedrawingdata'
    }

    lf = LogisticFunction(K=.09, x_0=50)
    result = lf(np.array(range(1, 101)))
    acc = result
    loss = 1 - result

    pm = get_performance_metrics(config)
    for i in range(len(result)):
        time.sleep(0.1)
        pm.send_metrics({"acc": acc[i], "loss": loss[i]}, step=i)
