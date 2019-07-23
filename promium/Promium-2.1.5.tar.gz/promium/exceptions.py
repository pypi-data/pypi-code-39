

class PromiumException(Exception):
    pass


class PromiumTimeout(PromiumException):
    def __init__(self, message="no error message", seconds=10, screen=None):
        self.message = f"{message} (waited {seconds} seconds)"
        if screen:
            from promium.common import decode_and_upload_screen
            self.message += f"\nScreenshot: {decode_and_upload_screen(screen)}"
        super(PromiumTimeout, self).__init__(self.message)


class ElementLocationException(PromiumException):
    pass


class LocatorException(PromiumException):
    pass


class BrowserConsoleException(PromiumException):
    pass
