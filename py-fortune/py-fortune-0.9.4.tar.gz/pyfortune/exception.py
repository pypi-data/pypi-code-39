class PyfortuneException(Exception):
    pass


class LoginFailureException(PyfortuneException):
    pass


class LoginRequireException(PyfortuneException):
    pass
