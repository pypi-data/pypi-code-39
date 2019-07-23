class LogWindowWriter:
    def __init__(self, window, key):
        self.window = window
        self.key = key

    def write(self, string):
        self.window.Element(self.key).Update(value=string, append=True)


def print_to_log(window, key, string):
    window.Element(key).Update(value=string + "\n", append=True)
