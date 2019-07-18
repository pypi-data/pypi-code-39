from __init__ import scope

class FatalError(RuntimeError):
    ROBOT_EXIT_ON_FAILURE = True
class Error(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = True