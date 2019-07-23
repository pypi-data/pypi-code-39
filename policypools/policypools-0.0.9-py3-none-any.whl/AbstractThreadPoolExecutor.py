import queue
import time
from abc import abstractmethod, ABC
from concurrent.futures import _base, ThreadPoolExecutor
from concurrent.futures.thread import _WorkItem
from queue import Queue


class AbstractThreadPoolExecutor(ABC, ThreadPoolExecutor):

    FUTURE_INVALID_STATE = "INVALID"

    def __init__(self, max_q_size: int = 1, max_workers: int = None, thread_name_prefix: str = ''):
        """
        Generic Abstract Thread Pool
        :param max_q_size: the maximum size for the thread queue
        :param max_workers: the maximum number of concurrently running workers
        """
        super(AbstractThreadPoolExecutor, self).__init__(max_workers=max_workers, thread_name_prefix=thread_name_prefix)
        self._max_q_size = max_q_size
        self._pre_work_queue = Queue(maxsize=self._max_q_size)

    @abstractmethod
    def submit(self, fn, *args, **kwargs):
        """
        Submits a new thread with the given policy of execution
        :param fn: the function to run in a separate thread
        :param args: the arguments to pass to that function
        :param kwargs: the keyword arguments to pass to that function
        :return: Future for the submitted thread
        """
        e = False
        f = _base.Future()
        f.add_done_callback(self.on_task_complete)
        w = _WorkItem(f, fn, args, kwargs)
        if len(self._threads) < self._max_workers:
            self._work_queue.put(w)
            self._adjust_thread_count()
            e = True
        return f, w, e

    def on_task_complete(self, future):
        """
        Called after a submitted task is completed, looks to replace completed task with one in pre work queue
        :param future: the future for the completed task, unused parameter
        :return: None
        """
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')
            try:
                worker = self._pre_work_queue.get(block=False)
                self._work_queue.put(worker)
                self._adjust_thread_count()
            except queue.Empty:
                pass

    def map(self, fn, *iterables, timeout=None, chunksize=1):
        """
        Returns an iterator equivalent to map(fn, iter).
        :param fn: A callable that will take as many arguments as there are
                passed iterables.
        :param iterables: The arguments to map the function over.
        :param timeout: The maximum number of seconds to wait. If None, then there
                is no limit on the wait time.
        :param chunksize:  The size of the chunks the iterable will be broken into
                before being passed to a child process. This argument is only
                used by ProcessPoolExecutor; it is ignored by
                ThreadPoolExecutor.
        :return: An iterator equivalent to: map(func, *iterables) but the calls may
            be evaluated out-of-order.
        :raises: TimeoutError: If the entire result iterator could not be generated
                before the given timeout.
        :raises: Exception: If fn(*args) raises for any values.
        """
        if timeout is not None:
            end_time = timeout + time.monotonic()

        # Just adding the filter to get rid of the futures that were not actually submitted and to the futures that
        # were submitted successfully, but were removed before they ran
        fs = list(filter(lambda x: x is not None and x._state != AbstractThreadPoolExecutor.FUTURE_INVALID_STATE,
                         [self.submit(fn, *args) for args in zip(*iterables)]))

        # Yield must be hidden in closure so that the futures are submitted
        # before the first iterator value is required.
        def result_iterator():
            try:
                # reverse to keep finishing order
                fs.reverse()
                while fs:
                    # Careful not to keep a reference to the popped future
                    if timeout is None:
                        yield fs.pop().result()
                    else:
                        yield fs.pop().result(end_time - time.monotonic())
            finally:
                for future in fs:
                    future.cancel()
        return result_iterator()


