from tasklog.constants import WORKLOG_DELIMITER
from tasklog.operations.common.tasklogoperation import OperationStatus

def _saveFailedWorklog(tasklogOperation, toFile):
    tasklog = None
    if tasklogOperation.genericWorklog is not None:
        tasklog = "{}".format(tasklogOperation.genericWorklog)
    elif tasklogOperation.rawWorklog is not None:
        tasklog = "{}".format(tasklogOperation.rawWorklog)

    if tasklog is None:
        # FIXME
        pass

    content = "{}\n{}".format(WORKLOG_DELIMITER, tasklog)
    toFile.write(content)


def _saveSuccessWorklog(tasklogOperation, toFile):
    content = "{}\n{}".format(WORKLOG_DELIMITER, tasklogOperation.genericWorklog)
    toFile.write(content)


def saveWorklogs(workLogOperations, filePath):
    with open(filePath, "a") as file:
        for workLogOperation in workLogOperations:
            if workLogOperation.status is OperationStatus.SUCCESS:
                _saveSuccessWorklog(workLogOperation, file)
            else:
                _saveFailedWorklog(workLogOperation, file)

            file.write("\n\n")
