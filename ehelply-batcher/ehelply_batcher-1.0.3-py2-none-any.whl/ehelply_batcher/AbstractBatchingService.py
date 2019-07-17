import time

from ehelply_batcher.Batch import Batch


class AbstractBatchingService(Batch):

    def __init__(self, batch_size: int = 16, max_message_delay: float = 2, sleep_interval: float = 20, debug=False):
        super().__init__(batch_size)

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

        if self.debug:
            print("Starting Batching Service:")
            print("  * Batch size: " + str(self.batch_size) + " items.")
            print("  * Max message delay: " + str(self.max_message_delay) + " minutes.")
            print("  * Delay time after receiving 0 messages: " + str(self.sleep_interval) + " seconds.")
            print("  * Batch timer: " + str(self.batch_timer_max) + " iterations of no messages.")
            print("")

        print("Delegating control of this thread to Batching Service.")
        print("This thread will now be 'locked' by the batching service.")
        print("  * If this is unintended, please start the Batching Service is a new thread.")
        print()
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

            if self.debug:
                print(str(len(messages)) + " messages received.")

            if len(messages) > 0:
                for message in messages:
                    self.receipt_message(message)

                    i = len(messages)
                    if not self.is_message_valid(message):
                        i -= 1
                        continue
                    if self.debug and i != len(messages):
                        print(str(i) + " messages were invalid and discarded.")

                    self._insert(self.form_message(message))

                if self.size() == self.batch_size:
                    if self.debug:
                        print("Releasing batch due to no batch capacity remaining")
                        print()
                    self.release_batch()
                    self._clear()
                    continue

            elif self.batch_timer == self.batch_timer_max:
                if self.debug:
                    print("Releasing batch due to batch timer reaching its maximum")
                    print()
                self.release_batch()
                self._clear()
                continue

            else:
                time.sleep(self.sleep_interval)
                if self.size() > 0:
                    self.batch_timer += 1

            if self.debug:
                print("Batch timer: " + str(self.batch_timer))
                print("Batch size: " + str(self.size()))
                print()
