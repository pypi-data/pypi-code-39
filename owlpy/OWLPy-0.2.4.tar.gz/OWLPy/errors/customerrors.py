# define Python user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   def __init__(self):
      pass

class NotFound(Error):
   """Raised when the input value is too small"""
   pass
class PlayerNotFound(NotFound):
   """Raised when the input value is too large"""
   pass

class TeamNotFound(NotFound):
   """Raised when the input value is too large"""
   pass

class MatchNotFound(NotFound):
   """Raised when the input value is too large"""
   pass