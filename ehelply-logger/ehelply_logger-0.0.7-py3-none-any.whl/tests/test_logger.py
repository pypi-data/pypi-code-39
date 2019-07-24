from ehelply_logger.Logger import Logger
from ehelply_logger.LogFormatter import LogFormatter


def test_basic_out_1():
    print("test_basic_out_1")
    logger: Logger = Logger()
    logger.info("info test")
    logger.warning("warning test")
    logger.severe("severe test")
    logger.debug("debug test which should not print")
    logger.debugg("debugg test which should not print")
    logger.debuggg("debuggg test which should not print")
    print()


def test_basic_out_2():
    print("test_basic_out_2")
    logger: Logger = Logger(debug_mode=1)
    logger.info("info test")
    logger.warning("warning test")
    logger.severe("severe test")
    logger.debug("debug test")
    logger.debugg("debugg test which should not print")
    logger.debuggg("debuggg test which should not print")
    print()


def test_basic_out_3():
    print("test_basic_out_3")
    logger: Logger = Logger(debug_mode=2)
    logger.info("info test")
    logger.warning("warning test")
    logger.severe("severe test")
    logger.debug("debug test")
    logger.debugg("debugg test")
    logger.debuggg("debuggg test which should not print")
    print()


def test_basic_out_4():
    print("test_basic_out_4")
    logger: Logger = Logger(debug_mode=3)
    logger.info("info test")
    logger.warning("warning test")
    logger.severe("severe test")
    logger.debug("debug test")
    logger.debugg("debugg test")
    logger.debuggg("debuggg test")
    print()


def test_basic_prefix_1():
    print("test_basic_prefix_1")
    logger: Logger = Logger(prefix="logger", debug_mode=3)
    logger.info("info test")
    logger.warning("warning test")
    logger.severe("severe test")
    logger.debug("debug test")
    logger.debugg("debugg test")
    logger.debuggg("debuggg test")
    print()


def test_basic_prefix_2():
    print("test_basic_prefix_2")
    logger: Logger = Logger(prefix="logger", debug_mode=3)
    logger = logger.spinoff()
    logger.info("info test")
    logger.warning("warning test")
    logger.severe("severe test")
    logger.debug("debug test")
    logger.debugg("debugg test")
    logger.debuggg("debuggg test")
    print()


def test_basic_prefix_3():
    print("test_basic_prefix_3")
    logger: Logger = Logger(prefix="logger", debug_mode=3)
    logger = logger.spinoff(prefix="logger2")
    logger.info("info test")
    logger.warning("warning test")
    logger.severe("severe test")
    logger.debug("debug test")
    logger.debugg("debugg test")
    logger.debuggg("debuggg test")
    print()


class CustomFormatter(LogFormatter):
    def do_timestamps(self) -> bool:
        return True


def test_basic_formatter_1():
    print("test_basic_formatter_1")
    logger: Logger = Logger(prefix="logger", debug_mode=3, log_formatter=CustomFormatter())
    logger.info("info test")
    logger.warning("warning test")
    logger.severe("severe test")
    logger.debug("debug test")
    logger.debugg("debugg test")
    logger.debuggg("debuggg test")
    print()


test_basic_out_1()
test_basic_out_2()
test_basic_out_3()
test_basic_out_4()
test_basic_prefix_1()
test_basic_prefix_2()
test_basic_prefix_3()
test_basic_formatter_1()
