class OasaTelematicsError(Exception):

    def __init__(self, message, *args, **kwargs):
        self.message = message

    def __str__(self):
        return repr(self.message)