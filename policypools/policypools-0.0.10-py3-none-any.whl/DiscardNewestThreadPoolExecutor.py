import queue

from policypools.AbstractThreadPoolExecutor import PolicyFuture
from policypools.BoundedThreadPoolExecutor import BoundedThreadPoolExecutor


class DiscardNewestThreadPoolExecutor(BoundedThreadPoolExecutor):

    def __init__(self, max_q_size: int = 1, max_workers: int = 1, thread_name_prefix: str = ''):
        """
        Thread pool that will not put the new thread into in the thread queue if the thread queue is full
        :param max_q_size: the maximum size for the thread queue
        :param max_workers: the maximum number of concurrently running workers
        """
        super(DiscardNewestThreadPoolExecutor, self).__init__(max_q_size=max_q_size,
                                                              max_workers=max_workers,
                                                              thread_name_prefix=thread_name_prefix)

    def submit(self, fn, *args, **kwargs):
        if len(self._pre_work_queue) >= self._max_q_size:
            worker = self._pre_work_queue.pop()
            worker.future._state = PolicyFuture.INVALID_STATE
        return super().submit(fn, *args, *kwargs)

    submit.__doc__ = BoundedThreadPoolExecutor.submit.__doc__
