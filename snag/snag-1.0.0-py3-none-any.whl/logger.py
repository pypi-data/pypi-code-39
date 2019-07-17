import sys
class Logger():

    def __init__(self, log, quiet, verbose, echo_limit, log_file_location):
        self.log_flag = log
        self.quiet_flag = quiet
        self.verbose_flag = verbose
        self.log_file_location = log_file_location
        self.echo_limit = echo_limit

    def start(self):
        if self.log_flag:
            self.log_file = open(self.log_file_location, 'w')

    def log(self, message, important=False):
        message = self.truncate(str(message), self.echo_limit)
        if important or self.verbose_flag and not self.quiet_flag:
            print(message)
        if self.log_flag:
            self.log_file.write("\n"+message)

    def close(self):
        if self.log_flag:
            self.log_file.close()    

    def truncate(self, string, length):
        try:
            if len(string) <= length or length == 0:
                return string
            else:
                return string[:length]
        except TypeError as err:
            self.log("Tried to truncate a non-string", True)
            return string
