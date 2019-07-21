from threading import Thread

from policypools.AbstractThreadPool import AbstractThreadPool


class DiscardNewestThreadPool(AbstractThreadPool):

    def __init__(self, max_q_size: int = 1, num_workers: int = 1):
        """
        Thread pool that will not put the new thread into in the thread queue if the thread queue is full
        :param max_q_size: the maximum size for the thread queue
        :param num_workers: the maximum number of concurrently running workers
        """
        super(DiscardNewestThreadPool, self).__init__(max_q_size, num_workers)

    def submit(self, thread: Thread):
        """
        Submits a new thread, discarding the the given thread if the queue is full
        :param thread: the given thread to run
        :return: None
        """
        if not self._thread_q.full():
            self._thread_q.put(thread)
