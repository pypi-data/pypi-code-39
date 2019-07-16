

class Pipeline:
    def __init__(self, read_function, transform_function, write_function):
        self.read = read_function
        self.transform = transform_function
        self.write = write_function

    def execute(self):
        sources = self.read()
        result = self.transform(sources)
        self.write(result)
