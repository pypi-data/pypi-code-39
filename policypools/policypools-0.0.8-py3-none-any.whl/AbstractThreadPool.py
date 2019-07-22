from abc import abstractmethod, ABC
from concurrent.futures import _base, ThreadPoolExecutor
from concurrent.futures.thread import _WorkItem


class AbstractThreadPoolExecutor(ABC, ThreadPoolExecutor):

    def __init__(self, max_q_size: int = 1, max_workers: int = None, thread_name_prefix: str = ''):
        """
        Generic Abstract Thread Pool
        :param max_q_size: the maximum size for the thread queue
        :param max_workers: the maximum number of concurrently running workers
        """
        super(AbstractThreadPoolExecutor, self).__init__(max_workers=max_workers, thread_name_prefix=thread_name_prefix)
        self._max_size = max_q_size

    @abstractmethod
    def submit(self, fn, *args, **kwargs):
        """
        Submits a new thread with the given policy of execution
        :param fn: the function to run in a separate thread
        :param args: the arguments to pass to that function
        :param kwargs: the keyword arguments to pass to that function
        :return: Future for the submitted thread
        """
        f = _base.Future()
        w = _WorkItem(f, fn, args, kwargs)
        return f, w
