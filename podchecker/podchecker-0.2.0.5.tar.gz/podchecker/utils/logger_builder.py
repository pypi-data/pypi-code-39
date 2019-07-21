#! /usr/local/bin/python3
# encoding: utf-8
# Author: LiTing


import logging

"""
    logger = LoggerBuilder.build('pod-logger', logging.INFO).addConsole().addFile('~/Desktop/logfile.txt').logger()
    logger.info('info')
    logger.error('error')
    logger.critical('critical')
    logger.log(logger.level, 'log msg')    
    
    ==========                         =========
       DESC                               TAG
    ----------  had better begin with  ---------
    【error】                             '[!] '
    【stage】                             '-> '
    ----------                         ---------
"""


# ------------------ define builder ------------------

class LoggerBuilder(object):
    s_logger: logging.Logger
    msg_only: bool

    @classmethod
    def build(cls, name='default', level=logging.DEBUG, msgOnly=False):
        def _logger(name, level):
            # 级别 logging.(CRITICAL|ERROR|WARNING|INFO|DEBUG)
            logger = logging.getLogger(name)
            logger.setLevel(level)
            return logger

        builder = cls()
        builder.msg_only = msgOnly
        builder.s_logger = _logger(name, level)
        return builder

    def addConsole(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.s_logger.level)
        console_handler.setFormatter(ConsoleColoredFormatter.standardFormatter(self.msg_only))
        self.s_logger.addHandler(console_handler)
        return self

    def addFile(self, filepath=''):
        if len(filepath) > 0:  # 这里期望判断字符串是否是合法的文件路径格式（无论存在与否）
            file_handler = logging.FileHandler(filepath)
            file_handler.setLevel(self.s_logger.level)
            file_handler.setFormatter(FileNormalFormatter.standardFormatter(self.msg_only))
            # 为了保证console的颜色标记不出现在file里面，这里强制把fileHandler提到所有consoleHandler的前面
            self.s_logger.handlers = [file_handler] + self.s_logger.handlers
        return self

    def logger(self):
        return self.s_logger


# ------------------ define Formatter ------------------

class ConsoleColoredFormatter(logging.Formatter):
    @classmethod
    def standardFormatter(cls, msgOnly=False):
        # 这里不直接用asctime，而是采用datefmt+msecs的方式，因为毫秒在着色时会被截断（暂未查原因）
        if msgOnly:
            fmt = '%(message)s'
        else:
            fmt = '{1}%(asctime)s.%(msecs)03d{0} {2}[%(name)s] %(filename)s:%(lineno)s{0} [%(levelname)s] {3}:{0} %(message)s'\
                .format(kLoggerFore.RESET, kLoggerFore.GREEN, kLoggerFore.CYAN, kLoggerFore.WHITE)
        return ConsoleColoredFormatter(fmt, '%Y-%m-%d %H:%M:%S')

    def format(self, record):
        if record.levelno in Level2ColorMap:
            # 这里进行分段着色（将levelname和msg跟随level颜色进行着色）
            (record.levelname, record.msg) = ('{}{}{}'.format(Level2ColorMap[record.levelno], x, kLoggerFore.RESET)
                                              for x in (record.levelname, record.msg))
            pass
        return super().format(record)

    # HOOK str attr（将str getter属性进行hook）
    # def __getattribute__(self, item):
    #     value = logging.Formatter.__getattribute__(self, item)
    #     if isinstance(value, str):  # 类型判断
    #         if item not in ('name', 'levelname', 'msg'):
    #             value = '{}{}{}'.format(kLoggerFore.WHITE, value, kLoggerFore.RESET)
    #     return value

class FileNormalFormatter(logging.Formatter):
    @classmethod
    def standardFormatter(cls, msgOnly=False):
        if msgOnly:
            fmt = '%(message)s'
        else:
            fmt = '%(asctime)s.%(msecs)03d [%(name)s] %(filename)s:%(lineno)s [%(levelname)s] : %(message)s'
        return FileNormalFormatter(fmt, '%Y-%m-%d %H:%M:%S')


# ... add more ColoredFormatter as above if needed


# ------------------ define color ------------------

LTCSI = '\033['


def code_to_chars(code):
    return LTCSI + str(code) + 'm'


class LTCodes(object):
    def __init__(self):
        # the subclasses declare class attributes which are numbers.
        # Upon instantiation we define instance attributes, which are the same
        # as the class attributes but wrapped with the ANSI escape sequence
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))


class LTFore(LTCodes):
    RESET       = 0
    BLACK       = 30
    RED         = 31
    GREEN       = 32
    YELLOW      = 33
    BLUE        = 34
    MAGENTA     = 35
    CYAN        = 36
    WHITE       = 37


kLoggerFore = LTFore()

Level2ColorMap = {
    logging.CRITICAL: kLoggerFore.MAGENTA,
    logging.ERROR:    kLoggerFore.RED,
    logging.WARNING:  kLoggerFore.YELLOW,
    logging.INFO:     kLoggerFore.WHITE,
    logging.DEBUG:    kLoggerFore.BLUE
}
