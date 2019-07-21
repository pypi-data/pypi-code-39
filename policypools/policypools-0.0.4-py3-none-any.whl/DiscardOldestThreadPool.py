from threading import Thread

from policypools.AbstractThreadPool import AbstractThreadPool


class DiscardOldestThreadPool(AbstractThreadPool):

    def __init__(self, max_q_size: int = 1, num_workers: int = 1):
        """
        Thread pool that will discard the oldest thread in the thread queue if the thread queue is full
        :param max_q_size: the maximum size for the thread queue
        :param num_workers: the maximum number of concurrently running workers
        """
        super(DiscardOldestThreadPool, self).__init__(max_q_size, num_workers)

    def submit(self, thread: Thread):
        """
        Submits a new thread, discarding the oldest thread in queue if queue is full
        :param thread: the given thread to run
        :return: None
        """
        if self.__thread_q.full():
            self.__thread_q.get(block=False)
        self.__thread_q.put(thread)
