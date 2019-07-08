""" We need to stop this task """
import asyncio
import logging

LOGGER = logging.getLogger(__name__)


class Broadcaster:
    """ This broadcaster reads from a queue and passes to a consumer """

    def __init__(self):
        self.task = None
        self._broadcast_q_ = asyncio.Queue()

    def start(self, queue, consumer):
        """ start and store our task """
        self.task = asyncio.ensure_future(self.broadcaster(queue, consumer))

    async def stop(self):
        """ usung globals and module works """
        LOGGER.info("stopping broadcaster")
        self.task.cancel()
        # await self.task

    @classmethod
    async def broadcaster(cls, queue, consumer):
        """ Connect websockets to manager broadcast queue """
        while True:
            value = await queue.get()
            await consumer(*value)
            queue.task_done()
