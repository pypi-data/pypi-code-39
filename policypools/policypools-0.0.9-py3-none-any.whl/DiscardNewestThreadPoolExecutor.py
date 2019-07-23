import queue

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
        try:
            return super().submit(fn, *args, *kwargs)
        except queue.Full:
            return None

    submit.__doc__ = BoundedThreadPoolExecutor.submit.__doc__
