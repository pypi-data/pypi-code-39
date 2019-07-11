import os
import re
import subprocess
import threading

from queue import Queue, Full
import time


class LogRotator(object):
    def __init__(self, directory, prefix="hour_"):
        self.directory = directory
        try:
            os.makedirs(self.directory)
        except:
            pass
        self.prefix = prefix
        self.file = None
        self.file_hour = None
        self.current_filename = None
        self.rotation_time = 3600
        self.gzip_timestamp = time.time() - self.rotation_time/60
        self.queue = None

    def get_hour(self):
        return int(time.time() / self.rotation_time)

    def filename(self, hour):
        return "{}{}.log".format(self.prefix, hour)

    def filepath(self, hour):
        return os.path.join(self.directory, self.filename(hour))

    def _open_file(self):
        try:
            if self.file:
                self.file.close()
        except:
            pass

        self.file_hour = self.get_hour()
        self.file = open(self.filepath(self.file_hour), "a")
        self.current_filename = self.filename(self.file_hour)

    def gzip(self):
        for file in os.listdir(self.directory):
            if file.endswith(".log") and re.match(self.prefix + "\d+\.log", file) and file != self.current_filename:
                subprocess.call("gzip {}".format(os.path.join(self.directory, file)), shell=True)

    def logrotate(self):
        if self.file:
            new_hour = self.get_hour()
            if new_hour != self.file_hour:
                self._open_file()
        else:
            self._open_file()

        if abs(time.time() - self.gzip_timestamp) > self.rotation_time/60:
            self.gzip()

    def write(self, line, flush=False):
        self.logrotate()
        self.file.write(line + "\n")
        if flush:
            self.file.flush()

    def run(self):
        while True:
            self.write(self.queue.get())

    def start_as_thread(self):
        self.queue = Queue(maxsize=1000)
        thread = threading.Thread(target=self.run)
        thread.setDaemon(True)
        thread.start()
        return thread

    def put_on_queue(self, line):
        if self.queue:
            try:
                self.queue.put_nowait(line)
            except Full:
                return "Full"
        else:
            return "Not running"
        return ""
