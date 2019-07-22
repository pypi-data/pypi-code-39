from os import cpu_count

from policypools.AbstractThreadPool import AbstractThreadPoolExecutor


class InfiniteThreadPool(AbstractThreadPoolExecutor):

    def __init__(self, thread_name_prefix: str = ''):
        """
        Infinite thread pool, very large queue size and num workers set based off computer specs
        """
        super(InfiniteThreadPool, self).__init__(max_workers=cpu_count() * 10, thread_name_prefix=thread_name_prefix)

    def submit(self, fn, *args, **kwargs):
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')
            future, worker = super().submit(fn, *args, *kwargs)
            self._work_queue.put(worker)
            self._adjust_thread_count()
            return future

    submit.__doc__ = AbstractThreadPoolExecutor.submit.__doc__
