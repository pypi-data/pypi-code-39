import logging
log = logging.getLogger()

class Pipeline:
    """ repository of functions to find the task that can make an output
    """
    def __init__(self):
        self.funcs = []
        self.opaths = []

    def add(self, func):
        """ add a func to the database """
        if func.opath not in self.opaths:
            self.funcs.append(func)
            self.opaths.append(func.opath)

    def find(self, output):
        """ return task for making output """
        for func in self.funcs:
            if func.parse_output() == output:
                return func
        return None