import logging


class MeLogger(object):
    def __init__(self,
                 logger_name="logger",
                 stdout_level=logging.DEBUG,
                 file_level=logging.DEBUG,
                 log_file_name="log.txt",
                 format="%(asctime)s - %(name)s - {%(filename)s:%(lineno)d} - %(levelname)s - %(message)s",
                 date_format="%Y-%m-%d %H:%M:%S"):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_file_name)
        fh.setLevel(file_level)
        
        ch = logging.StreamHandler()
        ch.setLevel(stdout_level)
        # Create formatter
        formatter = logging.Formatter(format, date_format)
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)
    
    def debug(self, msg):
        # Level 10
        self.logger.debug(msg)
    
    def info(self, msg):
        # Level 20
        self.logger.info(msg)
    
    def warning(self, msg):
        # Level 30
        self.logger.warning(msg)
    
    def error(self, msg):
        # Level 40
        self.logger.error(msg)
