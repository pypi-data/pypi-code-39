""" Application commands common to all interfaces.

"""
from tasklog.operations.submitWorklog.main import main as submitWorklogCommand
from tasklog.operations.submitDaily.main import main as submitDailyCommand

__all__ = ['submitWorklogCommand', 'submitDailyCommand']
