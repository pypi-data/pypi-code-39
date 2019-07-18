import time

from ehelply_batcher.Batch import Batch
from ehelply_logger.Logger import Logger


class AbstractBatchingService(Batch):

    def __init__(self, batch_size: int = 16, max_message_delay: float = 2, sleep_interval: float = 20, debug=False,
                 logger: Logger = None):
        super().__init__(batch_size)

        self.logger = logger if logger else Logger(debug_mode=debug)

        # Defines the max time from when the logging service receives a message to when that message will enter the DB
        self.max_message_delay = max_message_delay

        # Defines the responsiveness of the logging service in seconds
        self.sleep_interval = sleep_interval

        if self.sleep_interval > (self.max_message_delay * 60):
            self.sleep_interval = self.max_message_delay * 60

        self.batch_timer_max: int = int(self.max_message_delay * 60 / self.sleep_interval)
        self.batch_timer: int = 0

        if self.batch_timer_max < 1:
            self.batch_timer_max = 1

        self.debug = debug

        self.logger.debug("Starting Batching Service:")
        self.logger.debug("  * Batch size: " + str(self.batch_size) + " items.")
        self.logger.debug("  * Max message delay: " + str(self.max_message_delay) + " minutes.")
        self.logger.debug("  * Delay time after receiving 0 messages: " + str(self.sleep_interval) + " seconds.")
        self.logger.debug("  * Batch timer: " + str(self.batch_timer_max) + " iterations of no messages.")
        self.logger.debug("")

        self.logger.info("Delegating control of this thread to Batching Service.")
        self.logger.info("This thread will now be 'locked' by the batching service.")
        self.logger.info("  * If this is unintended, please start the Batching Service is a new thread.")
        self.logger.info("")
        self._service()

    def release_batch(self) -> bool:
        return True

    def receive(self, limit: int) -> list:
        return []

    def is_message_valid(self, message) -> bool:
        return True

    def receipt_message(self, message) -> bool:
        return True

    def form_message(self, message):
        return message

    def _clear(self):
        super()._clear()
        self.batch_timer = 0

    def _service(self):
        while True:
            capacity = self.capacity()

            messages = self.receive(limit=capacity)

            self.logger.debug(str(len(messages)) + " messages received.")

            if len(messages) > 0:
                i = len(messages)

                for message in messages:
                    self.logger.debug(message)

                    self.receipt_message(message)

                    if not self.is_message_valid(message):
                        i -= 1
                        continue

                    self._insert(self.form_message(message))

                self.logger.debug(str(i) + " messages were invalid and discarded.")

                if self.size() == self.batch_size:
                    self.logger.debug("Releasing batch due to no batch capacity remaining")
                    self.logger.debug("")

                    self.release_batch()
                    self._clear()
                    continue

            elif self.batch_timer == self.batch_timer_max:
                self.logger.debug("Releasing batch due to batch timer reaching its maximum")
                self.logger.debug("")

                self.release_batch()
                self._clear()
                continue

            else:
                time.sleep(self.sleep_interval)
                if self.size() > 0:
                    self.batch_timer += 1

            if self.size() > 0:
                self.logger.debug("Batch timer: " + str(self.batch_timer))
                self.logger.debug("Batch size: " + str(self.size()))
                self.logger.debug()
