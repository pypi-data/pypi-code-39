from enum import Enum
from tasklog.operations.common.generictasklog import GenericWorklog

class OperationStatus(Enum):
    UNKNOWN = 0
    SUCCESS = 1
    FAILED = 2
    PENDING = 3


class Reason(Enum):
    UNKNOWN = 0
    NO_APPLICABLE_REASON = 1
    NO_WORKLOG_PARSED = 2
    NO_ISSUE_TYPE_FOUND = 3
    NO_PROJECT_FOUND = 4
    NO_WORKLOG_APPENDED = 5


class WorklogOperation:
    def __init__(self, genericWorklog=None, rawWorkLog=None, status=OperationStatus.UNKNOWN, reason=Reason.UNKNOWN):
        self.customWorklog = None
        self.genericWorklog = genericWorklog
        self.rawWorklog = rawWorkLog
        self.status = status
        self.reason = reason

    def __format__(self, format):
        if format == 'human':
            customWorklog = self.customWorklog
            if customWorklog is not None:
                customWorklog = "{} ({} - {})\n{}\n{}\n{}".format(
                    customWorklog.issueId,
                    customWorklog.id,
                    customWorklog.author.name,
                    customWorklog.started,
                    customWorklog.timeSpent,
                    customWorklog.comment
                )

            genericWorklog = self.genericWorklog
            if genericWorklog is None:
                genericWorklog = GenericWorklog()

            value = "RAW:\n{}\n\nGENERIC:\n{:human}\n\nCUSTOM:\n{}\n\nSTATUS:\n{}\n\nREASON:\n{}".format(
                self.rawWorklog,
                genericWorklog,
                customWorklog,
                self.status,
                self.reason,
            )

            return value

        return "{} {} {} {} {}".format(
            self.projectKey,
            self.issueKey,
            self.date,
            self.durationInSeconds,
            self.description,
        )
