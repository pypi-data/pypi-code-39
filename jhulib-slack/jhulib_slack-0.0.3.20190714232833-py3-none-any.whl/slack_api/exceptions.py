
class Error(Exception):
    pass

class UserNotFound(Error):
    pass

class UnimplementedSearchMethod(Error):
    pass