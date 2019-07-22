from queue import Queue

from policypools.BoundedThreadPoolExecutor import BoundedThreadPoolExecutor


class DiscardOldestThreadPoolExecutor(BoundedThreadPoolExecutor):

    def __init__(self, max_q_size: int = 1, num_workers: int = 1, thread_name_prefix: str = ''):
        """
        Thread pool that will discard the oldest thread in the thread queue if the thread queue is full
        :param max_q_size: the maximum size for the thread queue
        :param num_workers: the maximum number of concurrently running workers
        """
        super(DiscardOldestThreadPoolExecutor, self).__init__(max_q_size, num_workers, thread_name_prefix)

    def submit(self, fn, *args, **kwargs):
        if self._work_queue.qsize() >= self._max_size:
            self._work_queue.get(block=False)
        return super().submit(fn, *args, *kwargs)

    submit.__doc__ = BoundedThreadPoolExecutor.submit.__doc__
