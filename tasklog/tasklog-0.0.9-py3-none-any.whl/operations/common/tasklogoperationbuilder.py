from tasklog.operations.common.tasklogoperation import WorklogOperation

def buildWorklogOperations(tasklogs, defaultOperationStatus, defaultOperationReason):
    tasklogOperations = []

    for (rawWorklog, genericWorklog) in tasklogs:
        tasklogOperation = WorklogOperation(genericWorklog, rawWorklog, defaultOperationStatus, defaultOperationReason)
        tasklogOperations.append(tasklogOperation)

    return tasklogOperations

