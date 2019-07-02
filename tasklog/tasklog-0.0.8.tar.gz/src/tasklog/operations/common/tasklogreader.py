import re
from tasklog.constants import WORKLOG_DELIMITER
from tasklog.operations.common.tasklogparser import parseGenericWorklog


def readWorklogsFile(filePath=None):
    with open(filePath, 'r') as content_file:
        # Read file content
        content = content_file.read()

        # Split raw content into raw work log
        rawWorklogs = re.split(WORKLOG_DELIMITER, content)

        # Remove spurious whitespaces on either side of the text
        rawWorklogs = [rawWorklog.strip() for rawWorklog in rawWorklogs]

        # Keep non empty tasklogs only
        rawWorklogs = args = [rawWorklog for rawWorklog in rawWorklogs if rawWorklog]

        # Parse tasklogs
        genericWorklogs = _parseWorklogs(rawWorklogs)

        return genericWorklogs


def _parseWorklogs(rawWorklogs):
    genericWorklogs = []

    for rawWorklog in rawWorklogs:
        genericWorklog = None
        try:
            genericWorklog = parseGenericWorklog(rawWorklog)
        except:
            pass

        genericWorklogs.append((rawWorklog, genericWorklog))

    return genericWorklogs
