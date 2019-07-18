#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from clogger import CustomLogger

if __name__ == '__main__':

    logger = CustomLogger(
        handler_name="MyCustomLogger",
        stream_handler=True,
        file_handler=True,
        filenames="default.log",
        level="INFO",
    )

    logger.starting_message()

    logger.debug("Debug test")
    logger.info("Info test")
    logger.warning("Warning test")
    logger.error("Error test")

    try:
        1 + 'a'
    except:
        logger.exception("Exception test (exception follows)")

    logger.exiting_message()
