class LogWindowWriter:
    def __init__(self, window, key):
        self.window = window
        self.key = key

    def write(self, string):
        self.window.Element(self.key).Update(value=string, append=True)
