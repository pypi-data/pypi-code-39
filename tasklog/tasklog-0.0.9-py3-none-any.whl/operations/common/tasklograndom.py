from tasklog.commandexception import CommandException


def exitWithExitCodeIf(booleanExpression, message, exitCode):
    if booleanExpression:
        raise CommandException(message, exitCode)


def _formatWorkLogOperation(tasklogOperation):
    return "{:human}".format(tasklogOperation)


def displayWorklogOperation(logger, tasklogOperations):
    for tasklogOperation in tasklogOperations:
        logger.info("\n{}\n{}".format(
            '-' * 80,
            _formatWorkLogOperation(tasklogOperation)
        ))
