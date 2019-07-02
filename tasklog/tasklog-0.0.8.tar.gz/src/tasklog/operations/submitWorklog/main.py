""" Command implementation

"""

import re
from tasklog.helper.logger import logger
from tasklog.operations.common.tasklogreader import readWorklogsFile
from tasklog.operations.common.tasklogoperation import OperationStatus, Reason
from tasklog.operations.common.tasklogoperationbuilder import buildWorklogOperations
from tasklog.operations.common.tasklograndom import displayWorklogOperation, exitWithExitCodeIf
from tasklog.operations.common.tasklogwriter import saveWorklogs
from tasklog.helper.jira import JIRA2
from tasklog.constants import EXIT_CODE_FAIL_GENERIC
from pathlib import Path
from shutil import copy
import datetime


def isProjectAvailable(projectKey, projectKeys):
    hasProject = projectKey in projectKeys
    return hasProject


def extractDayXs(sentences, validChoices):
    # Find out whether sentence contains one of the valid choices
    matchingSentences = []

    for choice in validChoices:
        patternString = r"((?i){}) (\d+)".format(choice)
        pattern = re.compile(patternString)
        for sentence in sentences:
            results = pattern.findall(sentence)
            for result in results:
                # Format of data appended (day, number)
                matchingSentences.append(result)

    return matchingSentences


def generateNextDayX(dayXPairs, defaultDayString, defaultDayNumber):
    numbers = [int(number) for (day, number) in dayXPairs]

    if len(numbers) == 0:
        return (defaultDayString, defaultDayNumber)

    maxNumber = max(numbers)
    nextNumber = maxNumber + 1

    (day, number) = dayXPairs[0]

    return (day, nextNumber)


def getBestMatchingIssueType(preferedIssueTypeNamesSortedASC, availableIssueTypesSortedASC):
    # Map issue type names to issue type objects
    preferedIssueTypes = []
    for preferedIssueTypeName in preferedIssueTypeNamesSortedASC:
        for availableIssueType in availableIssueTypesSortedASC:
            if availableIssueType.name == preferedIssueTypeName:
                preferedIssueTypes.append(availableIssueType)

    availableIssueTypesIdsSortedASC = [issueType.id for issueType in availableIssueTypesSortedASC]

    # Find best match
    matchings = [preferedIssueType for preferedIssueType in preferedIssueTypes
                 if preferedIssueType.id in availableIssueTypesIdsSortedASC
                 ]
    return matchings


def main(config, fromFilePath):
    """ Execute the command.
    :param fromFilePath: Work logs file to read from
    """

    #
    # Setup
    #
    jira = JIRA2()
    jira.connect(config.jira.serverURL, config.jira.username, config.jira.password,
                 config.jira.verifyCertificate)

    exitWithExitCodeIf(
        jira is None or not jira.isConnected(),
        "NOT logged in as {:s} to JIRA at ${:s}".format(config.jira.username, config.jira.serverURL),
        EXIT_CODE_FAIL_GENERIC
    )

    projects = jira.getProjects()
    projectKeys = [project.key for project in projects]

    jiraUsers = jira.getUsers(config.jira.username, projectKeys)

    exitWithExitCodeIf(
        len(jiraUsers) == 0,
        "User {:s} details not found".format(config.jira.username),
        EXIT_CODE_FAIL_GENERIC
    )

    jiraUser = jiraUsers[0]

    preferedIssueTypeNames = config.issue.creation.typePreferedOrder
    issuesTypesPerProjectKey = {}

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
    # Update JIRA with tasklogs
    #
    logger.debug("Inserting tasklogs {}".format(genericWorklogs))

    for tasklogOperation in allWorklogOperations:
        hasNoGenericWorklog = tasklogOperation.genericWorklog is None

        if hasNoGenericWorklog:
            tasklogOperation.status = OperationStatus.FAILED
            tasklogOperation.reason = Reason.NO_WORKLOG_PARSED
            continue

        if not isProjectAvailable(tasklogOperation.genericWorklog.projectKey, projectKeys):
            tasklogOperation.status = OperationStatus.FAILED
            tasklogOperation.reason = Reason.NO_PROJECT_FOUND

    for tasklogOperation in allWorklogOperations:
        if tasklogOperation.status is not OperationStatus.PENDING:
            continue

        projectKey = tasklogOperation.genericWorklog.projectKey

        # Get/Create Issue on the server
        requireNewIssue = tasklogOperation.genericWorklog.issueKey is None
        if requireNewIssue:
            # Get most recent issues
            jiraIssues = jira.getAllIssuesOnProject(projectKey, maxIssues=50)

            # Find most recent Day X used

            issueDayXLikeSummaryPairs = [issue.fields.summary.strip() for issue in jiraIssues]
            issueDayXLikeSummaryPairs = extractDayXs(issueDayXLikeSummaryPairs, config.dayX.prefixPreferedOrder)
            (day, number) = generateNextDayX(
                issueDayXLikeSummaryPairs,
                config.dayX.prefixPreferedOrder[0],
                1
            )

            issueTitleSummary = "{} {}".format(day, number)
            # Get most issue type to create issue with
            if not (projectKey in issuesTypesPerProjectKey):
                # Get allowed issue types for a project
                projectIssueTypes = jira.getIssueTypesForProject(projectKey)

                # Get best matching issueType
                bestMatchingIssueTypes = getBestMatchingIssueType(preferedIssueTypeNames, projectIssueTypes)

                if len(bestMatchingIssueTypes) == 0:
                    # Fallback to project issue types
                    bestMatchingIssueTypes = projectIssueTypes

                if len(bestMatchingIssueTypes) == 0:
                    tasklogOperation.status = OperationStatus.FAILED
                    tasklogOperation.reason = Reason.NO_ISSUE_TYPE_FOUND
                    continue

                bestIssueType = bestMatchingIssueTypes[0]
                issuesTypesPerProjectKey[projectKey] = bestIssueType

            issueType = issuesTypesPerProjectKey[projectKey]
            jiraIssue = jira.createIssue(projectKey, jiraUser, issueTitleSummary, "", issueType.name)
        else:
            jiraIssue = jira.getIssue(tasklogOperation.genericWorklog.issueKey)

        # Update import data with issue
        tasklogOperation.genericWorklog.issueKey = jiraIssue.key

        # Post issue's import to the server
        jiraWorkLog = jira.addWorkLog(jiraUser, jiraIssue, tasklogOperation.genericWorklog)
        tasklogOperation.customWorklog = jiraWorkLog

        if jiraWorkLog is None:
            tasklogOperation.status = OperationStatus.FAILED
            tasklogOperation.reason = Reason.NO_WORKLOG_APPENDED
            continue

        tasklogOperation.status = OperationStatus.SUCCESS
        tasklogOperation.reason = Reason.NO_APPLICABLE_REASON

    #
    # Summary of tasklogs inserted
    #
    successWorkLogOperations = [tasklogOperation for tasklogOperation in allWorklogOperations
                                if tasklogOperation.status is OperationStatus.SUCCESS
                                ]

    failedWorkLogOperations = [tasklogOperation for tasklogOperation in allWorklogOperations
                               if tasklogOperation.status is not OperationStatus.SUCCESS
                               ]

    totalWorkLog = len(allWorklogOperations)
    totalSuccessWorklog = len(successWorkLogOperations)
    totalFailedWorkLog = len(failedWorkLogOperations)

    logger.info("Summary: {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
    logger.info("Worklogs ADDED: {}/{}".format(totalSuccessWorklog, totalWorkLog))
    displayWorklogOperation(logger, successWorkLogOperations)

    if totalWorkLog != totalSuccessWorklog:
        logger.info("Worklogs NOT ADDED {}/{}".format(totalFailedWorkLog, totalWorkLog))
        displayWorklogOperation(logger, failedWorkLogOperations)
        saveWorklogs(failedWorkLogOperations, failedWorklogsFilePath)

    exitWithExitCodeIf(
        len(failedWorkLogOperations) > 0,
        "Work logs not added stored at {}".format(failedWorklogsFilePath.resolve()),
        EXIT_CODE_FAIL_GENERIC
    )
