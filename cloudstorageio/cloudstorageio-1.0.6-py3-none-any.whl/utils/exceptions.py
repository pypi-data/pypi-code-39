class Exceptions(Exception):

    class ValueError(Exception):
        pass

    class FileNotFoundError(Exception):
        pass

    class ConnectionRefusedError(Exception):
        pass

    class NotADirectoryError(Exception):
        pass

    class InvalidPathError(Exception):
        pass
