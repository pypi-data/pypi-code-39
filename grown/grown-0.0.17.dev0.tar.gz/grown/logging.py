import ulogging


class FileHandler(object):
    def __init__(self, filename, mode="a"):
        self.mode = mode
        self.terminator = "\n"
        self.filename = filename
        self._f = open(self.filename, self.mode)

    def read(self, *args):
        return self._f.read(*args)

    def readinto(self, *args):
        return self._f.readinto(*args)

    def write(self, *args):
        self._f.write(*args)
        self._f.flush()

    def flush(self):
        self._f.flush()

    def close(self):
        self._f.close()

    def seek(self, *args):
        return self._f.seek(*args)


ulogging.basicConfig(
    ulogging.DEBUG,
    'run_information.log',
    FileHandler('run_information.log')
)
grown_log = ulogging.getLogger("grown")
