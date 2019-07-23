from ioflow.task_status import get_task_status


def test_task_status():
    config = {
        "progress_report_url": "http://10.43.17.53:25005/redis",
        "task_id": "1234567890",
        "task_status_schema": "http"
    }

    task_status = get_task_status(config)

    task_status.send_status(task_status.START_DOWNLOAD_CORPUS)

    task_status.send_progress(50)


def test_task_status_multiple_turn():
    config = {
        "progress_report_url": "http://10.43.17.53:25005/redis",
        "task_id": "1234567890",
        "task_status_schema": "http"
    }

    task_status = get_task_status(config)

    for status in [
        task_status.START_DOWNLOAD_CORPUS,
        task_status.START_PROCESS_CORPUS,
        task_status.START_TRAIN,
        task_status.START_TEST,
        task_status.START_UPLOAD_MODEL,
    ]:
        task_status.send_status(status)


def test_task_status_multiple_progress():
    config = {
        "progress_report_url": "http://10.43.17.53:25005/redis",
        "task_id": "1234567890",
        "task_status_schema": "http"
    }

    task_status = get_task_status(config)

    for i in range(0, 101):
        task_status.send_progress(i)
