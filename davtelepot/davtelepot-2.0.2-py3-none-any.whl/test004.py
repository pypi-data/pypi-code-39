import asyncio
import logging

from bot import Bot


log_formatter = logging.Formatter(
    "%(asctime)s [%(module)-15s %(levelname)-8s]     %(message)s",
    style='%'
)
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(log_formatter)
consoleHandler.setLevel(logging.DEBUG)
root_logger.addHandler(consoleHandler)

logging.getLogger('asyncio').setLevel(logging.WARNING)


sancobot = Bot("197190910:AAGzsK6eliocHcgFu2WLl2baKQ8hGz0ORag")

state = Bot.run(local_host='localhost', port=1400)
print(state)
