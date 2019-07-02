""" Command implementation

"""

from tasklog.helper.logger import logger
from tasklog.operations.common.tasklogreader import readWorklogsFile
from tasklog.operations.common.tasklogoperation import WorklogOperation, OperationStatus, Reason
from tasklog.operations.common.tasklogoperationbuilder import buildWorklogOperations
from tasklog.operations.common.tasklogwriter import saveWorklogs
from tasklog.operations.common.tasklograndom import displayWorklogOperation, exitWithExitCodeIf
from tasklog.helper.slack import SLACK2
from tasklog.constants import EXIT_CODE_FAIL_GENERIC
from pathlib import Path
from shutil import copy
from natural.date import day
import datetime


def _buildDailyMessageForSlack(previousGenericWorklog, plannedGenericWorklog):
    previousDate = previousGenericWorklog.dateTime
    previousContent = previousGenericWorklog.description
    currentDate = plannedGenericWorklog.dateTime
    currentContent = plannedGenericWorklog.description

    previously = day(previousDate.timestamp(), now=currentDate.timestamp())
    now = day(currentDate.timestamp(), now=currentDate.timestamp())

    message = "*{}*\n{}\n\n*{}*\n{}".format(previously.capitalize(), previousContent, now.capitalize(), currentContent)

    return message


def main(config, fromFilePath):
    """ Execute the command.
    :param fromFilePath: Work logs file to read from
    """

    #
    # Setup
    #
    slack = SLACK2()
    slack.connect(config.slack.apiToken)

    exitWithExitCodeIf(
        slack is None or not slack.isConnected(),
        "NOT connected to Slack",
        EXIT_CODE_FAIL_GENERIC
    )

    #
    # Get Worklogs to post
    #
    logger.debug("Reading tasklogs from {:s}.".format(fromFilePath))
    tasklogsFilePath = Path(fromFilePath).resolve()
    backupWorklogsFilePath = Path("{:s}.backup".format(fromFilePath))
    failedWorklogsFilePath = Path("{:s}.failed".format(fromFilePath))
    copy(str(tasklogsFilePath), str(backupWorklogsFilePath))

    genericWorklogs = readWorklogsFile(tasklogsFilePath)

    allWorklogOperations = buildWorklogOperations(genericWorklogs, OperationStatus.PENDING, Reason.UNKNOWN)

    #
    # Update Slack with tasklogs
    #
    logger.debug("Computing daily tasklogs {}".format(genericWorklogs))

    for tasklogOperation in allWorklogOperations:
        hasNoGenericWorklog = tasklogOperation.genericWorklog is None

        if hasNoGenericWorklog:
            tasklogOperation.status = OperationStatus.FAILED
            tasklogOperation.reason = Reason.NO_WORKLOG_PARSED
            continue

    # Sort tasklog by date
    todayDatetime = datetime.datetime.today()
    twoDaysEarlierDatetime = todayDatetime - datetime.timedelta(days=2)

    # Remove tasklog in the future if any
    filteredWorklogOperations = [tasklogOperation for tasklogOperation in allWorklogOperations if
                                 twoDaysEarlierDatetime.date() <= tasklogOperation.genericWorklog.dateTime.date() and tasklogOperation.genericWorklog.dateTime.date() <= todayDatetime.date()
                                 ]

    sortedWorklogOperations = sorted(filteredWorklogOperations,
                                     key=lambda worklogOperation: worklogOperation.genericWorklog.dateTime)

    countWorklogOperations = len(sortedWorklogOperations)

    if countWorklogOperations >= 3:
        # Keep last 2 most recent worklogs
        sortedWorklogOperations = sortedWorklogOperations[-2:]
        pass

    if countWorklogOperations < 2:
        # Min 2 worklog to compute daily
        exitWithExitCodeIf(
            True,
            "Not enough worklog to compute yesterday/today daily",
            EXIT_CODE_FAIL_GENERIC
        )

    previousWorklog = sortedWorklogOperations[0]
    plannedWorklog = sortedWorklogOperations[1]

    dailyMessage = _buildDailyMessageForSlack(previousWorklog.genericWorklog, plannedWorklog.genericWorklog)

    response = slack.postMessage(config.slack.channel, dailyMessage)

    isPosted = response is not None and response["ok"]

    #
    # Summary
    #

    logger.info("Summary: {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
    logger.info("Daily: {}".format("Posted to channel \"{}\"".format(config.slack.channel) if isPosted else "Not Posted"))
    if isPosted:
        logger.info("Message: \n\n{}".format(dailyMessage))
    else:
        logger.error("Error:".format(response["error"]))
