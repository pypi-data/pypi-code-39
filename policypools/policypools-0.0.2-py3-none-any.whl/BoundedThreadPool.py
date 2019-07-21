from threading import Thread

from pools.AbstractThreadPool import AbstractThreadPool


class BoundedThreadPool(AbstractThreadPool):

    def __init__(self, max_q_size: int = 1, num_workers: int = 1):
        """
        Creates a thread pool bounded by the size and the num workers
        since there is no policy this pool throws exceptions
        :param max_q_size: the maximum size for the thread queue
        :param num_workers: the maximum number of concurrently running workers
        """
        super(BoundedThreadPool, self).__init__(max_q_size, num_workers)

    def submit(self, thread: Thread):
        """
        Submits a new thread, may throw queue.Full
        :param thread: the given thread to run
        :return: None
        """
        self.__thread_q.put(thread, block=False)
